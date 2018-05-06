from flask import session
from flask_socketio import join_room, emit
import uuid
from app import socketio
from app.appModel.models import User
from app.mod_conversation.conversation_api import conversation_manager
from app.constants import APPLICATION_PATH, APPLICATION_IMAGES_PATH, APPLICATION_AUDIOS_PATH


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



@socketio.on('textMessage', namespace='/chat')
def textMessage(text, recipients, conversationId, loggedUserName):
    """Texto enviado por el cliente
        Se envia un evento a todos los participantes con el texto
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    conversation_manager.log_message(user_id, text, conversationId, "text")

    data = {'msg': text, 'from': loggedUserName}
    sendEventToRecipients(recipients, data, 'uiTextMessage')



@socketio.on('imageMessage', namespace='/chat')
def imageMessage(image, recipients, conversationId, loggedUserName):
    """Imagen enviada por el cliente
      Se envia un evento a todos los participantes con la imagen
    """

    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    filePath = saveFile(image, APPLICATION_IMAGES_PATH, '.png')
    conversation_manager.log_message(user_id, filePath, conversationId, "image")

    data = {'imagePath': filePath, 'from': loggedUserName}
    sendEventToRecipients(recipients, data, 'uiImageMessage')


@socketio.on('audioMessage', namespace='/chat')
def audioMessage(audio, recipients, conversationId, loggedUserName):
    """Audio enviada por el cliente
      Se envia un evento a todos los participantes con el audio
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    my_user = User.query.get(user_id)
    if not my_user:
        return

    filePath = saveFile(audio, APPLICATION_AUDIOS_PATH, '.wav')
    conversation_manager.log_message(user_id, filePath, conversationId, "audio")

    data = {'audioPath': filePath, 'from': loggedUserName}
    sendEventToRecipients(recipients, data, 'uiAudioMessage')


def sendEventToRecipients(recipients, data, eventName):
    for recipient in recipients:
        emit(eventName, data, room=recipient)


def saveFile(file, applicationFileTypePath, fileExtension):
    id = uuid.uuid4().hex  # server-side filename
    file_relative_path = applicationFileTypePath + id + fileExtension
    f = open(APPLICATION_PATH + file_relative_path, 'wb')
    f.write(file)
    return file_relative_path
