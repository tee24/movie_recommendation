from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskmovie.models import User


class RegistrationForm(FlaskForm):
	username = StringField('Username',
						   validators=[DataRequired(), Length(4,16)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password',
									 validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	def validate_username(self, username):
		if User.query.filter_by(username=username.data).first():
			raise ValidationError("Username is already taken.")

	def validate_email(self, email):
		if User.query.filter_by(email=email.data).first():
			raise ValidationError("Email is already taken.")

class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign Up')