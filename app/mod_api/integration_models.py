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


        fromUser = User.query.filter(User.external_id == fromUserId, User.platform_id == fromPlatformId).first()
        toUser = User.query.filter(User.id == toUserId).first()


        conversation = Conversation(users=[fromUser, toUser], platform_id = fromPlatformId, external_id= id)
        db.session.add(conversation)
        db.session.flush()
        db.session.commit()
    elif type == "public":#"crear el grupo. Se asume que existen todos los usuarios.."
        conversationUserList = []
        for usersFromPlatform in users:
            for platform in usersFromPlatform:
                fromPlatformId = Platform.query.filter(Platform.name == platform).first().id
                for userId in usersFromPlatform[platform]:
                    if app.config.appName == platform:#id de usuario de mi app
                        ownUser = User.query.filter(User.id == userId).first()
                        conversationUserList.append(ownUser)
                    else:#id de usuario externo
                        externalUser = User.query.filter(User.external_id == userId, User.platform_id == fromPlatformId).first()
                        conversationUserList.append(externalUser)
        group = Group(name, conversationUserList)
        db.session.add(group)
        db.session.flush()
        db.session.commit()
        platformConversationOwnerId = Platform.query.filter(Platform.name == platformName).first().id
        conversation = conversation_manager.startGroupConversation(group.id, platform_id= platformConversationOwnerId, external_id= id)





def saveAndSendMessageToInternalUsers(roomOriginalPlatform, roomId, senderId, senderPlatform, text):
    roomOriginalPlatformId = Platform.query.filter(Platform.name == roomOriginalPlatform).first().id
    if roomOriginalPlatformId == app.config.platformId:
        conversation = Conversation.query.filter(Conversation.id == roomId).first()
    else:
        conversation = Conversation.query.filter(Conversation.external_id == roomId, Conversation.platform_id == roomOriginalPlatformId).first()

    if conversation is None:
       return

    platformId = Platform.query.filter(Platform.name == senderPlatform).first().id
    senderUser = User.query.filter(User.external_id == senderId, User.platform_id == platformId).first()
    recipients = getDestinationUsers(conversation)
    if len(recipients) is not 0:
        setupAndSendEvent(recipients, 'uiTextMessage', {'msg': text}, senderUser.name, conversation.id, senderUser.id)
        conversation_manager.log_message(senderUser.id, text, conversation.id, "text")


def getDestinationUsers(conversation):
    return [user for user in (conversation.users if (len(conversation.users) is not 0) else (
        conversation.group.users if (conversation.group is not None) else [])) if
            user.platform_id == app.config.platformId]


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

