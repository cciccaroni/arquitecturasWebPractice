from app.appModel.models import *
from app import app
import json
import requests
from app.mod_database import db
from flask_login import login_user, logout_user, current_user
import logging

headers = {'content-type': 'application/json'}


def initializePlatform():
    me = {
      'name': app.config.appName, 
      'supportAudio': 'True', 
      'supportImage': 'True'
    }
    
    app.config.platformId = addPlatform(me)
    
    print('myPlatformId', app.config.platformId)
    return

def importAll():
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'platforms'
    r = requests.get(url=endpoint, headers=headers, verify=False)

    if(not r.status_code == requests.codes.ok):
        app.logger.error('Error getting platforms: {}'.format(r.status_code))
        return

    platforms = r.json()['platforms']
    app.logger.debug('Importing platforms/users...\n{}'.format(platforms))
    for platform in platforms:
        addPlatform(platform)
        
        # No deberia poder devolver nuestra plataforma
        if platform['name'] == app.config.appName:
          continue
        
        addUsers(platform)
        deleteUsers(platform) 
    return


def addPlatform(platform):
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


def addUsers(platform):
    p = Platform.query.filter(Platform.name == platform['name']).first()
    actuales = User.query.filter(User.platform_id == p.id)

    app.logger.debug('Adding users from platform {}'.format(p.name))
    app.logger.debug('Existent users: {}'.format([a for a in actuales]))
    for user in platform['users']:
        exists = User.query.filter(
            User.platform_id == p.id,
            User.external_id == user['id']
        ).first()
        if not exists:
            # TODO: Ver si las demas plataformas pueden exportar email
            email = user['name'] + "@" + platform['name']
            newUser = User(user['name'], email, 'bla', p.id, user['id'])
            db.session.add(newUser)
            app.logger.debug('Adding user: {}'.format(newUser))
    db.session.commit()
    return


def deleteUsers(platform):
    # Borrar localmente todos los usuarios que ya no existen en sus plataforms
    p = Platform.query.filter(Platform.name == platform['name']).first()
    savedPlatformUsers = User.query.filter(User.platform_id == p.id).all()
    ids = [element['id'] for element in platform['users']]
    for user in savedPlatformUsers:
        if user.external_id not in ids:
            # TODO: borrar en cascada a las tablas donde figure el user_id
            db.session.delete(user)
            app.logger.debug('Deleting user: {}'.format(user))
    db.session.commit()
    return


def exportUser(user):
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'user'
    jsonUser = {"id": user.id, "name": user.name, "token": app.config.appToken}
    app.logger.debug('Exporting new user: {} | {}'.format(user, jsonUser))
    r = requests.post(url=endpoint, headers=headers,
                      data=json.dumps(jsonUser), verify=False)
    return


def exportConversation(conversationId, fromUser, toUser):
    toPlatform = Platform.query.filter(Platform.id == toUser.platform_id).first().name
    users = [
                {app.config.appName: [fromUser.id]},
                {toPlatform: [toUser.external_id]}
            ]
    room = createJsonRoom(
                              conversationId, 
                              " - ".join([fromUser.name, toUser.name]), 
                              "private", 
                              users
                          )
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'room'
    r = requests.post(url=endpoint, headers=headers,
                      data=json.dumps(room), verify=False)
    return

def exportMessage(data):
    conversation = Conversation.query.filter(Conversation.id == data['conversationId']).first()
    platformOriginalId = conversation.platform_id
    if(platformOriginalId == 1):
        originalRoomPlatform = app.config.appName
        roomId = data['conversationId']
    else:
        originalRoomPlatform = Platform.query.filter(
            Platform.id == platformOriginalId).first().name
        roomId = conversation.external_id

    senderId = data['user_id']
    text = data['msg']
    token = app.config.appToken

    message = {"roomOriginalPlatform": originalRoomPlatform,
               "roomId": roomId, "senderId": senderId, "text": text, "token": token}
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'message'
    r = requests.post(url=endpoint, headers=headers,
                      data=json.dumps(message), verify=False)
    return

def createJsonRoom(id, name, type, users):
    return {"id": id, "name": name, "token":  app.config.appToken, "type": type, "users": users}
