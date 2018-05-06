# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect, url_for, g


# Import module forms
from app.mod_auth.forms import LoginForm, SignUpForm

# Import module models (i.e. User)
from app.appModel.models import User

#to decode form data
import unicodedata

from app.mod_database import db

from flask_login import login_user, logout_user, current_user
from . import LoggedUser

# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates/auth')

# Set the route and accepted methods

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)
    next = request.args.get('next')
    
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()

        if user and user.password == form.password.data:
            login_user(LoggedUser(user), remember=form.remember.data)
            # Now the user is accesible via current_user
            return redirect(next or '/')

        else:
            flash('Wrong email or password', 'error')
    
    if (next):
      return render_template('signin.html', form=form, next=next)

    return render_template('signin.html', form=form)


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    # If sign in form is submitted
    form = SignUpForm(request.form)
    next = request.args.get('next')

    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data).first()
        if not user:
            email = form.email.data
            name = form.name.data
            password = form.password.data
            user = User(name, email, password)
            db.session.add(user)
            db.session.commit()
            
            login_user(LoggedUser(user))
            return redirect(next or '/')

        flash('Email already exists', 'error')

    if (next):
        return render_template('signup.html', form=form, next=next)

    return render_template('signup.html', form=form)


@mod_auth.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('auth.signin'))
