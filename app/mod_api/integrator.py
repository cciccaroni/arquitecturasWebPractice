from app.appModel.models import *
from app import app
import json
import requests
from app.mod_database import db
from flask_login import login_user, logout_user, current_user
import logging
from flask_socketio import emit

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

def addUser(user, platform):
    exists = User.query.filter(
        User.platform_id == platform['id'],
        User.external_id == user['id']
    ).first()
    if not exists:
        # TODO: Ver si las demas plataformas pueden exportar email
        email = user['name'] + "@" + platform['name']
        newUser = User(user['name'], email, 'bla', platform['id'], user['id'])
        db.session.add(newUser)
        app.logger.debug('Adding user: {}'.format(newUser))
        db.session.commit()
        us = User.query.all()
        for u in us:
            if u.id != u.id:
                if u.platform_id == app.config.platformId:
                    emit('newUser', newUser, room=u.id)

def addUsers(platform):
    p = Platform.query.filter(Platform.name == platform['name']).first()
    
    if not p:
        return
    
    platform['id'] = p.id
    actuales = User.query.filter(User.platform_id == p.id)

    app.logger.debug('Adding users from platform {}'.format(platform['name']))
    app.logger.debug('Existent users: {}'.format([a for a in actuales]))
    for user in platform['users']:
        addUser(user, platform)
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
    r = requests.post(url=endpoint, headers=headers,
                      data=json.dumps(jsonUser), verify=False)
    app.logger.debug('New user exported: {} :: {} :: {}'.format(jsonUser, endpoint, r))
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
    app.logger.debug('Conversation exported {}::{}::{}'.format(room, endpoint, r))
    return

def exportMessage(data):
    conversation = Conversation.query.filter(Conversation.id == data['conversationId']).first()
    platformOriginalId = conversation.platform_id
    app.logger.debug('Exporting msg')
    
    if(platformOriginalId == app.config.platformId):
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
    app.logger.debug('Msg exported {}::{}::{}'.format(message, endpoint, r))
    return

def createJsonRoom(id, name, type, users):
    return {"id": id, "name": name, "token":  app.config.appToken, "type": type, "users": users}



def exportGroup(group, conversation):
    users = group.users
    platforms = Platform.query.all()
    groupUsers = []

    for platform in platforms:
        if platform.name == app.config.appName:
            platformUsers = []
            for user in users:
                if user.platform_id == platform.id:
                    platformUsers.append(user.id)
            groupUsers.append({ platform.name : platformUsers})
        else:
            platformUsers = []
            for user in users:
                if user.platform_id == platform.id:
                    platformUsers.append(user.external_id)
            groupUsers.append({ platform.name : platformUsers})


    room = createJsonRoom(
                          conversation.id,
                          group.name,
                          "public",
                          groupUsers
                      )

    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'room'
    r = requests.post(url=endpoint, headers=headers,
                      data=json.dumps(room), verify=False)
    app.logger.debug('Group exported {}::{}::{}'.format(room, endpoint, r))
    return
