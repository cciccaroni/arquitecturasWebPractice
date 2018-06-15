import functools

from flask import session
from flask_socketio import join_room, emit, disconnect
import uuid
from app import socketio
from app import app
from app.appModel.models import User, Conversation
from app.mod_api.integrator import exportMessage
from app.mod_conversation.conversation_api import conversation_manager
from app.constants import APPLICATION_PATH, APPLICATION_IMAGES_PATH, APPLICATION_AUDIOS_PATH


#TODO: check if user is authenticated and redirect?
def authentication_required(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        userIsAuthenticated = True
        if not userIsAuthenticated:
            disconnect()
        else:
            return f(*args, **kwargs)
    return wrapped


@socketio.on('joined', namespace='/chat')
@authentication_required
def joined():
    user_id = session.get('user_id', None)
    join_room(user_id)

# @socketio.on('newUser', namespace='/chat')
# @authentication_required
# def newUser():
#     user_id = session.get('user_id', None)


@socketio.on('textMessage', namespace='/chat')
@authentication_required
def textMessage(text, recipients, conversationId, loggedUserName):
    """Texto enviado por el cliente
        Se envia un evento a todos los participantes con el texto
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    conversation_manager.log_message(user_id, text, conversationId, "text")
    setupAndSendEvent(recipients, 'uiTextMessage', {'msg': text}, loggedUserName, conversationId, user_id)


@socketio.on('imageMessage', namespace='/chat')
@authentication_required
def imageMessage(image, recipients, conversationId, loggedUserName):
    """Imagen enviada por el cliente
      Se envia un evento a todos los participantes con la imagen
    """

    user_id = session.get('user_id', None)
    if not user_id:
        return

    filePath = saveFile(image, APPLICATION_IMAGES_PATH, '.png')
    conversation_manager.log_message(user_id, filePath, conversationId, "image")
    setupAndSendEvent(recipients, 'uiImageMessage', {'imagePath': filePath}, loggedUserName, conversationId, user_id)


@socketio.on('audioMessage', namespace='/chat')
@authentication_required
def audioMessage(audio, recipients, conversationId, loggedUserName):
    """Audio enviada por el cliente
      Se envia un evento a todos los participantes con el audio
    """
    user_id = session.get('user_id', None)
    if not user_id:
        return

    filePath = saveFile(audio, APPLICATION_AUDIOS_PATH, '.wav')
    conversation_manager.log_message(user_id, filePath, conversationId, "audio")
    setupAndSendEvent(recipients, 'uiAudioMessage', {'audioPath': filePath}, loggedUserName, conversationId, user_id)


def setupAndSendEvent(recipients, eventName, data, sender, conversationId, user_id):
    data['user_id'] = user_id
    data['from'] = sender
    data['conversationId'] = conversationId
    group = Conversation.query.filter(Conversation.id == conversationId).first().group
    if group:
        data['group'] = group.name
        data['group_id'] = group.id
    sendEventToRecipients(data, eventName, recipients)


def sendEventToRecipients(data, eventName, recipients=None):
    if (recipients):
        users = User.query.filter(User.id.in_(recipients)).all()
    else:
        users = User.query.all()
    
    thereIsAnExternalUser = False
    for user in users:
        if user.platform_id == app.config.platformId:
            socketio.emit(eventName, data, room=user.id, namespace='/chat')
        else: 
            thereIsAnExternalUser = True

    if thereIsAnExternalUser:
        exportMessage(data)


def saveFile(file, applicationFileTypePath, fileExtension):
    id = uuid.uuid4().hex  # server-side filename
    file_relative_path = applicationFileTypePath + id + fileExtension
    f = open(APPLICATION_PATH + file_relative_path, 'wb')
    f.write(file)
    return file_relative_path
