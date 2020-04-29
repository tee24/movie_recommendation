from flask import render_template, request, url_for, flash, redirect, session, jsonify
from flaskmovie import app, bcrypt, db, key
from flaskmovie.forms import RegistrationForm, LoginForm, AccountUpdateForm, CommentForm, RequestResetPasswordForm, ResetPasswordForm
from flaskmovie.models import Movie, User, Post, MovieList, Tv, TvList
from flask_login import login_user, current_user, logout_user, login_required
import requests
import requests_cache
import json
from random import randint

requests_cache.install_cache(cache_name='movie_cache', backend='sqlite', expire_after=86400)

def api_call(endpoint, page=1):
	movie = requests.get(f"https://api.themoviedb.org/3/{endpoint}?api_key={key}&language=en-US&page={page}&region=US").json()['results']
	return movie

@app.route('/')
def index():
	movies = api_call('movie/popular')
	return render_template('index.html', movies=movies)

@app.route('/load', methods=['GET', 'POST'])
def load():
	page = request.values.get('page')
	endpoint = request.values.get('endpoint')
	html = html_gen(api_call(endpoint=endpoint, page=page), tv='tv' in endpoint)
	session['page'] = page
	return html

@app.route('/register', methods=['GET', 'POST'])
def register():
	register_image = randint(1, 16)
	form = RegistrationForm()
	if form.validate_on_submit():
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		user.confirmation_email()
		flash('Account created, please check your email to verify your account', 'success')
		return redirect(url_for('login'))
	return render_template('register.html', form=form, register_image=register_image)

@app.route('/login', methods=['GET', 'POST'])
def login():
	hide_navbar = False
	login_image = randint(1,16)
	form = LoginForm()
	if form.validate_on_submit():
		print(form.remember.data)
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
	return render_template('login.html', form=form, hide_navbar=hide_navbar, login_image=login_image)

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
	movie = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={key}&language=en-US&append_to_response=videos,credits,reviews").json()
	movie_credits = movie['credits']['cast']
	movie_credits = [x for x in movie_credits if x['profile_path'] is not None]
	movie_reviews = movie['reviews']['results']
	if current_user.is_authenticated:
		user_movies = MovieList.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
	else:
		user_movies = None
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
						   form=form, posts=my_movie.posts, movie_reviews=movie_reviews,
						   user_movies=user_movies)

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
	endpoint = request.values.get('command')
	tv = request.values.get('tv')
	return html_gen(api_call(endpoint=endpoint), tv=tv)

def html_gen(list, tv=False):
	title = 'original_name' if tv else 'original_title'
	html = ""
	for result in list:
		image_src = f"https://image.tmdb.org/t/p/w500/{result['poster_path']}" if result['poster_path'] is not None else url_for('static', filename='background.jpg')
		html += f"""
	<div class="col-6 col-sm-4 col-md-3 col-xl-2 py-1">
		<div class="card h-100">
			<img src="{image_src}" class="card-img-top movie-header"
				 alt="image">
			<div class="card-body">
				<h5 class="card-title">{result[title]}</h5>
				<a href="{url_for('television', television_id=result['id']) if tv else url_for('movie', movie_id=result['id'])}" class="stretched-link"></a>
			</div>
		</div>
	</div>
		"""
	return html

@app.route('/search', methods=['GET', 'POST'])
def search():
	search_term = request.args.get('search')
	search_results = requests.get(f"https://api.themoviedb.org/3/search/multi?api_key={key}&language=en-US&query={search_term}&page=1&region=US").json()['results']
	for item in search_results:
		if item['media_type'] == 'person':
			search_results.remove(item)
	if not search_results:
		flash('No results found, please check your search!', 'info')
	return render_template('search.html', search_results=search_results)

@app.route('/watchlist/movies', methods=['GET', 'POST'])
@login_required
def watchlist_movies():
	ids = [movie.movie_id for movie in current_user.movies if movie.watch_list == True]
	watchlist = db.session.query(Movie).filter(Movie.tmdb_id.in_(ids)).all()
	tv = False
	return render_template('watchlist.html', watchlist=watchlist, tv=tv)

@app.route('/watchlist/tv', methods=['GET', 'POST'])
@login_required
def watchlist_tv():
	ids = [show.show_id for show in current_user.tv if show.watch_list == True]
	watchlist = db.session.query(Tv).filter(Tv.tmdb_show_id.in_(ids)).all()
	tv = True
	return render_template('watchlist.html', watchlist=watchlist, tv=tv)

