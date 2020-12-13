from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb import escape_string as thwart
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

from flask_session import Session

  
app = Flask(__name__)

SESSION_TYPE = 'filesystem'
app.config.from_object(__name__)
Session(app)

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sammy:root@localhost/database_be'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#for regular mysql
conn = MySQLdb.connect(host="localhost",user="sammy",password="root",db="database_be") 
cursor = conn.cursor()



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
		attempted_investigatorID = request.form.get("investigatorID")
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
	print("caseIDDDD" + case_id)
	all_data = Finding.query.filter_by(caseID_fk=case_id).all()
	return render_template("Overview.html", Finding = all_data)

#insert data to mysql database via html forms
@app.route('/insert', methods = ['POST'])
def insert():
	if request.method == 'POST':
		Description = request.form['Description_of_the_Finding']
		Evidence_Details = request.form['Evidence_details']
		#File = request.form('File')
		Datetime_of_the_Finding = request.form['findingtime']
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
	
#display four values from sql table file
@app.route('/')
def display_tableinfo(): 
    cursor.execute("select * from vmdb") 
    data = cursor.fetchall() #data from database 
    return render_template("display_table.html", value=data) 


@app.route('/eviRepo', methods = ['POST','GET'])
def eviRepo():
	return render_template("eviRepo.html")	
	
if __name__ == "__main__":
	app.debug = True
	app.run()
