from flask import session
from flask_socketio import emit, join_room, leave_room

from app.appModel.models import User
from .. import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    user_id = session.get('user_id', None)
    if not user_id:
      return
    
    my_user = User.query.get(user_id)
    if not my_user:
      return
    
    # Join into my room
    join_room(user_id)

    # Broadcast of my new status to all users.
    status = {'msg': {'id': my_user.id, 'name': str(my_user.name), 'status': 'ENTERED'}}
    users = User.query.all()
    for user in users:
        print (str(user_id), 'sending join status to', str(user.id))
        emit('status', status, room=user.id)


@socketio.on('textMessage', namespace='/chat')
def textMessage(message, users):
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

    status = {'msg': message, 'from': {'name': str(my_user.name), 'id': my_user.id}}
    for user in users:
        print ('Sending:', message, user)
        emit('message', status, room=int(user))

@socketio.on('imageMessage', namespace='/chat')
def imageMessage(message, users):
    """Iamgen enviado por el cliente a un usuario en particular
      Se envia un evento tanto al emisor como al destinatario
      (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
    """
    user_id = session.get('user_id', None)
    if not user_id:
      return

    my_user = User.query.get(user_id)
    if not my_user:
      return

    status = {'msg': message, 'from': {'name': str(my_user.name), 'id': my_user.id}}
    for user in users:
        emit('image', status, room=int(user))

@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    user_id = session.get('user_id')
    status = {'msg': {'id': user_id, 'status': 'LEFT'}}
    users = User.query.all()
    for user in users:
        print (str(user_id), 'sending left status to', user.name)
        emit('status', status, room=user.id)
