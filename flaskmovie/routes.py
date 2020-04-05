from flask import render_template, request, url_for, flash, redirect
from flaskmovie import app, bcrypt
from flaskmovie.forms import RegistrationForm, LoginForm
from flaskmovie.models import Movie, User, movie_list

@app.route('/')
def index():
	return render_template('index.html', movie_list=movie_list)

@app.route('/recommendations/', methods=['GET', 'POST'])
def movie():
	if request.method == "POST":
		user_movie = request.form["user_movie"]
		movie = Movie.query.filter_by(title=user_movie).first()
		if movie:
			return render_template('recommend.html', movie=movie,
								   movie_list=movie_list, table=Movie)
		else:
			flash("No movie found please try another!", 'danger')
			return render_template('index.html', movie_list=movie_list)
	else:
		return render_template('index.html', movie_list=movie_list)

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

