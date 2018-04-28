from flask import Blueprint, session, render_template, request
from werkzeug.utils import redirect

from app import mod_index
from app.mod_auth.models import User
from app.mod_database import db

mod_chat = Blueprint('chat', __name__)

@mod_chat.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'GET':
        if session.get('user_id'):
            return render_template("bootstrap_prueba/bootstrap.html", users=User.query.all())
        else:
            return redirect("auth/signin")
    else:
        return 'ok'

