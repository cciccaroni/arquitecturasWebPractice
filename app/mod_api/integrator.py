from app.appModel.models import *
from app import app
import json
import requests
from app.mod_database import db
from flask_login import login_user, logout_user, current_user

headers = {'content-type': 'application/json'}

def importAll():
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'platforms'
    r = requests.get(url=endpoint, headers=headers, verify=False)

    if(not r.status_code == requests.codes.ok):
      return
    
    platforms = r.json()['platforms']
    for platform in platforms:
        if not platform['name'].lower() == app.config.appName.lower():
            addPlatform(platform)
            addUsers(platform)
            deleteUsers(platform)


def addPlatform(platform):
    #chequear si la plataforma existe, sino agregarla con las keys
    exists = Platform.query.filter(Platform.name == platform['name']).first()
    if not exists:
        newPlatform = Platform(platform['name'], 'True' == platform['supportAudio'], 'True' == platform['supportImage'])
        db.session.add(newPlatform)
        db.session.commit()

def addUsers(platform):
    platformId = Platform.query.filter(Platform.name == platform['name']).first().id
    for user in platform['users']:
        exists = User.query.filter(User.platform_id == platformId, User.external_id == user['id']).first()
        if not exists:
            #todo: sacar este mail hardcodeado y ver si las demas plataformas pueden exportar email
            email = user['name'] + "@" + platform['name']
            newUser = User(user['name'], email, 'bla', platformId, user['id'])
            db.session.add(newUser)
    db.session.commit()

def deleteUsers(platform):
    #quiero borrar todos los usuarios en mi base que ya no estan en los usuarios de la plataforms
    platformId = Platform.query.filter(Platform.name == platform['name']).first().id
    savedPlatformUsers =  User.query.filter(User.platform_id == platformId).all()
    ids = [element['id'] for element in platform['users']]
    for user in savedPlatformUsers:
        if user.external_id not in ids:
            #todo: borrar en cascada a las tablas donde figure el user_id
            db.session.delete(user)
    db.session.commit()

def exportUser(user):
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'user'
    jsonUser = { "id" : user.id, "name" : user.name, "token": app.config.appToken}
    r = requests.post(url=endpoint, headers=headers, data=json.dumps(jsonUser), verify=False)

def exportConversation(conversationId, fromUser, toUser):
    toPlatform = Platform.query.filter(Platform.id == toUser.platform_id).first().name
    users = [{ app.config.appName : [fromUser.id]}, {toPlatform : [toUser.external_id]}]
    room = createJsonRoom(conversationId, fromUser.name + " - " + toUser.name, "private", users)
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'room'
    r = requests.post(url=endpoint, headers=headers, data=json.dumps(room), verify=False)
    a = 'a'

def exportMessage(data):
    conversation = Conversation.query.filter(Conversation.id == data['conversationId']).first()
    platformOriginalId = conversation.platform_id
    if(platformOriginalId == 1):
        originalRoomPlatform = app.config.appName
        roomId = data['conversationId']
    else:
        originalRoomPlatform = Platform.query.filter(Platform.id == platformOriginalId).first().name
        roomId = conversation.external_id

    senderId = data['user_id']
    text = data['msg']
    token = app.config.appToken

    message = { "roomOriginalPlatform": originalRoomPlatform, "roomId": roomId, "senderId": senderId, "text": text, "token": token}
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'message'
    r = requests.post(url=endpoint, headers=headers, data=json.dumps(message), verify=False)

def createJsonRoom(id, name, type, users):
    return { "id" : id, "name" : name, "token" :  app.config.appToken, "type": type, "users" : users}

