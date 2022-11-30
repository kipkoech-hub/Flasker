from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
#FLASK INSTANCE
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"

#Create  aform class
class NamerForm(FlaskForm):
	name = StringField("Whats your name", validators=[DataRequired()])
	submit = SubmitField("Submit")


#ROUTE DECORATOR
@app.route('/')

def index():
	return render_template('index.html')



@app.route('/user/<name>')

def user(name):
	return render_template('user.html', user_name=name)


#invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404


#Internal Server Error
@app.errorhandler(500)
def page_not_found(e):
	return render_template('500.html'), 500


#Create Name Page
@app.route('/name', methods=['GET', 'POST'])
def name():
	name = None
	form = NamerForm()
	#validate form
	if form.validate_on_submit():
		name = form.name.data
		form.name.data = ''
	return render_template("name.html",
		name = name,
		form = form)