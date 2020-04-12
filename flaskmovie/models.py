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
	imdb_id = db.Column(db.String, unique=True)
	title = db.Column(db.String, nullable=False)
	overview = db.Column(db.String)
	date_released = db.Column(db.DateTime)
	poster_path = db.Column(db.String)
	runtime = db.Column(db.Integer)
	vote_count = db.Column(db.Integer)
	vote_avg = db.Column(db.DECIMAL)
	rec_1 = db.Column(db.String, nullable=False)
	rec_2 = db.Column(db.String, nullable=False)
	rec_3 = db.Column(db.String, nullable=False)
	rec_4 = db.Column(db.String, nullable=False)
	rec_5 = db.Column(db.String, nullable=False)
	rec_6 = db.Column(db.String, nullable=False)
	posts = db.relationship('Post', backref='movie', lazy=True)

	def __repr__(self):
		return f"{self.id}, {self.title}, {self.rec_1}, {self.rec_2} ..."

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)
	confirmed = db.Column(db.Boolean, nullable=False, default=False)
	posts = db.relationship('Post', backref='author', lazy=True)

	def generate_confirm_token(self, expiry=600):
		serial = Serializer(app.config['SECRET_KEY'], expiry)
		return serial.dumps({'user_id': self.id}).decode('utf-8')

	@staticmethod
	def confirm_token(token):
		serial = Serializer(app.config['SECRET_KEY'])
		user_id = serial.loads(token).get('user_id')
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
	movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.message[:100]}', '{self.date_time}', '{self.user_id}', '{self.movie_id}')"


movie_list = [m.title for m in Movie.query.all()]