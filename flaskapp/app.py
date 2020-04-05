from flask import Flask, render_template, url_for, request, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from flaskapp.forms import RegistrationForm, LoginForm
from flask_bcrypt import Bcrypt
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
from flaskapp import models

@app.route('/')
def index():
	return render_template('index.html', movie_list=models.movie_list)

@app.route('/recommendations/', methods=['GET', 'POST'])
def movie():
	if request.method == "POST":
		user_movie = request.form["user_movie"]
		movie = models.Movie.query.filter_by(title=user_movie).first()
		if movie:
			return render_template('recommend.html', movie=movie,
								   movie_list=models.movie_list, table=models.Movie)
		else:
			flash("No movie found please try another!", 'danger')
			return render_template('index.html', movie_list=models.movie_list)
	else:
		return render_template('index.html', movie_list=models.movie_list)

@app.route('/register', methods=['GET', 'POST'])
def register():
	recommend = False
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		flash('Account created!', 'success')
		return redirect(url_for('index'))
	return render_template('register.html', form=form, recommend=recommend)

@app.route('/login', methods=['GET', 'POST'])
def login():
	recommend = False
	form = LoginForm()
	if form.validate_on_submit():
		if form.email.data == "test@root.com" and form.password.data == "pass":
			flash('You have successfully logged in', 'success')
			return redirect(url_for('index'))
		else:
			flash('Login Failed', 'danger')
	return render_template('login.html', form=form, recommend=recommend)



if __name__ == '__main__':
	app.run(debug=True)