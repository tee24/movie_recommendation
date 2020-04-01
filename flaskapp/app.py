from flask import Flask, render_template, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)
from flaskapp import models

@app.route('/')
def index():
	return render_template('index.html', movie_list=models.movie_list)

@app.route('/recommendations/', methods=['GET', 'POST'])
def movie():
	if request.method == "POST":
		user_movie = request.form["user_movie"]
		movie = models.Movie.query.filter_by(title=user_movie).first()
		if movie:
			return render_template('recommend.html', movie=movie,
								   movie_list=models.movie_list)
		else:
			flash("No movie found please try another!", 'danger')
			return render_template('index.html', movie_list=models.movie_list)
	else:
		return render_template('index.html', movie_list=models.movie_list)

if __name__ == '__main__':
	app.run(debug=True)