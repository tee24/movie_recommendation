from flaskapp.app import db, app

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	imdb_id = db.Column(db.String, unique=True)
	title = db.Column(db.String, nullable=False)
	rec_1 = db.Column(db.String, nullable=False)
	rec_2 = db.Column(db.String, nullable=False)
	rec_3 = db.Column(db.String, nullable=False)
	rec_4 = db.Column(db.String, nullable=False)
	rec_5 = db.Column(db.String, nullable=False)
	rec_6 = db.Column(db.String, nullable=False)

	def __repr__(self):
		return f"{self.id}, {self.title}, {self.rec_1}, {self.rec_2} ..."

movie_list = [m.title for m in Movie.query.all()]