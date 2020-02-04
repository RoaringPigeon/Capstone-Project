
from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm
app = Flask(__name__, static_url_path='/static')

app.config['SECRET_KEY'] = '73982ac8l3l2hs7blh43l29bliha82914'

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
@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template("register.html", title='Register', form = form)