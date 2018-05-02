# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect, url_for


# Import module forms
from app.mod_auth.forms import LoginForm, SignUpForm

# Import module models (i.e. User)
from app.appModel.models import User

#to decode form data
import unicodedata

from app.mod_database import db
from app import login_manager

# Login Manager configuration.
login_manager.login_view = '/auth/signin/'

@login_manager.user_loader
def user_loader(user_id):
    user = User.query.filter_by(id=user_id).first()
    return None if not user else user


# Define the blueprint: 'auth', set its url prefix: app.url/auth
mod_auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='../templates/auth')

# Set the route and accepted methods

@mod_auth.route('/signin/', methods=['GET', 'POST'])
def signin():

    # If sign in form is submitted
    form = LoginForm(request.form)
    print(request.args)
    # Verify the sign in form
    if form.validate_on_submit():
        user = User.query.filter(User.email == form.email.data.encode()).first()

        if user and user.password == form.password.data.encode():
            session['user_id'] = user.id
            session['user_name'] = user.name
            next = request.args.get('next')
            print(request.args)
            print('we are moving to', next)
            return redirect(next or '/')

        else:
            flash('Wrong email or password', 'error')
    return render_template('signin.html', form=form)


@mod_auth.route('/signup/', methods=['GET', 'POST'])
def signup():
    # If sign in form is submitted
    form = SignUpForm(request.form)

    # Verify the sign in form
    if form.validate_on_submit():
        email = unicodedata.normalize('NFKD', form.email.data).encode('ascii', 'ignore')
        name = unicodedata.normalize('NFKD', form.name.data).encode('ascii', 'ignore')
        password = unicodedata.normalize('NFKD', form.password.data).encode('ascii', 'ignore')
        user = User(name, email, password)
        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return redirect('/')

    return render_template('signup.html', form=form)


@mod_auth.route('/logout/', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('auth.signin'))
