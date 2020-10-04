from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL,MySQLdb
from MySQLdb import escape_string as thwart
from datetime import datetime

app = Flask(__name__)

conn = MySQLdb.connect(host="localhost",user="sammy",password="root",db="databast_be") 
cursor = conn.cursor()
@app.route('/', methods=['GET'])
def index():
	return redirect(url_for('login'))

@app.route('/login', methods=['GET','POST'])
def login():
	# print("hello")
	# print(request.method)
	
	if(request.method == "POST"):
		# print(request.method)
		attempted_username = request.form.get("username")
		attempted_password = request.form.get("password")
		
		# cursor = conn.cursor()
		query = "SELECT password FROM user WHERE userName = '%s'" % attempted_username
		# value = (attempted_username)
		cursor.execute(query)
		records = cursor.fetchall()
		for row in records:
		 	Pass = row[0]
		print(Pass)
		print("aattempted", attempted_password)
		
		if(Pass == attempted_password):
			print("matched")
			now = datetime.now()
			query1 = "INSERT INTO session (loginTime,userID_fk) VALUES (%s, (SELECT userID FROM user WHERE userName=%s))"

			val1 =  (now ,attempted_username)
			cursor.execute(query1,val1)
			conn.commit()
			return redirect(url_for('caseManage'))

		# print(attempted_username)
		# print(attempted_password)
		
		# now = datetime.now()
		# query1 = "INSERT INTO user (userName,password) VALUES (%s, %s)"
		# val1 = (attempted_username,attempted_password)
		# cursor.execute(query1, val1)

		# query2 = "SELECT userID FROM user WHERE userName = '%s'" % attempted_username
		# cursor.execute(query2)
		# records = cursor.fetchall()
		# print("Total number of rows is: ", cursor.rowcount)
		# for row in records:
		# 	userid = row[0]
		# print("id", userid)
		
		# print("yeye")
		
		# print("eee")
		# conn.commit()
		# return redirect(url_for('caseManage'))
	
	return render_template("login.html")
	

@app.route('/caseManage',methods=['POST','GET'])
def caseManage():
	if(request.method == "POST"):
		attempted_caseID = request.form.get("caseID")
		attempted_investigatorID = request.form.get("investigatorID")
		attempted_casePassword = request.form.get("casePassword")

		query2 = "SELECT caseID FROM case_table WHERE caseID = '%s'" % attempted_caseID"
		cursor.execute(query2)
		records = cursor.fetchall()
		print("Total number of rows is: ", cursor.rowcount)

		if(cursor.rowcount == 1):
			return redirect(url_for('overview'))


	
	return render_template("caseManage.html")

@app.route('/newCase',methods=['POST','GET'])
def newCase():
	if(request.method == "POST"):
		attempted_caseID = request.form.get("caseID")
		attempted_caseName = request.form.get("caseName")
		attempted_description = request.form.get("description")
		attempted_investigatorName = request.form.get("investigatorName")
		attempted_casePassword = request.form.get("casePassword")
		
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
		
			#SELECT userID FROM (USER) TABLE
			# query2 = "SELECT userID FROM user WHERE userName = '%s'" % attempted_investigatorName
			# cursor.execute(query2)
			# records = cursor.fetchall()
			# print("Total number of rows is: ", cursor.rowcount)
			# for row in records:
			# 	userid = row[0]
			# print("id", userid)

			# query3 = "INSERT INTO case_user_mapping(caseID_fk,userID_fk) VALUES(%s, (SELECT userID FROM user WHERE userName=%s))"
			
			#INSERT INTO (CASE_USER_MAPPING) TABLE
			cursor.execute('''INSERT INTO case_user_mapping(caseID_fk,userID_fk) VALUES(%s, (SELECT userID FROM user WHERE userName=%s))''', (attempted_caseID,attempted_investigatorName))
			
			now = datetime.now()
			#INSERT INTO THE (FINDINGS) TABLE
			cursor.execute('''INSERT INTO findings(caseID_fk,date) VALUES(%s, %s)''', (attempted_caseID,now))
		
		
		conn.commit()


	return render_template("newCase.html")	

@app.route('/overview')
def overview():
	return render_template("overview.html")	


if __name__ == "__main__":
	app.debug = True
	app.run()