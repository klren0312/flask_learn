from flask import Flask
from flask import render_template
from flask import session
from flask import flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_wtf import FlaskForm
from flask_migrate import Migrate, MigrateCommand
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import pymysql

app = Flask(__name__)

#配置session
app.config['SECRET_KEY'] = '123456'

#引入bootstrap
bootstrap = Bootstrap(app)

#数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/zflask'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) #实例化SQLAlchemy
#mysql库配置
pymysql.install_as_MySQLdb()
#配置数据库迁移
migrate = Migrate(app, db)

#引入脚本script
manager = Manager(app)
manager.add_command("db", MigrateCommand)
#配置迁移命令 python blog.py db init
# #python default.py db migrate -m "说明"

#数据类
#python blog.py shell
#from blog import db
#db.create_all()根据数据类创建数据库表
#db.drop_all()删除创建的数据库表

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))

#表单类
class LoginForm(FlaskForm):
    username = StringField("请输入用户名", validators=[DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    submit = SubmitField("登录")

class RegisterForm(FlaskForm):
    username = StringField("请输入用户名", validators=[DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    submit = SubmitField("注册")

#路由
@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data,
        password = form.password.data,
        user = User.query.filter_by(username=username, password=password).first()#数据库查询
        if user is not None:
            session["user"] = username
            return render_template("/index.html", name=username, site_name="zzes")
        else:
            flash("您输入的用户名或密码错误")
            return render_template("/login.html", form=form)
    return render_template("/login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data
        )
        if(User.query.filter_by(username=user.username).first()):
            flash("当前用户名已经注册！")
            return render_template("/register.html", form=form)
        else:
            flash("注册成功!")
            db.session.merge(user)
            return render_template("/register.html", form=form)
    return render_template("/register.html", form=form)


if __name__ == '__main__':
    app.run(debug=True)
    #manager.run()#使用脚本时打开注释

