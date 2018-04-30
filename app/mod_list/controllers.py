from flask import Blueprint, session, render_template, request
from werkzeug.utils import redirect

from app import socketio
from app.appModel.models import User
from flask_socketio import emit, join_room


mod_list = Blueprint('list', __name__)


@mod_list.route('/index', methods=['GET'])
def chat():
    actual_user = User.query.filter(User.id == session['user_id']).first()
    if actual_user:
        return render_template("contacts/list.html", 
                                users=User.query.all(), 
                                actual_user=actual_user, text="1")
    
    return redirect("auth/signin")
