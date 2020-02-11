
from flask import Flask, render_template, url_for, redirect
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from forms import RegistrationForm, LoginForm


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '73982ac8l3l2hs7blh43l29bliha82914'

mail = Mail(app)
s = URLSafeTimedSerializer('ThisIsSecret')

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
@app.route("/login")
def login():
    form = LoginForm()
    return render_template("login.html", title='Login', form=form)
@app.route("/confirmation/<message>")
def confirmation(message):
    return render_template("sendconfirmation.html", title='Confirmation email has been sent', content=message)

@app.route("/register", methods=['GET', 'POST'])
# Display register.html on the browser and its associated form from forms.py
def register():
    form = RegistrationForm()
    if form.validate_on_submit():  # return True when the form is submitted
        email = form.data.get('email') # get email address stored in form.
        print("Registered user email:", email)
        token = s.dumps(email, salt='email-confirm')
        msg = Message('RoomBooker User Registration', sender='jinyoungan85@gmail.com', recipients=[email])
        link = url_for('register', token=token, _external=True)
        msg.body = 'Click this link to complete your user account registration: {}'.format(link)
        mymsg = 'Confirmation email has been sent to {}. Token is {}'.format(email, token)
        # mail.send(msg)
        return redirect(url_for('confirmation', message=mymsg))
    return render_template("register.html", title='Register', form = form)

# When completed form is submitted, create a token, 
# and send a confirmation email to the registered address.
# def sendConfirmationMail():
#     form = RegistrationForm()
#     email = form.data.get('email') # get email address stored in form.
#     print("Registered user email:", email)
#     token = s.dumps(email, salt='email-confirm')
#     msg = Message('RoomBooker User Registration', sender='jinyoungan85@gmail.com', recipients=[email])
#     link = url_for('register', token=token, _external=True)
#     msg.body = 'Click this link to complete your user account registration: {}'.format(link)
#     mymsg = '<h1>Confirmation email has been sent to {}. Token is {}</h1>'.format(email, token)
#     print(mymsg)
#     # return redirect('confirmation')
#     # mail.send(msg)
#     #return '<h1>Confirmation email has been sent to {}. Token is {}</h1>'.format(email, token)


@app.route("/register/<token>")
# Checking a registered user clicked the link in the confirmation email,
# then display confirmation message and completion of the user registration.
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=60)
    except SignatureExpired:
        return '<h1>Your email confirmation link is expired.'
    # statements to change user database, 'confire=True'
    return '<h1>Thank you. Now your registration is completed. Please Sign-in.'