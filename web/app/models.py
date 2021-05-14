import jwt
from time import time
from app import db, login
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from flask_login import LoginManager # new code entry
from werkzeug.security import generate_password_hash, check_password_hash

# timestamp to be inherited by other class models
class TimestampMixin(object):
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    added_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login.user_loader  # new code entry
def load_user(id):  # new code entry
    return User.query.get(int(id)) # new code entry --- # slightly modified such that the user is loaded based on the id in the db

# user class
class User(db.Model, TimestampMixin, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password_hash = db.Column(db.String(128))
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    admin = db.Column(db.Integer, nullable=False, default=0)

    # print to console username created
    def __repr__(self):
        return f'<User {self.username}>'
    # generate user password i.e. hashing
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    # check user password is correct
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    # for reseting a user password
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')
    # verify token generated for resetting password
    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

# Cars class
class Cars(TimestampMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    manufacturer = db.Column(db.String(30), nullable=False)
    model = db.Column(db.String(50), nullable=False)
    summary = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Float, default=1970, nullable=False)
    mileage = db.Column(db.Float, default=1, nullable=False)
    transmission = db.Column(db.String(10), default='manual', nullable=False)
    fuel = db.Column(db.String(10), default='diesel', nullable=False)
    engine_size = db.Column(db.Float, default=0.0, nullable=False)
    seats = db.Column(db.Float, default=2, nullable=False)
    doors = db.Column(db.Float, default=2, nullable=False)
    colour = db.Column(db.String(20), default='white', nullable=False) # must be a pain to constantly wash
    mot = db.Column(db.Boolean, default=False, nullable=False)
    last_mot = db.Column(db.Text, default='01/01/1970', nullable=False)
    has_warranty = db.Column(db.Boolean, default=False, nullable=False)
    photo = db.Column(db.Text)

    def __init__(self):
        return f'<Cars {self.year, self.manufacturer, self.model}>'

# FAQ class
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, default='question', nullable=False)
    answer = db.Column(db.Text, default='answer', nullable=False)

    def __init__(self):
        return f'<FAQ {self.question}>'