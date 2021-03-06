from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField, TextAreaField, HiddenField, RadioField, 
SelectField, TextField, StringField)
from wtforms.fields.html5 import DateField, TimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from crb.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators = [DataRequired(), EqualTo('password') ])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists. Please choose a different username.')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('An account has already been created with this Email.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired()])
    submit = SubmitField('Login')

# Merged Andrew's code block (4/17/2020)
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators = [DataRequired(), Email()])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already exists. Please choose a different username.')
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('An account has already been created with this Email.')

class BookForm(FlaskForm):
    roomNumber = HiddenField('Room_Number')
    submit = SubmitField('Confirm')
    date = HiddenField('datePicked')
    time = HiddenField('timePicked')
    timeSelect = TimeField('Time Desired', format="%H:%M", validators= [DataRequired()])
    dateSelect = DateField('Date Desired', format='%Y-%m-%d', validators = [DataRequired()])
    duration = SelectField('Programming Language',
        choices=[('0.5', '0.5 Hours'), ('1', '1 Hour'), ('1.5', '1.5 Hours'), ('2', '2 Hours')],
        validators=[DataRequired()]
    )
    reason = StringField('Reason for Booking', validators = 
        [DataRequired(), Length(max=60)])

class ApproveForm(FlaskForm):
    roomNumber = HiddenField('Room_Number')
    request = HiddenField('Request_Number')
    choice = RadioField('Action to be taken:', choices=[('approved', 'Approve'), ('denied', 'Deny')], default='approved', validators = [DataRequired()])
    reason = StringField('Reason for Choice', validators = [DataRequired(), Length(max=100)])
    submit = SubmitField('Submit')