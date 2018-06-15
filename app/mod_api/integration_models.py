from app.appModel.models import *
from app.mod_api.integrator import importAll
from app.mod_conversation.conversation_api import conversation_manager
from flask_socketio import join_room, emit, disconnect
from app import socketio
from app import app

import functools



def getUsersJson():
    result = []
    users = User.query.filter(User.platform_id == 1)
    for user in users:
        result.append({'id': user.id, 'name': user.name})
    return result

def saveExternalUser(id, name, platformName):
    users = User.query.all()

    platform = Platform.query.filter(Platform.name == platformName).first()
    if platform:
        email = name + "@" + platformName
        _user = User(name, email, 'bla', platform.id, id)
        db.session.add(_user)
        db.session.flush()
        db.session.commit()
        app.logger.debug('Saved as external {}-{}'.format(_user, platformName))
        newUser = {
          'id':_user.id,
          'name': _user.name
        }
        for user in users:
            if user.platform_id == app.config.platformId:
                app.logger.debug('Adverting {}: {}; to: {}'.format('newUser', newUser, user.id))
                socketio.emit('newUser', newUser, room=user.id, namespace='/chat')
    else:
        platforms = Platform.query.all()
        app.logger.debug('Platform not found. {}-{}-{}'.format(id, name, platformName))
        app.logger.debug('Available platforms: {}'.format([p.name for p in platforms]))
        importAll()
    return

def saveExternalConversation(id, name, platformName, type, users):
    if type == "private":

        fromPlatformId = Platform.query.filter(Platform.name == platformName).first().id

        if list(users[0].keys())[0] == platformName:
            fromUserId =  list(users[0].values())[0][0]
            toUserId =  list(users[1].values())[0][0]
        else:
            fromUserId =  list(users[1].values())[0][0]
            toUserId =  list(users[0].values())[0][0]

        "el from user lo tengo que buscar por external id y por platform id"
        "el from user es el que coincide con el from platform"
        "el to user lo busco por id"

        fromUser = User.query.filter(User.external_id == fromUserId, User.platform_id == fromPlatformId).first()
        toUser = User.query.filter(User.id == toUserId).first()


        conversation = Conversation(users=[fromUser, toUser], platform_id = fromPlatformId, external_id= id)
        db.session.add(conversation)
        db.session.flush()
        db.session.commit()

def saveAndSendMessageToInternalUsers(roomOriginalPlatform, roomId, senderId, senderPlatform, text):
    roomOriginalPlatformId = Platform.query.filter(Platform.name == roomOriginalPlatform).first().id
    if roomOriginalPlatformId == app.config.platformId:
        conversation = Conversation.query.filter(Conversation.id == roomId).first()
    else:
        conversation = Conversation.query.filter(Conversation.external_id == roomId, Conversation.platform_id == roomOriginalPlatformId).first()
    conversationId = conversation.id

    "busco sender id y user namme"
    platformId = Platform.query.filter(Platform.name == senderPlatform).first().id
    senderUser = User.query.filter(User.external_id == senderId, User.platform_id == platformId).first()
    user_id = senderUser.id
    senderName = senderUser.name

    "recipients son todos los usuarios de nuestra plataforma en esa conversacion"
    recipients = []

    for user in conversation.users:
        if user.platform_id == app.config.platformId:
            recipients.append(user)

    conversation_manager.log_message(user_id, text, conversationId, "text")
    setupAndSendEvent(recipients, 'uiTextMessage', {'msg': text}, senderName, conversationId, user_id)


def setupAndSendEvent(recipients, eventName, data, sender, conversationId, user_id):
    data['user_id'] = user_id
    data['from'] = sender
    data['conversationId'] = conversationId
    group = Conversation.query.filter(Conversation.id == conversationId).first().group
    if group:
        data['group'] = group.name
        data['group_id'] = group.id
    sendEventToRecipients(recipients, data, eventName)

def sendEventToRecipients(recipients, data, eventName):
    for user in recipients:
        if user.platform_id == app.config.platformId:
           socketio.emit(eventName, data, room=user.id, namespace='/chat')

