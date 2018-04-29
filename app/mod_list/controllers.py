from flask import Blueprint, session, render_template, request
from werkzeug.utils import redirect

from app import socketio
from app.appModel.models import User
from flask_socketio import emit, join_room


mod_list = Blueprint('list', __name__)


@mod_list.route('/', methods=['GET'])
def chat():
    user_id = session.get('user_id', None)
    if user_id:
        return render_template("contacts/list.html", 
                                users=User.query.all(), 
                                user=user_id, text="1")
    
    return redirect("auth/signin")