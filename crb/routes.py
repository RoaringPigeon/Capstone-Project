from flask import render_template, url_for, flash, redirect
from crb import app, db, bcrypt
from crb.forms import RegistrationForm, LoginForm
from crb.models import User, ClassRoom
from flask_login import login_user, current_user, logout_user
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os

classRooms = [
    {
        'roomNumber' : '248',
        'availability' : True, 
        'booked' : False
    },
    {
        'roomNumber' : '250',
        'availability' : True, 
        'booked' : False
    },
    {
        'roomNumber' : '253',
        'availability' : True, 
        'booked' : False
    },
    {
        'roomNumber' : '255',
        'availability' : False, 
        'booked' : False
    },
    {
        'roomNumber' : '256',
        'availability' : False, 
        'booked' : False
    },
    {
        'roomNumber' : '258',
        'availability' : False, 
        'booked' : False
    }
]
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": os.environ['EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']
}
app.config.update(mail_settings)
mail = Mail(app)
s = URLSafeTimedSerializer('ThisIsSecret')

@app.route('/', methods=['GET'])

@app.route("/home")
def home():
    return render_template("home.html", title='Home', classRooms=classRooms)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Login unsuccessful. Please check email and password.', 'danger')
    return render_template("login.html", title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()

    if form.validate_on_submit():  # returns True when the form is submitted
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            password=hashed_password,
            email=form.email.data,
            email_confirmed=False
            )
        print(user.username, user.email_confirmed)  # print a msg for debugging.

        db.session.add(user)  # record user information to the database.
        db.session.commit()

        # Confirmation Email Code Block
        email = form.data.get('email') # get email address stored in the form.
        flash(f'User account is created succesfully for {form.username.data}. \
            Confirmation email has been sent to {email}', 'success')
        token = s.dumps(email, salt='email-confirm')  # generate a token for confirmation email.
        msg = Message('RoomBooker User Registration', sender='mgacabstone.crb@gmail.com', recipients=[email])
        confirmation_link = url_for('email_confirmed', token=token, _external=True)
        msg.body = 'Please click this link to confirm your email address and activate your account:<br>\
            <a href="{}">Activate your acount</a>'.format(confirmation_link)
        mail.send(msg)
        return redirect(url_for('login'))

    return render_template("register.html", title='Register', form = form)

@app.route("/emailsent/<message>")
def emailsent(message):
    return render_template("sendconfirmation.html", title='Confirmation email has been sent', content=message)

@app.route("/confirm/<token>")
# Checking new users confirmed their email addresses,
# then display confirmation message and activate the user account.
def email_confirmed(token):
    try:  # Check if the token is valid or not
        email = s.loads(token, salt='email-confirm', max_age=3600)  # token is valid for 3600 seconds (1 hour)

    except SignatureExpired:
        return '<h1>Your email confirmation link is expired.</h1>'

    # statements to update users table, Column 'email_confirmed=True'
    user = User.query.filter_by(email=email).first_or_404()
    user.email_confirmed = True
    db.session.add(user)
    db.session.commit()
    print(user.username, user.email_confirmed)  # For debugging

    return redirect(url_for('login')), flash ('Thank you. Your account is now activated. Please Sign-in.', 'success')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))