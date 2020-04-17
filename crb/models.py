from crb import db, login_manager, bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    admin = db.Column(db.Boolean, unique=False, default=False) # will make it so that only Admins can appoint a user to be an Admin.
    email_confirmed = db.Column(db.Boolean, default=True)  # for confirmation email, default value is False.
    requests = db.relationship('Request', backref='requester')

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.admin}', '{self.email_confirmed}' '{self.requests}')"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.String(3), unique=True, nullable=False)
    availability = db.Column(db.Boolean, unique=False, default=True)
    booked = db.Column(db.Boolean, unique=False, default=False)
    pending = db.Column(db.Boolean, unique=False, default=False)
    requests = db.relationship('Request', backref='requested')

    def __repr__(self):  # method for debugging/test
        return f"Room('{self.roomNumber}', '{self.availability}', '{self.booked}', '{self.booked}', {self.pending}', '{self.requests}')"

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requestingUser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requestedRoom = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    pending = db.Column(db.Boolean, unique=False, default=True)
    approved = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f"Request('{self.requestingUser}', '{self.requestedRoom}', '{self.pending}', '{self.approved}')"

    
db.drop_all()
db.create_all()
hashed_password = bcrypt.generate_password_hash("Password1").decode('utf-8')
user1 = User(username="Andrew", email="Andrew@demo.com", password=hashed_password, admin=True, email_confirmed=True)
user2 = User(username="Melissa", email="Melissa@demo.com", password=hashed_password, email_confirmed=True)
room1 = Room(roomNumber = "248")
room2 = Room(roomNumber = "250", pending=True)
room3 = Room(roomNumber = "253")
room4 = Room(roomNumber = "255", availability=False)
room5 = Room(roomNumber = "256")
room6 = Room(roomNumber = "258")
db.session.add(user1)
db.session.add(user2)
db.session.add(room1)
db.session.add(room2)
db.session.add(room3)
db.session.add(room4)
db.session.add(room5)
db.session.add(room6)
db.session.commit()
request1 = Request(requestingUser = user2.id, requestedRoom = room2.id)
db.session.add(request1)
db.session.commit()