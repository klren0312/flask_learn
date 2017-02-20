from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import flash
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap 

app = Flask(__name__)
#数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/zblog'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
db = SQLAlchemy(app)#实例化SQLAlchemy

#配置session
app.config['SECRET_KEY'] = '123456'
bootstrap = Bootstrap(app)
 

@app.route("/login",methods=["GET"])
def login():
	return render_template("/btlogin.html")

@app.route("/login",methods=["POST"])
def loginPost():
    username=request.form.get("username","")
    password=request.form.get("password","")
    if username=="test" and password=="123" :
        session["user"]=username
        return render_template("/index.html",name=username,site_name='myblog')
    else:
        flash("您输入的用户名或密码错误")
        return render_template("/btlogin.html") #返回的仍为登录页

if __name__ == '__main__':
	app.run(debug=True)