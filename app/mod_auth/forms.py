# Import Form and RecaptchaField (optional)
from flask_wtf import FlaskForm # , RecaptchaField

# Import Form elements such as TextField and BooleanField (optional)
from wtforms import TextField, PasswordField, fields

# Import Form validators
from wtforms.validators import Email, DataRequired, Length


# Define the login form (WTForms)

class LoginForm(FlaskForm):
    email    = TextField('Email Address', [Email(), DataRequired(message='Forgot your email address?')])
    password = PasswordField('Password', [DataRequired(message='Must provide a password.')])
    remember = fields.BooleanField(label='Remember me')


#Define signUp form

class SignUpForm(FlaskForm):
    name = TextField('Name', [DataRequired(message='Please, enter your name')])
    email = TextField('Email Address', [Email(), DataRequired(message='Please, enter a valid email address for sign up')])
    password = PasswordField('Password', [Length(min=6, message='Length must be at least 6'), DataRequired(message='Please, provide a password')])