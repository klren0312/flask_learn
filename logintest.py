from flask import Flask 
from flask import request
app=Flask(__name__)

@app.route("/login",methods=["GET"])
def login():
	html="<form method='post' action='http://127.0.0.1:5000/login'>"\
		 "<table>"\
		 "<tr><td>please input username</td><td><input type='text' name='username'/></td></tr>" \
		 "<tr><td>please input password</td><td><input type='password' name='password'/></td></tr>" \
		 "<tr><td><input type='submit' value='登录'/></td></tr>" \
		 "</table>"\
		 "</form>"
	return html

@app.route("/login",methods=["POST"])
def loginPost():
	username = request.form.get("username","")
	password = request.form.get("password","")
	if username == "test" and password=="123":
		return "login success"
	else:
		return "login fail"

if __name__ == '__main__':
	app.run(debug=True)