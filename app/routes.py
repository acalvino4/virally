from flask import render_template, redirect, url_for, request, flash, abort
from app import app, db, login_manager
from app.models import User, Post, following
from app.forms import RegistrationForm, LoginForm, PostForm
from flask_login import login_user, logout_user, login_required, current_user
from is_safe_url import is_safe_url

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(user_id)

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
  return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, full_name=form.full_name.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return redirect('/login')
  return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=form.username.data).first()
    if user and user.check_password(form.password.data):
      login_user(user, remember=form.remember.data)
      flash('Login Successful')
      next = request.args.get('next')
      if next and not is_safe_url(next, {app.config.get('SERVER_NAME')}):
        return abort(400)
      return redirect(next or url_for('dashboard', username=form.username.data))
    else:
      flash('No Such User or Bad Password')
  if current_user.is_authenticated:
    return redirect(url_for('dashboard', username=current_user.username))
  return render_template('login.html', form=form)

@app.route('/logout')
def logout():
  logout_user()
  return redirect('/')


@app.route('/dashboard/')
@app.route('/dashboard/<username>')
@login_required
def dashboard(username=''):
  if username=='':
    username = current_user.username
  elif username != current_user.username:
    abort(401)
  form = PostForm()
  followee_ids = [followee.id for followee in current_user.followees]
  print(followee_ids)
  posts = Post.query.filter(Post.author_id.in_(followee_ids)).order_by(Post.posted_at.desc()).limit(10).all()
  print(posts)
  return render_template('dashboard.html', form=form, posts=posts)

@app.route('/profile/')
@app.route('/profile/<username>')
@login_required
def profile(username=''):
  if username=='':
    username= current_user.username
  user = User.query.filter_by(username=username).first_or_404()
  posts = Post.query.filter_by(author_id=user.id).order_by(Post.posted_at.desc()).limit(10).all()
  form = PostForm()
  followee_ids = [followee.id for followee in current_user.followees]
  return render_template('profile.html', user=user, posts=posts, form=form, followee_ids=followee_ids)

@app.route('/people')
@login_required
def people():
  users = User.query.all()
  followee_ids = [followee.id for followee in current_user.followees]
  return render_template('people.html', users=users, followee_ids=followee_ids)

@app.route('/post', methods=['POST'])
@login_required
def postpost():
  form = PostForm(request.form)
  if form.validate_on_submit():
    post = Post(author_id=current_user.id, title=form.title.data, content=form.content.data)
    db.session.add(post)
    db.session.commit()
    flash('Post Created!')
  else:
    flash('No valid post data supplied.')
  next = request.args.get('next')
  if next and not is_safe_url(next, {app.config.get('SERVER_NAME')}):
    return abort(400)
  return redirect(next or url_for('dashboard', username=current_user.username))

@app.route('/post/<id>', methods=['POST'])
@login_required
def postdelete(id):
  # I know using post instead of delete here is semantically incorrect - needs a workaround becuase forms only submit post and get requests
  post = Post.query.filter_by(id=id).first_or_404()
  if post.author_id != current_user.id:
    abort(401)
  db.session.delete(post)
  db.session.commit()
  next = request.args.get('next')
  if next and not is_safe_url(next, {app.config.get('SERVER_NAME')}):
    return abort(400)
  return redirect(next or url_for('dashboard', username=form.username.data))

@app.route('/following/<user_id>', methods=['POST', 'GET'])
@login_required
def following(user_id):
  user = User.query.get(user_id)
  if user:
    if request.method == 'POST':
      if user not in current_user.followees:
        current_user.followees.append(user)
        db.session.commit()
        flash(f'You are now following {user.full_name}')
      else:
        flash(f'You were already following {user.full_name}')
    # I know this method is semantically incorrect - needs a workaround becuase forms only submit post and get requests
    if request.method == 'GET':
      if user in current_user.followees:
        current_user.followees.remove(user)
        db.session.commit()
        flash(f'You are no longer following {user.full_name}')
      else:
        flash(f'You were not following {user.full_name}')
  else:
    flash('No such user exists')
  next = request.args.get('next')
  print(next)
  if next and not is_safe_url(next, {app.config.get('SERVER_NAME')}):
    return abort(400)
  return redirect(next or url_for('people'))
