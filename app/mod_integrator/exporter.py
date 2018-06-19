from app.appModel.models import *
from app import app
import json
import grequests

headers = {'content-type': 'application/json'}


def exportUser(user):
    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'user'
    jsonUser = {"id": user.id, "name": user.name, "token": app.config.appToken}
    grequests.map([grequests.post(endpoint, data=json.dumps(jsonUser), headers=headers, verify=False)])
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
    grequests.map([grequests.post(endpoint, data=json.dumps(room), headers=headers, verify=False)])
    return


def exportMessage(data):
    conversation = Conversation.query.filter(Conversation.id == data['conversationId']).first()
    platformOriginalId = conversation.platform_id
    app.logger.debug('Exporting msg')

    if (platformOriginalId == app.config.platformId):
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

    grequests.map([grequests.post(endpoint, data=json.dumps(message), headers=headers, verify=False)])
    return

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
            groupUsers.append({platform.name: platformUsers})
        else:
            platformUsers = []
            for user in users:
                if user.platform_id == platform.id:
                    platformUsers.append(user.external_id)
            groupUsers.append({platform.name: platformUsers})

    room = createJsonRoom(
        conversation.id,
        group.name,
        "public",
        groupUsers
    )

    endpoint = app.config['INTEGRATION_ENDPOINT'] + 'room'

    grequests.map([grequests.post(endpoint, data=json.dumps(room), headers=headers, verify=False)])
    return

def exportUsers():
    result = []
    users = User.query.filter(User.platform_id == 1)
    for user in users:
        result.append({'id': user.id, 'name': user.name, 'platform': app.config.appName})
    app.logger.debug('Returning users.\n {}'.format(result))
    return result

def createJsonRoom(id, name, type, users):
    return {"id": id, "name": name, "token": app.config.appToken, "type": type, "users": users}
