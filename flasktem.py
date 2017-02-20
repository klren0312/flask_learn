from flask import Flask
from flask import request
from flask import render_template
from flask import session
from flask import flash
from flask_sqlalchemy import SQLAlchemy 
from flask_bootstrap import Bootstrap 
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from flask_wtf import Form 
from wtforms import StringField,PasswordField,SubmitField,DateField
from wtforms.validators import DataRequired,EqualTo,Length,Email 
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

 
#数据类
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

#表单类
class RegisterForm(Form):
    username = StringField("请输入用户名", validators=[DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    birthday = DateField("出生日期")
    email = StringField("邮箱地址", validators=[Email()])
    submit = SubmitField("提交")

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
    form=RegisterForm()
    if form.validate_on_submit():
        user=User()
        user.username=form.username.data
        user.password=form.password.data
        user.birthday=form.birthday.data
        user.email=form.email.data
        user.role_id=1           
        db.session.add(user)
    return  render_template("/register.html",form=form)

if __name__ == '__main__':
	app.run(debug=True)
	#manager.run()