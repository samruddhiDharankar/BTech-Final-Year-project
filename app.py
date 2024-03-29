from flask import Flask, render_template, request, redirect, flash, url_for, session, json, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb import escape_string as thwart
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
import sqlite3
import time
import random
import subprocess
import json
import html
import os
from werkzeug.utils import secure_filename
from flask import Markup
# from flask_cors import CORS, cross_origin
# cors = CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
  
app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1234@localhost/databast_be'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#for regular mysql
conn = MySQLdb.connect(host="localhost",user="root",password="1234",db="databast_be")
cursor = conn.cursor()

path = os.getcwd()
# file Upload
app.secret_key = "secret key"
UPLOAD_FOLDER = os.path.join(path,'fetched')

# Make directory if uploads is not exists
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/', methods=['GET'])
def index():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():

	# print(request.method)
	if(request.method == "POST"):
		# print(request.method)
		attempted_username = request.form.get("username")
		attempted_password = request.form.get("password")
		
		query = "SELECT password FROM user WHERE userName = '%s'" % attempted_username
		
		cursor.execute(query)
		records = cursor.fetchall()
		for row in records:
		 	Pass = row[0]
		print(Pass)
		print("attempted", attempted_password)
		
		if(Pass == attempted_password):
			print("matched")
			now = datetime.now()
			query1 = "INSERT INTO session (loginTime,userID_fk) VALUES (%s, (SELECT userID FROM user WHERE userName=%s))"

			val1 =  (now ,attempted_username)
			cursor.execute(query1,val1)
			conn.commit()

			session['user_name'] = attempted_username					#session saved for USER_NAME	

			return redirect(url_for('caseManage'))

	return render_template("login.html")
	

@app.route('/caseManage',methods=['POST','GET'])
def caseManage():
	if(request.method == "POST"):
		attempted_caseID = request.form.get("caseID")
		# attempted_investigatorID = request.form.get("investigatorID")

		attempted_casePassword = request.form.get("casePassword")
		

		
		query2 = "SELECT caseID FROM case_table WHERE caseID = '%s'" % attempted_caseID
		cursor.execute(query2)
		records = cursor.fetchall()
		print("Total number of rows is: ", cursor.rowcount)

		if(cursor.rowcount == 1):
			session['case_id'] = attempted_caseID
			return redirect(url_for('Overview'))


	
	return render_template("caseManage.html")

@app.route('/newCase',methods=['POST','GET'])
def newCase():
	if(request.method == "POST"):
		attempted_caseID = request.form.get("caseID")
		attempted_caseName = request.form.get("caseName")
		attempted_description = request.form.get("description")
		attempted_investigatorName = request.form.get("investigatorName")
		attempted_casePassword = request.form.get("casePassword")
		
		sequence = session.get('user_name')
		print("seqqqq" + sequence)
		session['case_id'] = attempted_caseID	
		val1 = (attempted_caseID,attempted_caseName,attempted_description,attempted_casePassword)
		print("val", val1)

		query2 = "SELECT caseID FROM case_table WHERE caseID = '%s'" % attempted_caseID
		cursor.execute(query2)
		records = cursor.fetchall()
		print("Total number of rows is: ", cursor.rowcount)

		if(cursor.rowcount > 0):
			feedback = "caseID already exists"
			return render_template("newCase.html", feedback=feedback)
		else:
			#INSERT INTO THE CASE_TABLE
			query1 = "INSERT INTO case_table(caseID,caseName,description,casePassword) VALUES(%s, %s, %s, %s)"
			cursor.execute(query1, val1)
		
			#INSERT INTO (CASE_USER_MAPPING) TABLE
			cursor.execute('''INSERT INTO case_user_mapping(caseID_fk,userID_fk) VALUES(%s, (SELECT userID FROM user WHERE userName=%s))''', (attempted_caseID,attempted_investigatorName))
			
			# now = datetime.now()
			# #INSERT INTO THE (FINDINGS) TABLE
			# cursor.execute('''INSERT INTO findings(caseID_fk,Datetime_of_the_Finding) VALUES(%s, %s)''', (attempted_caseID,now))
		
		
		conn.commit()


	return render_template("newCase.html")	
	# return redirect(url_for('Overview'))


