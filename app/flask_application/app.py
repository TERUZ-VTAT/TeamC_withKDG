from flask import Flask,render_template, redirect, request
# from flask_sqlalchemy import SQLAlchemy
from .models.database import init_db, db
from .models.post import Post

app = Flask(__name__)

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
    'user': 'user',
    'password': 'pass',
    'host': 'db',
    'db_name': 'flask_database'
})
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = False
init_db(app)

# db = SQLAlchemy(app)

@app.route('/')
def HeadPage():
    return render_template("header.html")
@app.route('/profile')
def ProfilePage():
    return render_template("profile.html")
@app.route('/home')
def PostList():
    return render_template("postlist.html")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)