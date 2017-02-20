from flask import Flask 
from flask import request
from flask import make_response
from flask import redirect
from flask import abort

app = Flask(__name__)#创建flask类实例

@app.route("/")
def index():
	return "<h1>hello</h1>"

@app.route("/tiao")
def tiao():
	return redirect("https://www.baidu.com")
@app.route("/user",methods=["POST"])
def user():
	name = request.args.get("name")
	return "<h1>hello %s</h1>"%name

@app.route('/user/<name>')
def username(name):
	if name == 'test':
		abort(500)
	return "<h1>hello %s</h1>"%name

@app.route("/req_test")
def req_test():
	val=""
	for key,value in request.args.items():
		val +="%s = %s<br>"%(key,value)
	return val;

@app.route("/res_test")
def res():
	response = make_response("<h1>hello ren</h1>")
	response.set_cookie("name","klren")
	return response;

if __name__ == '__main__':#Python入口程序
	app.run(debug=True)#使其运行于本地服务器