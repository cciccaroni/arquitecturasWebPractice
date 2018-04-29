from flask import Blueprint, session, render_template, request
from flask_socketio import join_room
from werkzeug.utils import redirect

from app import mod_index
from app.appModel.models import User
from app.mod_database import db

mod_list = Blueprint('list', __name__)


@mod_list.route('/', methods=['GET'])
def chat():
    user_id = session.get('user_id', None)
    if user_id:
        return render_template("bootstrap_prueba/bootstrap.html", 
                                users=User.query.all(), 
                                user=user_id, text="1")
    
    return redirect("auth/signin")