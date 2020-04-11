from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskmovie.models import User
from flask_login import current_user


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

class AccountUpdateForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	current_password = PasswordField('Current Password', validators=[DataRequired()])
	password = PasswordField('New Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm New Password',
									 validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Update Account')

	def validate_email(self, email):
		if email.data != current_user.email:
			if User.query.filter_by(email=email.data).first():
				raise ValidationError("Email is already taken.")

class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign Up')

class CommentForm(FlaskForm):
	comment = StringField('Comment', validators=[DataRequired(), Length(10,5000)])
	submit = SubmitField('Post Comment')