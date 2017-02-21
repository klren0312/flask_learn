#Flask 学习
>使用的框架:flask,render_template,flask-bootstrap,flask-sqlalchemy,flask-wtf,flask-migrate,wtforms,pymysql

##数据库配置代码
```
#数据库配置
app.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:root@localhost/zflask'
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app) #实例化SQLAlchemy
#mysql库配置
pymysql.install_as_MySQLdb()
#配置数据库迁移
migrate = Migrate(app, db)

```

##数据类
```
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password = db.Column(db.String(50))
```

##表单类
```
class LoginForm(FlaskForm):
    username = StringField("请输入用户名", validators=[DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    submit = SubmitField("登录")

class RegisterForm(FlaskForm):
    username = StringField("请输入用户名", validators=[DataRequired()])
    password = PasswordField("请输入密码", validators=[DataRequired()])
    submit = SubmitField("注册")
```

##登录路由
```
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
```

##注册路由
```
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
```
===================更新日志=========================
###2017.2.21 解决注册问题，在之前加了判断
###2017.2.20 完成注册逻辑，有错误，当传入重复用户名时，会报错，变成白页
###2017.2.19 完成登录逻辑
