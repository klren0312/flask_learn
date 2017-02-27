#Flask 学习
>使用的框架:`flask`,`render_template`,`flask-bootstrap`,`flask-sqlalchemy`,`flask-wtf`,`flask-migrate`,`wtforms`,`pymysql`,`flask-login`,`url_for`

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

##flask_login相关配置
```
#登录状态管理配置
login_manager = LoginManager()
login_manager.session_protection = "strong" #可设置为None，basic，strong提供不同的安全等级
login_manager.login_view = "login" #设置登录页
login_manager.init_app(app)
#flask-login要求程序实现一个回调函数，使用指定的标识符加在用户上
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
```

##数据类
```
class User(UserMixin,db.Model):
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

##首页路由
```
@app.route('/index',methods=["GET"])
def index():
    return render_template("/index.html")

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
            login_user(user, form.remember_me.data)#第二项为记住我选项，若选上则为true，提供cookie存储状态
            return redirect(url_for("index"))
        else:
            flash("您输入的用户名或密码错误")
            return render_template("/login.html", form=form)
    return render_template("/login.html", form=form)
```

##登出路由
```
@app.route("/logout", methods=["GET", "POST"])
@login_required
#login_required 标识指的是只有登录用户才可以访问这个路由
def logout():
    logout_user()
    return redirect(url_for("index"))
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

##导航栏逻辑
```
        <ul class="nav navbar-nav navbar-right">
            {% if current_user.is_authenticated %}
                <li><p class="navbar-text"><a href="#" class="navbar-link">你好 {{ current_user.username }}</a></p></li>
                <li><a href="{{ url_for('logout') }}">登出</a></li>
            {% else %}
                <li><a href="{{ url_for('login') }}">登录</a></li>
            {% endif %}
        </ul>
```
===================更新日志=========================
###2017.2.27 登录注册基本完成
###2017.2.24 使用Flask-Login插件
###2017.2.21 解决注册问题，在之前加了判断
###2017.2.20 完成注册逻辑，有错误，当传入重复用户名时，会报错，变成白页
###2017.2.19 完成登录逻辑
