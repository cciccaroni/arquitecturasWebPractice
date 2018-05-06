from flask import session, url_for
from flask_socketio import join_room, emit
import wave
import uuid
from app import socketio
from app.appModel.models import User
from app.mod_conversation.conversation_api import conversation_manager
from config import APPLICATION_PATH, APPLICATION_IMAGES_PATH, APPLICATION_AUDIOS_PATH


@socketio.on('joined', namespace='/chat')
def joined():
    # """Sent by clients when they enter a room.
    # A status message is broadcast to all people in the room."""
    user_id = session.get('user_id', None)
    
    # Join into my room
    join_room(user_id)

    # Broadcast of my new status to all users.
    # status = {'msg': {'id': my_user.id, 'name': str(my_user.name), 'status': 'ENTERED'}}
    # users = User.query.all()
    # for user in users:
    #     emit('status', status, room=user.id)



# Se deberia iterar el toIds, que vienen todos los ids a los que hay que enviar el evento
@socketio.on('textMessage', namespace='/chat')
def textMessage(text, recipients, conversationId, loggedUserName):
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

    conversation_manager.log_message(user_id, text, conversationId, "text")

    status = {'msg': text, 'from': loggedUserName}
    for recipient in recipients:
        emit('uiTextMessage', status, room=recipient)
    print("mensaje enviado a los miembros del chat")



@socketio.on('imageMessage', namespace='/chat')
def imageMessage(image, recipients, conversationId, loggedUserName):
    """Imagen enviada por el cliente a un usuario en particular
      Se envia un evento tanto al emisor como al destinatario
      (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
    """

    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    id = uuid.uuid4().hex  # server-side filename
    file_relative_path = APPLICATION_IMAGES_PATH + id + '.png'
    f = open(APPLICATION_PATH + file_relative_path, 'wb')
    f.write(image)

    conversation_manager.log_message(user_id, file_relative_path, conversationId, "image")

    status = {'imagePath': file_relative_path, 'from': loggedUserName}
    for recipient in recipients:
        emit('uiImageMessage', status, room=recipient)


@socketio.on('audioMessage', namespace='/chat')
def audioMessage(audio, recipients, conversationId, loggedUserName):
    """Imagen enviada por el cliente a un usuario en particular
      Se envia un evento tanto al emisor como al destinatario
      (emisor updetea la ui mostrando el nuevo mensaje cada vez que recibe un evento, lo mismo el destinatario)
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    id = uuid.uuid4().hex  # server-side filename
    file_relative_path = APPLICATION_AUDIOS_PATH + id + '.wav'
    f = open(APPLICATION_PATH + file_relative_path, 'wb')
    f.write(audio)

    conversation_manager.log_message(user_id, file_relative_path, conversationId, "audio")

    status = {'url': file_relative_path, 'from': loggedUserName}
    for recipient in recipients:
        emit('uiAudioMessage', status, room=recipient)

