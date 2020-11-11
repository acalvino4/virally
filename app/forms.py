from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, EqualTo

class RegistrationForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  full_name = StringField('Full Name', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  password2 = PasswordField('Enter password again', validators=[DataRequired(), EqualTo('password')])
  submit = SubmitField('Register')

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[DataRequired()])
  password = PasswordField('Password', validators=[DataRequired()])
  remember = BooleanField('Remember Me')
  submit = SubmitField('Login')

class PostForm(FlaskForm):
  title = StringField('Title', validators=[DataRequired()])
  content = TextAreaField('Content', validators=[DataRequired()])
  submit = SubmitField('Go Viral!')
