from flask import Blueprint, session, render_template, request
from werkzeug.utils import redirect

from app import socketio
from app.appModel.models import User
from flask_socketio import emit, join_room


mod_list = Blueprint('list', __name__)


@mod_list.route('/', methods=['GET'])
def chat():
    if session.get('user_id'):
        return render_template("bootstrap_prueba/bootstrap.html", users=User.query.all(), text="1")
    else:
        return redirect("auth/signin")


@socketio.on('textMessage', namespace='/chat')
def text_message_sent(json):
    """habria que emitir tambien a la room del adressee user que venga en el json"""
    name = User.query.filter(User.id == session['user_id']).first().name
    emit('updateUiWithTextMessage', {'msg': json['msg']}, room=session.get('user_id'))


@socketio.on('joinMe', namespace='/chat')
def joined(message):
    """Enviado por un usuario para ser joineado a su sala"""
    join_room(session.get('user_id'))
