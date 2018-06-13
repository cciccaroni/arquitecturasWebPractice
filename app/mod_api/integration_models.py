from app.appModel.models import *
from app.mod_conversation.conversation_api import conversation_manager
from app import app
from flask_socketio import SocketIO

import functools



def getUsersJson():
    result = []
    users = User.query.filter(User.platform_id == 1)
    for user in users:
        result.append({'id': user.id, 'name': user.name})
    return result

def saveExternalUser(id, name, platformName):
    platform = Platform.query.filter(Platform.name == platformName).first()
    if platform:
        email = name + "@" + platformName
        _user = User(name, email, 'bla', platform.id, id)
        db.session.add(_user)
        db.session.flush()
        db.session.commit()

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
        if user.platform_id == 1:
            recipients.append(user.id)

    conversation_manager.log_message(user_id, text, conversationId, "text")
    return {"recipients": recipients, "senderName" : senderName, "conversationId" : conversationId, "user_id" : user_id}

    #setupAndSendEvent(recipients, 'uiTextMessage', {'msg': text}, senderName, conversationId, user_id)

