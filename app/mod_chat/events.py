from flask import session
from flask_socketio import emit, join_room, leave_room

from app.appModel.models import User
from .. import socketio

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('user_id')
    join_room(room)
    # emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room)


@socketio.on('textMessage', namespace='/chat')
def textMessageSent(message, users):
    """Mensaje de texto enviado por el cliente a un usuario en particular
      Se envia un evento tanto al emisor como al destinatario
      (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
    """
    print(message, users)
    for user in users:
      emit('message', {'msg': message}, room=user)
      print ('Emitido:', message, user)



