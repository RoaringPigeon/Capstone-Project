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
    password = db.Column(db.String(60), nullable=False)
    email_confirmed = db.Column(db.Boolean, default=False)  # for confirmation email, default value is False.
    
    # Merged Andrew's code block (4/17/2020)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    admin = db.Column(db.Boolean, unique=False, default=False) # will make it so that only Admins can appoint a user to be an Admin.
    requests = db.relationship('Request', backref='requester')

    def __repr__(self):  # method for debugging/test
        # return f"User('{self.username}', '{self.email}')"
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.admin}', '{self.email_confirmed}' '{self.requests}')"

class ClassRoom(db.Model):
    # Fixed sqlalchemy.exc.NoReferencedTableError, by changing table name to match ClassRoom table ('class_room' in db)
    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.String(3), unique=True, nullable=False)
    availability = db.Column(db.Boolean, unique=False, default=True)
    booked = db.Column(db.Boolean, unique=False, default=False)
    
    # Merged Andrew's code block (4/17/2020)
    pending = db.Column(db.Boolean, unique=False, default=False)
    requests = db.relationship('Request', backref='requested')

    def __repr__(self):  # method for debugging/test
        # return f"ClassRoom('{self.roomNumber}', '{self.availability}')"
        return f"ClassRoom('{self.roomNumber}', '{self.availability}', '{self.booked}', '{self.booked}', {self.pending}', '{self.requests}')"


class Request(db.Model):
    # Merged Andrew's code block (4/17/2020)
    id = db.Column(db.Integer, primary_key=True)
    requestingUser = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    requestedRoom = db.Column(db.Integer, db.ForeignKey('class_room.id'), nullable=False) # class_room
    date = db.Column(db.String(10), unique=False, nullable=False)
    time = db.Column(db.Time, unique=False, nullable=False)
    pending = db.Column(db.Boolean, unique=False, default=True)
    approved = db.Column(db.Boolean, unique=False, default=False)

    def __repr__(self):
        return f"Request('{self.requestingUser}', '{self.requestedRoom}', '{self.pending}', '{self.approved}', '{self.date}', {self.time}')"

db.drop_all()
db.create_all()
hashed_password = bcrypt.generate_password_hash("Password1").decode('utf-8')
user1 = User(username="Andrew", email="Andrew@demo.com", password=hashed_password, admin=True, email_confirmed=True)
user2 = User(username="Melissa", email="Melissa@demo.com", password=hashed_password, email_confirmed=True)
room1 = ClassRoom(roomNumber = "248")
room2 = ClassRoom(roomNumber = "250")
room3 = ClassRoom(roomNumber = "253")
room4 = ClassRoom(roomNumber = "255")
room5 = ClassRoom(roomNumber = "256")
room6 = ClassRoom(roomNumber = "258")
db.session.add(user1)
db.session.add(user2)
db.session.add(room1)
db.session.add(room2)
db.session.add(room3)
db.session.add(room4)
db.session.add(room5)
db.session.add(room6)
db.session.commit()