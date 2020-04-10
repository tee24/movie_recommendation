from flaskmovie import db, login_manager
from flask_login import UserMixin
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
	posts = db.relationship('Post', backref='author', lazy=True)

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