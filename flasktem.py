from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import flash
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap 
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand 
import pymysql

app = Flask(__name__)

#配置session
app.config['SECRET_KEY'] = '123456'

#引入bootstrap
bootstrap = Bootstrap(app)

#数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/zblog'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)#实例化SQLAlchemy
#mysql库配置
pymysql.install_as_MySQLdb()
#配置数据库迁移
migrate = Migrate(app,db)

#引入script脚本
manager = Manager(app)
manager.add_command("db",MigrateCommand)#配置迁移命令

 
#类
class User(db.Model):
	__tablename__="users"
	id=db.Column(db.Integer,primary_key=True)
	username = db.Column(db.String(50),unique=True,index=True) #此列带索引
	password=db.Column(db.String(50))
	email = db.Column(db.String(100))
	birthday = db.Column(db.DateTime)
	role_id=db.Column(db.Integer,db.ForeignKey("roles.id"))#外键指向roles表中的id列

class Role(db.Model):#需继承模型
	__tablename__ = "roles"	#db中表明，如果不设置则会与类名相同
	id = db.Column(db.Integer,primary_key=True)#设置id为主键
	name = db.Column(db.String(50),unique=True)#表示name为字符串，不重复
	users = db.relationship("User",backref='role') #关联user模型，并在user中添加反向引用（backfef）

#路由
@app.route("/login",methods=["GET"])
def login():
	return render_template("/btlogin.html")

@app.route("/login",methods=["POST"])
def loginPost():
	username=request.form.get("username","")
	password=request.form.get("password","")
	user = User.query.filter_by(username=username,password=password).first()#数据库查询
	if user is not None:
		session["user"] = username
		return render_template("/index.html",name=username,site_name='myblog')
	else:
		flash("您输入的用户名或密码错误")
		return render_template("/btlogin.html")

@app.route("/register",methods=["GET"])
def register():
	return render_template("/register.html")

@app.route("/register",methods=["POST"])
def registerPost():
	user = User();
	user.username = request.form.get("username","")
	user.password = request.form.get("password","")
	user.email = request.form.get("email","")
	user.birthday= request.form.get("birthday","")
	user.role_id = 1
	if (len(user.username.strip())==0):
		flash("用户名不能为空")
		return render_template("/register.html")
	if (len(user.password.strip())==0):
		flash("密码不能为空")
		return render_template("/register.html")
	if (len(user.email.strip())==0):
		flash("邮箱不能为空")
		return render_template("/register.html")
	if (len(user.birthday.strip())==0):
		flash("生日不能为空")
		return render_template("/register.html")
	db.session.add(user);
	flash("您已注册成功")
	return render_template("/register.html")

if __name__ == '__main__':
	app.run(debug=True)
	#manager.run()