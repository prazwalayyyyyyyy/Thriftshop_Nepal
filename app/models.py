import email
from app import login #for session
from email.policy import default
from enum import unique
from datetime import datetime
from sqlite3 import Timestamp
from app import db
from werkzeug.security import generate_password_hash, check_password_hash #package to implement password hashing
from flask_login import UserMixin #includes generic implementations appropriate for most user model class

class User(UserMixin, db.Model):#constructon of db model for user login 
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # posts = db.relationship('Post', backref='author', lazy='dynamic')
    user_type=db.Column(db.String(58), default='buyer')
    goods = db.relationship('Goods', backref='creater', lazy='dynamic')
        
    def __repr__(self):
        return '<User {}>'.format(self.username)    
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class Post(db.Model):#construction of db model for the posts
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class Goods(db.Model):
    # photo = db.Column()
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(140))
    price = db.Column(db.Integer)
    name = db.Column(db.String(50))
    descripton = db.Column(db.String(500))
    seller = db.Column(db.Integer, db.ForeignKey('user.id'))

#flasklogin keeps track of logged user by storing identifier unique in flask's user session. each time logged user nagicates page, flasklogin retrieve ID of user from session and load in memory
#FLASK-login dont know about the db. so need app's help in loading user.so app will configure user loader function that can be called to load user given ID
@login.user_loader #registering userloader with this decorator
def load_user(id): #id that flasklogin pass to function as argument will be string
    return User.query.get(int(id))