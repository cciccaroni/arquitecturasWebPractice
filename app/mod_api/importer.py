from app.appModel.models import *
from app.mod_api.internalMessenger import sendMessageToInternalUsers
from app.mod_conversation.conversation_api import conversation_manager
from app import socketio
from app import app
import requests
headers = {'content-type': 'application/json'}

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
        conversation_manager.startGroupConversation(group.id, platform_id= platformConversationOwnerId, external_id= id)


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
        sendMessageToInternalUsers(recipients, 'uiTextMessage', {'msg': text}, senderUser.name, conversation.id, senderUser.id)
        conversation_manager.log_message(senderUser.id, text, conversation.id, "text")


def savePlatform(platform):
    # chequear si la plataforma existe, sino agregarla con las keys
    p = Platform.query.filter(Platform.name == platform['name']).first()

    if p:
        return p.id

    newPlatform = Platform(
        platform['name'],
        'True' == platform['supportAudio'],
        'True' == platform['supportImage']
    )
    db.session.add(newPlatform)
    db.session.commit()
    app.logger.debug('New platform added... {} - {}'.format(newPlatform.id, newPlatform.name))

    return newPlatform.id


def initializePlatform():
    me = {
        'name': app.config.appName,
        'supportAudio': 'True',
        'supportImage': 'True'
    }

    app.config.platformId = savePlatform(me)

    print('myPlatformId', app.config.platformId)
    return


def importAll():
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'platforms'
    r = requests.get(url=endpoint, headers=headers, verify=False)

    if (not r.status_code == requests.codes.ok):
        app.logger.error('Error getting platforms: {}'.format(r.status_code))
        return

    platforms = r.json()['platforms']
    app.logger.debug('Importing platforms/users...\n{}'.format(platforms))
    for platform in platforms:
        savePlatform(platform)

        # No deberia poder devolver nuestra plataforma
        if platform['name'] == app.config.appName:
            continue

        addUsers(platform)
    return

def saveUser(user, platform):
    exists = User.query.filter(
        User.platform_id == platform['id'],
        User.external_id == user['id']
    ).first()
    if not exists:
        email = user['name'] + "@" + platform['name']
        newUser = User(user['name'], email, 'bla', platform['id'], user['id'])
        db.session.add(newUser)
        app.logger.debug('Adding user: {}'.format(newUser))
        db.session.commit()

def addUsers(platform):
    p = Platform.query.filter(Platform.name == platform['name']).first()

    if not p:
        return

    platform['id'] = p.id
    actuales = User.query.filter(User.platform_id == p.id)

    app.logger.debug('Adding users from platform {}'.format(platform['name']))
    app.logger.debug('Existent users: {}'.format([a for a in actuales]))
    for user in platform['users']:
        saveUser(user, platform)
    return



def getDestinationUsers(conversation):
    return [user for user in (conversation.users if (len(conversation.users) is not 0) else (
        conversation.group.users if (conversation.group is not None) else [])) if
            user.platform_id == app.config.platformId]

