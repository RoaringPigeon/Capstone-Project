from crb import db, login_manager
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)  # for confirmation email, default value is False.

    def __repr__(self):  # method for debugging/test
        return f"User('{self.username}', '{self.email}')"

class ClassRoom(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.String(3), unique=True, nullable=False)
    availability = db.Column(db.Boolean, unique=False, default=True)
    # booked = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):  # method for debugging/test
        return f"ClassRoom('{self.roomNumber}', '{self.availability}')"