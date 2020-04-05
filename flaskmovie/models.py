from flaskmovie import db

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

	def __repr__(self):
		return f"{self.id}, {self.title}, {self.rec_1}, {self.rec_2} ..."

class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(16), unique=True, nullable=False)
	email = db.Column(db.String(100), unique=True, nullable=False)
	password = db.Column(db.String(30), nullable=False)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


movie_list = [m.title for m in Movie.query.all()]