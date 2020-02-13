from flask import render_template, url_for, flash, redirect
from crb import app, db, bcrypt
from crb.forms import RegistrationForm, LoginForm
from crb.models import User, ClassRoom
from flask_login import login_user, current_user, logout_user

classRooms = [
    {
        'roomNumber' : '255',
        'availability' : True, 
        'booked' : False
    },
    {
        'roomNumber' : '254',
        'availability' : False, 
        'booked' : False
    }
]

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
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created succesfully for {form.username.data}.', 'success')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form = form)
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))