#Finding table in database db_name
db = SQLAlchemy(app)
class Finding(db.Model):
	__tablename__ = 'Finding'
	findingID = db.Column('findingID',db.Integer, primary_key = True, autoincrement=True)
	user_name = db.Column('user_name',db.Text) 
	caseID_fk = db.Column('caseID_fk',db.Integer) 
	Description = db.Column('Description',db.Text)
	Evidence_Details = db.Column('Evidence_Details',db.Text)
	# File = db.Column('File',db.LargeBinary)
	Datetime_of_the_Finding = db.Column('Datetime_of_the_Finding',db.DateTime)
  
	def __init__(self, user_name,caseID_fk, Description, Evidence_Details, Datetime_of_the_Finding):
		self.user_name = user_name
		self.caseID_fk = caseID_fk
		self.Description = Description
		self.Evidence_Details = Evidence_Details
		self.Datetime_of_the_Finding = Datetime_of_the_Finding

db.create_all()

@app.route('/Overview', methods = ['POST','GET'])
def Overview():
	case_id = session.get('case_id')

	#cursor.execute("SELECT * FROM Finding WHERE caseId_fk= %S, (case_id)")
	#all_data = cursor.fetchall()
	all_data = Finding.query.filter_by(caseID_fk=case_id).all()
	
	return render_template("Overview.html", Finding = all_data)

#insert data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		Description = request.form['Description_of_the_Finding']
		Evidence_Details = request.form['Evidence_details']
		#File = request.form('File')
		# Datetime_of_the_Finding = request.form['findingtime']
		Datetime_of_the_Finding = datetime.now()
		name = session.get('user_name')
		case_id = session.get('case_id')

		my_data123 = (name, case_id, Description, Evidence_Details, Datetime_of_the_Finding)
		query123 = "INSERT INTO Finding(user_name,caseID_fk,Description,Evidence_Details,Datetime_of_the_Finding) VALUES(%s, %s, %s, %s, %s)"
		cursor.execute(query123, my_data123)
		conn.commit()
		#my_data = Finding(name, case_id, Description, Evidence_Details, Datetime_of_the_Finding)
		#db.session.add(my_data)
		#db.session.commit()
		return redirect(url_for('Overview'))


# @app.route('/fetch', methods=['GET'])
# def index1():
# 	return redirect(url_for('fetch'))


# @app.route('/fetch', methods=['GET','POST'])
# def fetch():

# 	#print(request.method)
# 	cursor = conn.cursor()

# 	if(request.method == "GET"or "POST"):
		
# 		#now = datetime.now()
# 		query1 = "select distinct vmid from mems";
# 		cursor.execute(query1)
# 		result = cursor.fetchall()
# 		myresult=sorted(result)
# 		myresult = str(myresult)
# 		myresult= re.sub('[(,)]','',myresult)
# 		myresult= myresult[1:-1:2]
		
# 	#	for row in myresult:
			
# 	#		print(row)

# 	return render_template("fetch.html",myresult=myresult)

# def index2():
# 	return redirect(url_for('fetch'))



# @app.route('/fetch', methods=['GET','POST'])
# def afterfetch():
# 	fetch()
# 	print(request.method)
# 	cursor = conn.cursor()

# 	if(request.method == "GET"or "POST"):
# 		vr = request.form.get("vmid")
# 		print(request.method)
# 		print(vr)

# 		cursor.execute("SELECT path FROM mems WHERE VMID= %s", (vr))

# 		my = cursor.fetchall()
# 		res=my[13:]
# 		for h in my:
# 			subprocess.run(["scp", res, "prasad@192.168.43.198:my"])
# 	return render_template("fetch.html",res=res)


cursor.execute("SELECT DISTINCT VMID FROM memory ORDER BY VMID")
vmid_dropdown_options1 = cursor.fetchall()


