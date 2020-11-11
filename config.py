from os import environ
env = environ.get

SQLALCHEMY_DATABASE_URI = env('DATABASE_URL') or env('SQLALCHEMY_DATABASE_URI')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY=env('SECRET_KEY')
if not SECRET_KEY:
  raise ValueError("No SECRET_KEY set for Flask application")
SERVER_NAME = env('SERVER_NAME') or '127.0.0.1:5000'
