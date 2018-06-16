from app.appModel.models import *
from app import app
import requests

from app.mod_api.importsSaver import savePlatform
from app.mod_database import db
from flask_socketio import emit

headers = {'content-type': 'application/json'}


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