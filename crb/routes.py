from flask import render_template, url_for, flash, redirect, request
from crb import app, db, bcrypt
from crb.forms import RegistrationForm, LoginForm, UpdateAccountForm, BookForm, ApproveForm
from crb.models import User, ClassRoom, Request
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import os
import secrets
from PIL import Image


# Confirmation Email configuration
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'mgacabstone.crb@gmail.com',
    "MAIL_PASSWORD": 'zdulswfyxonrdull'
}
app.config.update(mail_settings)
mail = Mail(app)
s = URLSafeTimedSerializer('ThisIsSecret')

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html", title="ClassRoomBooker | Welcome")
    # direct users to the index(landing) page, which acts as a gateway before accessing the protected pages.

@app.route("/home", methods=['GET', 'POST'])
@login_required
# def home():
#     # querying records of ClassRoom table, and send it home.html for displaying status
#     rooms = ClassRoom.query.order_by(ClassRoom.id).all()
#     print(rooms)
#     return render_template("home.html", title='Home', classRooms=rooms)
def home():
    rule = request.url_rule
    classRooms = ClassRoom.query.all()
    form = BookForm()
    l = len(classRooms)
    m = l%3
    if form.validate_on_submit():
        n = form.roomNumber.data
        r = ClassRoom.query.filter_by(roomNumber=n).first()
        if r.availability == True:
            r.pending = True
            request1 = Request(requestingUser = current_user.id, requestedRoom = r.id)
            db.session.add(request1)
            flash(f'Request for room {n} has been sent.', 'success')
        else:
            flash(f'Room {n} is not available at this time.', 'danger')
        db.session.commit()
        
        return redirect(url_for('home'))
    return render_template("home.html", title='Home', classRooms=classRooms, form=form, rule=rule, m=m, y=l-m,  f=l//3)

@app.route("/about")
def about():
    return render_template("about.html", title='About')

## roomstatus (Admin menu) code block Start ##
@app.route("/roomstatus", methods=['POST', 'GET'])
@login_required
# Only Admin account should access this page
# Add a new classroom to site.db (ClassRoom table, refer to model.py)
def roomstatus():
    if request.method == 'POST':
        roomNumber = request.form['roomNumber']
        new_room = ClassRoom(roomNumber=roomNumber)
        try:
            db.session.add(new_room)
            db.session.commit()
            return redirect('/roomstatus')
        except:
            return 'There was an issue adding a new classroom'
    else:
        rooms = ClassRoom.query.order_by(ClassRoom.id).all()
        print(rooms)
        return render_template('roomstatus.html', rooms=rooms, title='roomstatus manager')

@app.route('/deleteroom/<int:id>')
# related to roomstatus.html page: delete a classroom from db
def delete_room(id):
    room_to_delete = ClassRoom.query.get_or_404(id)
    try:
        db.session.delete(room_to_delete)
        db.session.commit()
        return redirect('/roomstatus')
    except:
        return 'There was a problem deleting that classroom'

@app.route("/updateroom/<int:id>/<int:available>")
# related to roomstatus.html page: apply change of a classroom's status
def update_room_availability(id, available):
    room = ClassRoom.query.get_or_404(id)
    check = available
    print(check)
    if check == 1:
        room.availability = True
        db.session.commit()
    else:
        room.availability = False
        db.session.commit()
    return redirect('/home')
## roomstatus (Admin page) code block End ##


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
    flash('Logged out.', 'success')
    return redirect(url_for('login'))

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


# Merged Andrew's code block (4/17/2020)
@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    rule = request.url_rule
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
    return render_template('account.html', title="Account", image_file=image_file, rule=rule, form=form)


# Merged Andrew's code block (4/17/2020)
@app.route("/admin", methods=['GET', 'POST'])
@login_required
def admin():
    rule = request.url_rule
    form = ApproveForm()
    classRooms = ClassRoom.query.all()
    requests = Request.query.all()
    if current_user.admin == True:
        if form.validate_on_submit():
            room = ClassRoom.query.filter_by(roomNumber = form.roomNumber.data).first()
            request1 = Request.query.filter_by(id=form.request.data).first()
            user = request1.requester.username
            if form.choice.data == 'approved':
                room.pending=False
                room.availability=False
                room.booked=True             
                db.session.delete(request1)
                db.session.commit()
                flash(f'Request for room {room.roomNumber} by {user} has been approved.', 'success')
                return redirect(url_for('admin'))
            else:
                room.pending = False
                db.session.delete(request1)
                db.session.commit()
                flash(f'Request for room {room.roomNumber} by {user} has been denied.', 'warning')
                return redirect(url_for('admin'))
    else:
        return redirect(url_for('home'))
    return render_template('admin.html', title="Administrator", classRooms = classRooms, requests = requests, form=form, rule=rule)