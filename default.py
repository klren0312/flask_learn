from flask import Flask,request,render_template
from flask.ext.bootstrap import Bootstrap 

app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
	return render_template("index.html",site_name='myblog')

if __name__ == '__main__':
	app.run(debug=True)