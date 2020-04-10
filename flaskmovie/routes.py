from flask import render_template, request, url_for, flash, redirect
from flaskmovie import app, bcrypt, db
from flaskmovie.forms import RegistrationForm, LoginForm, AccountUpdateForm, CommentForm
from flaskmovie.models import Movie, User, Post, movie_list
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/')
def index():
	return render_template('index.html', movie_list=movie_list)

@app.route('/recommendations/', methods=['GET', 'POST'])
def recommend():
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
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash('Account created!', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form, recommend=recommend)

@app.route('/login', methods=['GET', 'POST'])
def login():
	recommend = False
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			login_user(user, remember=form.remember.data)
			flash('You have successfully logged in', 'success')
			next = request.args.get('next')
			if next:
				return redirect(next)
			else:
				return redirect(url_for('index'))
		else:
			flash('Login Failed. Check Credentials', 'danger')
	return render_template('login.html', form=form, recommend=recommend)

@app.route('/logout')
def logout():
	logout_user()
	flash('You have logged out', 'success')
	return redirect(url_for('index'))

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
	form = AccountUpdateForm()
	if form.validate_on_submit():
		if bcrypt.check_password_hash(current_user.password, form.current_password.data):
			current_user.email = form.email.data
			current_user.password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
			db.session.commit()
			flash("Account has been updated!", "success")
			return redirect(url_for('index'))
		else:
			flash("Please check your current password is correct!", 'danger')

	elif request.method == "GET":
		form.email.data = current_user.email
	return render_template('account.html', form=form)

@app.route('/movie/<int:movie_id>', methods=['GET', 'POST'])
def movie(movie_id):
	form = CommentForm()
	movie = Movie.query.filter_by(id=movie_id).first()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			post = Post(message=form.comment.data, movie_id=movie.id, user_id=current_user.id)
			db.session.add(post)
			db.session.commit()
			flash('Comment Posted', 'success')
		else:
			flash('Please sign in to post a comment!', 'info')
	return render_template('movie.html', movie=movie, Movie=Movie, form=form, posts=reversed(movie.posts))


