from app.appModel.models import *
from app import app
import json
import requests
from app.mod_database import db

headers = {'content-type': 'application/json'}

def importAll():
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'platforms'
    r = requests.get(url=endpoint, headers=headers, verify=False)

    if(not r.status_code == requests.codes.ok):
      return
    
    platforms = r.json()['platforms']
    for platform in platforms:
        if not platform['name'] == app.config.appName:
            addPlatform(platform)
            addUsers(platform)


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