from flask import Flask, render_template, request, redirect, flash, url_for
app = Flask(__name__)

@app.route('/')
def login():
	
	error = ""
	try:
		if request.method == "POST":
			attempted_username = request.form['username']
			attempted_password = request.form['password']

			if attempted_username == "admin" and attempted_password == "password":
				return redirect(url_for('lef'))
				
			else:
				error = "invalid credentials. Try again"

		return render_template("login.html", error = error)


	except Exception as e:
		# flash(e)
		return render_template("login.html", error = error)


	return render_template("login.html")

@app.route('/about')
def lef():
	return render_template("caseManage.html")

if __name__ == "__main__":
	app.debug = True
	app.run()