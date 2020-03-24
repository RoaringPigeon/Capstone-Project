import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request
from crb import app, db, bcrypt
from crb.forms import RegistrationForm, LoginForm, UpdateAccountForm, BookForm
from crb.models import User, ClassRoom
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired



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

@app.route('/', methods=['GET', 'POST'])

@app.route("/home", methods=['GET', 'POST'])
def home():
    classRooms = ClassRoom.query.all()
    form = BookForm()
    if form.validate_on_submit():
        n = form.roomNumber.data
        r = ClassRoom.query.filter_by(roomNumber=n).all()[0]
        if r.availability == True:
            r.availability = False
            r.boooked = True
            flash(f'You have successfully booked room {n}.', 'success')
        else:
            r.availability = True
            r.booked = False
            flash(f'You have canceled your booking of room {n}.', 'success')
        db.session.commit()
        
        
        return redirect(url_for('home'))
    return render_template("home.html", title='Home', classRooms=classRooms, form=form)

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
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
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

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title="Account", image_file=image_file, form=form)

