from itsdangerous.url_safe import URLSafeTimedSerializer as Serializer
from openur import db, login_manager
from flask import current_app as app
from datetime import datetime
from flask_login import UserMixin

# This is the user loader function for the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique = True, nullable = False) # 20 characters max (same with flask forms), unique, and cannot be null
    email = db.Column(db.String(120), unique = True, nullable = False)
    image_file = db.Column(db.String(20), nullable = False, default = 'default.jpg') # 20 characters max, cannot be null, and default image is default.jpg
    password = db.Column(db.String(60), nullable = False) # 60 characters max, cannot be null
    posts = db.relationship('Post', backref='author', lazy=True) # one to many relationship with Post model

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"
    

    '''def get_reset_token(self, expires_sec=1800):
        # Create a token with the user id and expiration time
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')'''
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(secret_key=app.config['SECRET_KEY'], salt='Becky')
        return s.dumps({'user_id': self.id})

    
    @staticmethod
    def verify_reset_token(token):
        # Create a token with the user id and expiration time
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable = False) # 100 characters max, cannot be null
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow) # cannot be null, and default is current time
    content = db.Column(db.Text, nullable = False) # cannot be null
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False) # foreign key to user table, cannot be null

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"