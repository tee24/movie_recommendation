from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
	username = StringField('Username',
						   validators=[DataRequired(), Length(4,16)])
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
	confirm_password = PasswordField('Confirm Password',
									 validators=[DataRequired()])
	submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
	email = StringField('Email',
						validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired(), EqualTo('confirm_password')])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Sign Up')