from flask import render_template, redirect, url_for
from app import app, db
from app.models import User
from app.forms import RegistrationForm, LoginForm

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    return redirect('/login')
  return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    return redirect(url_for('user', username=form.username.data))
  return render_template('login.html', form=form)

@app.route('/user/<username>')
def user(username):
  return render_template('user.html', username=username)
