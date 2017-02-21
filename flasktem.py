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


#表单类
class LoginForm(Form):
	username = StringField("请输入用户名", validators=[DataRequired()])
	password = PasswordField("请输入密码", validators=[DataRequired()])
	submit = SubmitField("登录")
class RegisterForm(Form):
    username = StringField("请输入用户名", validators=[DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    submit = SubmitField("注册")


#路由
@app.route("/login",methods=["GET","POST"])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		username = form.username.data
		password = form.password.data
		user = User.query.filter_by(username=username,password=password).first()
		if user is not None:
			session["user"] = username
			return render_template("/index.html",name=username,site_name='myblog')
		else:
			flash("您输入的用户名或密码错误")
			return render_template("/btlogin.html",form=form)
	return render_template("/btlogin.html",form=form)

@app.route("/register",methods=["GET","POST"])
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        user=User(
        username=form.username.data,
        password=form.password.data,
 	 	)         
        db.session.add(user)

    return  render_template("/register.html",form=form)
    

if __name__ == '__main__':
	app.run(debug=True)
	#manager.run()