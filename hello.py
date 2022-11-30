from flask import Flask, render_template, flash, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#FLASK INSTANCE
app = Flask(__name__)
app.config['SECRET_KEY'] = "my super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///members.db'
# Initialize database
db = SQLAlchemy(app)

#Create database model
class Members(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(200), nullable=False)
	date_created = db.Column(db.DateTime, default=datetime.utcnow)
#Create a function to return a string when we add something
def __repr__(self):
	return '<name %r>' % self.id

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

#members
@app.route('/members', methods=['POST', 'GET'])
def members():
	title = "Group members"

	if request.method == "POST":
		member_name = request.form['name']
		new_member = Members(name=member_name)

		#Push to database
		try:
			db.session.add(new_member)
			db.session.commit()
			return redirect('/members')
		except:
			return "There was an error adding new Member."
	else:
		members = Members.query.order_by(Members.date_created)
		return render_template("members.html", title=title, members=members)


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
		flash("Form Submitted Successfully!!")


	return render_template("name.html",
		name = name,
		form = form)