@app.route('/fetch', methods = ['POST','GET'])
def fetch():
	return render_template("fetch.html",myresult = vmid_dropdown_options1)


@app.route('/fetch1', methods = ['GET', 'POST'])
def fetch1():
	if request.method == 'GET' or 'POST':
		cc=-1
		VMID = request.args.get("VMID")
		print(VMID)
		strqr="SELECT path FROM memory WHERE VMID='%s'"% VMID
		
		cursor.execute(strqr)
		qq = cursor.fetchall()
		
		for h in qq:
			
			h=str(h)
			g=h[2:-3]
			#print(h)
			res=g[12:]
			res=(str(res))
			#cc=("E:\memory\\")
			d=("\\fetched")
			cc=UPLOAD_FOLDER+d
			cc=cc+str(res)
			print(cc)
			#subprocess.run(["scp",res, cc])
			file = open(cc, 'w+')
			
		isExist = os.path.exists(cc) 
		if(cc==-1):
			message = Markup("VMID not selected")
		elif(isExist==True):
			message = Markup("Done!!!Check Fetched Folder")
		else:	
			message = Markup("Successfully Fetched!!!!")
		flash(message)
		
		return render_template("fetch.html",myresult = vmid_dropdown_options1,value1=qq)

			# strqry1="SELECT * FROM vmdb WHERE VMID='%s'"% VMID
			# print(strqry1)
			# cursor.execute(strqry1)
			# query98 = cursor.fetchall()
			# return render_template("Analysis.html", value1 = query98, value2 = vmid_dropdown_options, value3 = ipv4_dropdown_options)


# @app.route('/eviRepo', methods = ['POST','GET'])
# def eviRepo():
# 	return render_template("eviRepo.html")


cursor.execute("SELECT DISTINCT VMID FROM vmdb ORDER BY VMID")
vmid_dropdown_options = cursor.fetchall()

cursor.execute("SELECT DISTINCT IPV4 FROM vmdb")
ipv4_dropdown_options = cursor.fetchall()

with open('./cpu2.json', 'r') as myfile:
    json1 = myfile.read()

#print(json1) #just to confirm
@app.route("/getjson", methods = ['POST','GET'])
def json_():
   data = json1
   return data

input_dict = json.loads(json1)

output_dict = [x for x in input_dict if x[2] == 14]

json2 = json.dumps(output_dict)

@app.route('/Analysis', methods = ['POST','GET'])
def Analysis():
	cursor.execute("select * from vmdb")
	query = cursor.fetchall()
	# data = map(json1,query)
	# print(data)
	# return jsonify({json1 : json1})
	return render_template("Analysis.html",data = json1, value1 = query, value2 = vmid_dropdown_options, value3 = ipv4_dropdown_options)

# json.dumps(json1)



@app.route('/filter', methods = ['GET', 'POST'])
def filter():
	if request.method == 'GET' or 'POST':
		VMID = request.args.get("VMID")
		IPV4 = request.args.get("IPV4")

		#VMID = request.form['VMID']
		#IPV4 = request.form['IPV4']
		

		#cursor.execute("SELECT * FROM vmdb WHERE VMID= %S AND IPV4 = %S, (VMID,IPV4)")
		#cursor.execute("SELECT * FROM vmdb WHERE VMID= %S, (VMID)")

		#cursor.execute("SELECT * FROM vmdb WHERE VMID=%S",str(VMID))
		#VMID = 18


		print(json2)
		# print(VMID)
		# print(IPV4)
		strqry="SELECT * FROM vmdb WHERE VMID='%s'"% VMID
		# print(strqry)
		cursor.execute(strqry)
		query9 = cursor.fetchall()
		return render_template("Analysis.html", data = json1, value1 = query9, value2 = vmid_dropdown_options, value3 = ipv4_dropdown_options)


@app.route('/display_table', methods = ['POST','GET'])
def display_tableinfo(): 
	cursor.execute("select * from vmdb") 
	data = cursor.fetchall() #data from database 
	return render_template("display_table.html", value=data)

	
if __name__ == "__main__":
	app.debug = True
	app.run()