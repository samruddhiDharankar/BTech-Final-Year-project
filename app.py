from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime

app = Flask(__name__)

conn = MySQLdb.connect(host="sql12.freemysqlhosting.net",user="sql12366978",password="PlNdNPiBmB",db="sql12366978") 

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
		# print(attempted_username)
		# print(attempted_password)
		cursor = conn.cursor()
		now = datetime.now()
		query1 = "INSERT INTO user (userName,password) VALUES (%s, %s)"
		val1 = (attempted_username,attempted_password)
		cursor.execute(query1, val1)

		# query2 = "SELECT userID FROM user WHERE userName = '%s'" % attempted_username
		# cursor.execute(query2)
		# records = cursor.fetchall()
		# print("Total number of rows is: ", cursor.rowcount)
		# for row in records:
		# 	userid = row[0]
		# print("id", userid)
		
		print("yeye")
		query = "INSERT INTO session (loginTime,userID_fk) VALUES (%s, (SELECT userID FROM user WHERE userName=%s))"

		# query3 = "UPDATE session SET loginTime = %s userID = %s WHERE userID = %s" 
		val =  (now ,attempted_username)
		cursor.execute(query,val)
		print("eee")
		conn.commit()
		return redirect(url_for('caseManage'))
	
	return render_template("login.html")
	

@app.route('/caseManage',methods=['POST','GET'])
def caseManage():
	return render_template("caseManage.html")

@app.route('/newCase')
def Case():
	return render_template("newCase.html")	

@app.route('/overview')
def over():
	return render_template("overview.html")	


if __name__ == "__main__":
	app.debug = True
	app.run()