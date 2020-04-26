from flaskmovie import db, login_manager, app, mail
from flask import url_for
from flask_mail import Message
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
	user = User.query.get(int(user_id))
	return user

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tmdb_id = db.Column(db.String, nullable=False, unique=True)
	backdrop_path = db.Column(db.Text)
	poster_path = db.Column(db.Text)
	original_title = db.Column(db.Text)
	posts = db.relationship('Post', backref='movie', lazy=True)

	def __repr__(self):
		return f"{self.id}, {self.tmdb_id}"

class MovieList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.tmdb_id'), nullable=False)
	watch_list = db.Column(db.Boolean, nullable=False)

	def __repr__(self):
		return f"Post('{self.id}', '{self.user_id}', '{self.movie_id}', '{self.watch_list}')"

class Tv(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	tmdb_show_id = db.Column(db.String, nullable=False, unique=True)
	poster_path = db.Column(db.Text)
	original_name = db.Column(db.Text)

class TvList(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	show_id = db.Column(db.Integer, db.ForeignKey('tv.tmdb_show_id'), nullable=False)
	season_id = db.Column(db.Integer)
	episode_id = db.Column(db.Integer)
	watch_list = db.Column(db.Boolean, nullable=False)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)
	confirmed = db.Column(db.Boolean, nullable=False, default=False)
	posts = db.relationship('Post', backref='author', lazy=True)
	movies = db.relationship('MovieList', backref='movies', lazy=True)
	tv = db.relationship('TvList', backref='tv', lazy=True)

	def generate_confirm_token(self, expiry=600):
		serial = Serializer(app.config['SECRET_KEY'], expiry)
		return serial.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def confirm_token(token):
		serial = Serializer(app.config['SECRET_KEY'])
		try:
			user_id = serial.loads(token).get('user_id')
		except:
			return None
		return User.query.get(user_id)

	def confirmation_email(self):
		token = self.generate_confirm_token()
		message = Message('Email confirmation link', sender='noreply@moviesite.com',
				   recipients=[self.email])
		message.body = f""" Confirm your email address by visiting the following link:

{url_for('confirm_email', token=token, _external=True)}

Thank you!
		"""
		mail.send(message)

	def password_reset_email(self):
		token = self.generate_confirm_token()
		message = Message('Password reset link', sender='noreply@moviesite.com',
						  recipients=[self.email])
		message.body = f""" To reset your password please visit the following link:

{url_for('reset_password', token=token, _external=True)}

Thank you!
		"""
		mail.send(message)


	def __repr__(self):
		return f"User('{self.username}', '{self.email}')"

class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	date_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	message = db.Column(db.Text, nullable=False)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.tmdb_id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.message[:100]}', '{self.date_time}', '{self.user_id}', '{self.movie_id}')"

