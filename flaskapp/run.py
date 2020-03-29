from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')
db = SQLAlchemy(app)

class Movie(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	imdb_id = db.Column(db.String, unique=True)
	title = db.Column(db.String)
	rec_1 = db.Column(db.String)
	rec_2 = db.Column(db.String)
	rec_3 = db.Column(db.String)
	rec_4 = db.Column(db.String)
	rec_5 = db.Column(db.String)
	rec_6 = db.Column(db.String)

@app.route('/')
def hello():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)