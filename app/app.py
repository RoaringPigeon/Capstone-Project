
from flask import Flask, render_template, request, send_from_directory, redirect, url_for
app = Flask(__name__, static_url_path='/static')

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
def homePage():
    return render_template("home.html", title='Home', classRooms=classRooms)
@app.route("/login")
def loginPage():
    return render_template("login.html", title='Login')
@app.route("/register")
def registerPage():
    return render_template("register.html", title='Register')