@app.route('/watchlist/add/<int:id>', methods=['GET', 'POST'])
@login_required
def watchlist_add(id):
	tv = request.args.get('tv')
	if tv:
		check = TvList.query.filter_by(user_id=current_user.id, show_id=id).first()
		if check:
			check.watch_list = True
			db.session.commit()
		else:
			show_to_add = TvList(user_id=current_user.id, show_id=id, watch_list=True)
			db.session.add(show_to_add)
			db.session.commit()
		flash('TV show added to watchlist', 'success')
		return redirect(url_for('television', television_id=id))
	else:
		check = MovieList.query.filter_by(user_id=current_user.id, movie_id=id).first()
		if check:
			check.watch_list = True
			db.session.commit()
		else:
			movie_to_add = MovieList(user_id=current_user.id, movie_id=id, watch_list=True)
			db.session.add(movie_to_add)
			db.session.commit()
		flash('Movie added to watchlist', 'success')
		return redirect(url_for('movie', movie_id=id))

@app.route('/watchlist/remove/<int:id>', methods=['GET', 'POST'])
@login_required
def watchlist_remove(id):
	tv = request.args.get('tv')
	if tv:
		check = TvList.query.filter_by(user_id=current_user.id, show_id=id, watch_list=True).first()
		if check:
			check.watch_list = False
			db.session.commit()
			flash('Tv show removed from watchlist!', 'success')
		else:
			flash('Tv show not in watchlist', 'danger')
		return redirect(url_for('television', television_id=id))
	else:
		check = MovieList.query.filter_by(user_id=current_user.id, movie_id=id, watch_list=True).first()
		if check:
			check.watch_list = False
			db.session.commit()
			flash('Movie removed from watchlist!', 'success')
		else:
			flash('Movie not in watchlist', 'danger')
		return redirect(url_for('movie', movie_id=id))

@app.route('/television/<int:television_id>')
def television(television_id):
	show = requests.get(f"https://api.themoviedb.org/3/tv/{television_id}?api_key={key}&language=en-US&append_to_response=credits").json()
	season = requests.get(f"https://api.themoviedb.org/3/tv/{television_id}/season/1?api_key={key}&language=en-US&append_to_response=credits").json()
	show_credits = show['credits']['cast']
	show_credits = [x for x in show_credits if x['profile_path'] is not None]

	if current_user.is_authenticated:
		user_tv = TvList.query.filter_by(user_id=current_user.id, show_id=television_id).first()
	else:
		user_tv = None

	tv = Tv.query.filter_by(tmdb_show_id=television_id).first()

	if not tv:
		show = Tv(tmdb_show_id=television_id, poster_path=show['poster_path'], original_name=show['original_name'])
		db.session.add(show)
		db.session.commit()
		return redirect(url_for('television', television_id=television_id))

	return render_template('television.html', show=show, show_credits=show_credits, season=season, user_tv=user_tv)

@app.route('/graph')
def graph():
	return render_template('graph.html')

@app.route('/update_tv', methods=['GET', 'POST'])
def update_tv():
	season_number = request.values.get('season_number')[2:]
	show_id = request.values.get('show_id')
	season = requests.get(f"https://api.themoviedb.org/3/tv/{show_id}/season/{season_number}?api_key={key}&language=en-US&append_to_response=credits").json()

	ratings = []
	names = []
	for episode in season['episodes']:
		ratings.append(episode['vote_average'])
		names.append(episode['name'])

	graph = {}
	graph['ratings'] = ratings
	graph['names'] = names

	html = ""
	for episode in season['episodes']:
		html += f"""
<div class="card m-1 episode-card" style="width: 18rem;">
<img class="card-img-top episode" src="https://image.tmdb.org/t/p/w500/{ episode['still_path'] }" alt="Card image cap">
<div class="card-body">
<span class="font-weight-bold">{ episode['name'] }</span>
<span class="font-weight-bold">S{ episode['season_number'] }E{ episode['episode_number'] }</span><br>
<span class="text-muted">{ episode['air_date'] }</span>
</div>
</div>
		"""

	payload = {}
	payload['html'] = html
	payload['chart_info'] = graph
	payload = jsonify(payload)

	return payload

@app.route('/discover', methods=['GET', 'POST'])
def discover():
	if request.method == "POST":
		parameters = {}
		parameters['primary_release_date.gte'] = "" if not request.form['min_year'] else f"{request.form['min_year']}-01-01"
		parameters['primary_release_date.lte'] = "" if not request.form['max_year'] else f"{request.form['max_year']}-12-31"
		parameters['with_runtime.gte'] = request.form['min_length']
		parameters['with_runtime.lte'] = request.form['max_length']
		parameters['with_genres'] = ','.join(request.form.getlist('genres'))
		parameters = {k: v for k,v in parameters.items() if parameters[k]}

		query = ""
		for k,v in parameters.items():
			query += f"{k}={v}&"
		query = query[:-1]

		discovered_movies = requests.get(f"https://api.themoviedb.org/3/discover/movie?api_key={key}&language=en-US&sort_by=popularity.desc&include_adult=false&include_video=false&page=1{query}").json()['results']

		return render_template('recommendations.html', discovered_movies=discovered_movies)

	genre_list = requests.get(f"""https://api.themoviedb.org/3/genre/movie/list?api_key={key}&language=en-US""").json()['genres']
	return render_template('discover.html', genre_list=genre_list)
