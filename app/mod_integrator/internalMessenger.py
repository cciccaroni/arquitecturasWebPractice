from app.appModel.models import *
from app import socketio
from app import app


def sendMessageToInternalUsers(recipients, eventName, data, sender, conversationId, user_id):
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