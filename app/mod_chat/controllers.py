from flask import Blueprint, request, session, render_template
from flask_socketio import join_room, emit
from werkzeug.utils import redirect

from app import socketio
from app.appModel.models import Conversation, User
from app.mod_database import db

mod_chat = Blueprint('chat', __name__, url_prefix="/chat")


@mod_chat.route('/<user_id>', methods=['GET'])
def chat(user_id):
    actual_user = User.query.filter(User.id == session['user_id']).first()
    if not actual_user:
      return redirect("auth/signin")

    adressee_user = User.query.filter(User.id == user_id).first()
    conversations = actual_user.conversations
    users_have_conversation = len(list(filter(lambda conversation: actual_user in conversation.users and adressee_user in conversation.users, conversations))) > 0
    if not users_have_conversation:
        conversation = Conversation([actual_user, adressee_user])
        db.session.add(conversation)
        db.session.commit()

    return render_template("chat/chat.html", adressee=adressee_user, actual_user=actual_user)


#Los handlers los saque de events.py porque de ahi no se me llamaban
@socketio.on('joined', namespace='/chat')
def joined():
    # """Sent by clients when they enter a room.
    # A status message is broadcast to all people in the room."""
    user_id = session.get('user_id', None)
    my_user = User.query.get(user_id)
    if not my_user:
        return

    # Join into my room
    join_room(user_id)
    print("user joineado")

    # Broadcast of my new status to all users.
    # status = {'msg': {'id': my_user.id, 'name': str(my_user.name), 'status': 'ENTERED'}}
    # users = User.query.all()
    # for user in users:
    #     print (str(user_id), 'sending join status to', str(user.id))
    #     emit('status', status, room=user.id)


@socketio.on('textMessage', namespace='/chat')
def textMessage(json):
    """Mensaje de texto enviado por el cliente a un usuario en particular
      Se envia un evento tanto al emisor como al destinatario
      (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    status = {'msg': json['msg'], 'from': json['fromName']}
    emit('uiTextMessage', status, room=user_id)
    emit('uiTextMessage', status, room=json['toId'])
    print("mensaje enviado a los miembros del chat")
    # for user in users:
    #     print ('Sending:', message, user)
    #     emit('message', status, room=int(user))

