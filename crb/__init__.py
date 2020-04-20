from flask import Flask, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = '73982ac8l3l2hs7blh43l29bliha82914'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

# Merged Andrew's code block(4/17/2020)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.unauthorized_handler
# handles unauthorized access to protected pages. If not logged in, redirect to the login page.
# The protected pages are decorated w/ @login_required (check out routes.py)
def unauth_handler():
    flash('Please login to access our services.', 'danger')
    return redirect(url_for('login'))

from crb import routes