from flask import render_template, request, url_for, flash, redirect, jsonify, session
from flaskmovie import app, bcrypt, db, key
from flaskmovie.forms import RegistrationForm, LoginForm, AccountUpdateForm, CommentForm, RequestResetPasswordForm, ResetPasswordForm
from flaskmovie.models import Movie, User, Post, MovieList
from flask_login import login_user, current_user, logout_user, login_required
import requests
import requests_cache

requests_cache.install_cache(cache_name='movie_cache', backend='sqlite', expire_after=86400)


@app.route('/')
def index():
	if "movie" in session:
		return render_template('index.html', movies=session['movie'])
	r_dict = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={key}&language=en-US&page=1&region=US")
	r_dict = r_dict.json()
	movies  = r_dict['results']
	return render_template('index.html', movies=movies)

@app.route('/register', methods=['GET', 'POST'])
def register():
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		user.confirmation_email()
		flash('Account created, please check your email to verify your account', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
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
	return render_template('login.html', form=form)

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
	movie = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US&append_to_response=videos,credits").json()
	movie_credits = movie['credits']['cast']
	movie_credits = [x for x in movie_credits if x['profile_path'] is not None]
	movie_video = movie['videos']['results'][0]
	my_movie = Movie.query.filter_by(tmdb_id=movie_id).first()
	if not my_movie:
		new_movie = Movie(tmdb_id=movie_id, original_title=movie['original_title'],
						  backdrop_path=movie['backdrop_path'], poster_path=movie['poster_path'])
		db.session.add(new_movie)
		db.session.commit()
		return redirect(url_for('movie', movie_id=movie_id))
	form = CommentForm()
	if form.validate_on_submit():
		if current_user.is_authenticated:
			if current_user.confirmed:
				post = Post(message=form.comment.data, movie_id=my_movie.tmdb_id, user_id=current_user.id)
				db.session.add(post)
				db.session.commit()
				form.comment.data = ""
				flash('Comment Posted', 'success')
			else:
				flash('You must verify your email before commenting!', 'info')
		else:
			flash('Please sign in to post a comment!', 'info')
	return render_template('movie.html', movie=movie, movie_credits=movie_credits,
						   form=form, posts=my_movie.posts, movie_video=movie_video)

@app.route('/confirm/<token>', methods=['GET', 'POST'])
def confirm_email(token):
	user = User.confirm_token(token)
	if not user:
		flash('Invalid token', 'danger')
		return redirect(url_for('index'))
	user.confirmed = True
	db.session.commit()
	flash('Email verified!', 'success')
	return redirect(url_for('index'))

@app.route('/reset/password', methods=['GET', 'POST'])
def reset_password_token():
	form = RequestResetPasswordForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		user.password_reset_email()
		flash('A password reset link has been sent to your email!', 'info')
		return redirect(url_for('index'))
	return render_template('password_reset_request.html', form=form)

@app.route('/reset/password/<token>', methods=['GET', 'POST'])
def reset_password(token):
	user = User.confirm_token(token)
	if not user:
		flash('Invalid token', 'danger')
		return redirect(url_for('login'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash('Your password has been updated!', 'success')
		return redirect(url_for('login'))
	return render_template('password_reset.html', form=form)

@app.route('/update', methods=['GET', 'POST'])
def update():
	data = request.values.get('command')
	return html_gen(movie_api_call(data))

def html_gen(list):
	html = ""
	for result in list:
		image_src = f"https://image.tmdb.org/t/p/w500/{result['poster_path']}" if result['poster_path'] is not None else url_for('static', filename='background.jpg')
		html += f"""
	<div class="col-6 col-sm-4 col-md-3 col-xl-2 py-1">
		<div class="card h-100">
			<img src="{image_src}" class="card-img-top movie-header"
				 alt="image">
			<div class="card-body">
				<h5 class="card-title">{result['original_title']}</h5>
				<a href="{url_for('movie', movie_id=result['id'])}" class="stretched-link"></a>
			</div>
			<div class="card-footer">
				<small class="text-muted">{result['release_date']}</small>
			</div>
		</div>
	</div>
		"""
	html = f"""
	<div class="container-fluid">
	<div class="row mb-5">
	{html}
	</div>
	</div>
			"""
	return html

def movie_api_call(endpoint):
	movie = requests.get(f"https://api.themoviedb.org/3/movie/{endpoint}?api_key={key}&language=en-US&region=US").json()['results']
	#session['movie'] = movie
	return movie

@app.route('/search', methods=['GET', 'POST'])
def search():
	search = request.args.get('search')
	movies = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={key}&language=en-US&query={search}&page=1&region=US").json()['results']
	if not movies:
		flash('No results found, please check your search!', 'info')
	return render_template('search.html', movies=movies)

@app.route('/watchlist/', methods=['GET', 'POST'])
@login_required
def watchlist():
	ids = [movie.movie_id for movie in current_user.movies]
	watchlist = db.session.query(Movie).filter(Movie.tmdb_id.in_(ids)).all()
	return render_template('watchlist.html', watchlist=watchlist)

@app.route('/watchlist/add/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def watchlist_add(movie_id):
	check = MovieList.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
	if check:
		check.watch_list = True
		db.session.commit()
	else:
		movie_to_add = MovieList(user_id=current_user.id, movie_id=movie_id, watch_list=True, favourite_list=False)
		db.session.add(movie_to_add)
		db.session.commit()
	flash('Movie added to watchlist', 'success')
	return redirect(url_for('movie', movie_id=movie_id))


