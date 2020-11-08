from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(16), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  joined_at = db.Column(db.DateTime(), default = datetime.utcnow, index = True)
  def __repr__(self):
    return self.username
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  def check_password(self):
    return check_password_hash(self.password_hash, password)
