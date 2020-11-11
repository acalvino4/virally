from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin

following = db.Table('following',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True),
  db.Column('followee_id', db.Integer, db.ForeignKey('user.id'), nullable=False, primary_key=True)
)

class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(16), index=True, unique=True)
  full_name = db.Column(db.String(32))
  password_hash = db.Column(db.String(128))
  joined_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)
  def __repr__(self):
    return self.username
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)
  bio = db.Column(db.String(256))
  posts = db.relationship(
    'Post',
    backref='author',
    lazy='dynamic'
  )
  followees = db.relationship(
    'User',
    secondary='following',
    primaryjoin=(id == following.c.follower_id),
    secondaryjoin=(id == following.c.followee_id),
    backref='follower',
    lazy='dynamic'
  )

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  author_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True, nullable=False)
  title = db.Column(db.String(32))
  content = db.Column(db.String(256), nullable=False)
  posted_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)
