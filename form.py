from flask import Flask, render_template, request, redirect, flash, url_for
from flask_mysqldb import MySQL,MySQLdb
from datetime import datetime
import subprocess

app = Flask(__name__)
conn = MySQLdb.connect(host="localhost",user="root",password="Chinmay@99",db="dbbb") 

#conn = MySQLdb.connect(host="sql12.freemysqlhosting.net",user="sql12366978",password="PlNdNPiBmB",db="sql12366978") 

@app.route('/', methods=['GET'])
def index():
	return redirect(url_for('fetch'))
@app.route('/fetch', methods=['GET','POST'])
def fetch():	
		if(request.method == "POST"):
		# print(request.method)
		attempted_textbox = request.form.get("txtbox")

		cursor = conn.cursor()
		now = datetime.now()
		query1 = "SELECT path FROM user WHERE VMID=%s"
		val1 = (txtbox)
		cursor.execute(query1, val1)
		myresult = cursor.fetchall()
		res=myresult[13:]
		conn.commit()
		return redirect(url_for('caseManage'))
	
	return render_template("fetch.html")		
if __name__ == "__main__":
	app.debug = True
	app.run()	

subprocess.run(["scp", res, myresult])