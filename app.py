from flask import Flask, render_template, request, redirect, flash, url_for
app = Flask(__name__)

@app.route('/')
def login():
	
	error = ""
	try:
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			

		return render_template("login.html", error = error)


	except Exception as e:
		# flash(e)
		return render_template("login.html", error = error)


	return render_template("login.html")

@app.route('/caseManage')
def caseMan():
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