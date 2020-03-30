from flask import Flask, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

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

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def movie():
	if request.method == "POST":
		user_movie = request.form["user_movie"]
		movie = Movie.query.filter_by(title=user_movie).first()
		return render_template('index.html', movie=movie)
	else:
		return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)