This is a twitter-like social media app that allows users to make brief postings and to follow other users to view their postings.

[View web app](https://virally-2.herokuapp.com/login)

It was my first time implementing a full-scale authentication system, as well as my first time utilizing the SQLAlchemy ORM.

On a small note, I also used a native css variable for the first time here. (I have used sass variables, as my preference is generally to work with bootstrap.)

Some other interesting features that I worked though are
* implementing a many-to-many self-referential database relationship in SQLAlchemy
* dealing with all data exchange through form submission rather than ajax
* rerouting after login or a post request based on a 'next' url query parameter

## Running locally

1. Make sure pipenv is [installed](https://pipenv.pypa.io/en/latest/#install-pipenv-today)

2. Run this script
```bash
git clone https://github.com/acalvino4/virally.git
cd virally
pipenv install
```

3. Create `.env` file in project root with this structure
```
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI='sqlite:///my_app.db'
SECRET_KEY='MY_SECRET_KEY'
```

4. Run `pipenv run dev`
