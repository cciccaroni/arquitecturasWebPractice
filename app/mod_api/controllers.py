from flask import Blueprint, jsonify, request, abort
from app.mod_api.integration_models import saveExternalUser, saveExternalConversation, saveAndSendMessageToInternalUsers, getUsersJson
from app import socketio
from app import app
import logging

mod_api = Blueprint('api', __name__)



@mod_api.route('/api/users', methods=['GET'])
def getUsers():
    users = getUsersJson()
    app.logger.debug('Returning users.\n {}'.format(users))
    return jsonify({'users': users})

@mod_api.route('/api/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)
    id = request.json['id']
    name = request.json['name']
    platform = request.json['platform']
    app.logger.debug('New user received. {}-{}-{}'.format(id, name, platform))
    saveExternalUser(id, name, platform)
    return "success"

@mod_api.route('/api/room', methods=['POST'])
def new_room():
    if not request.json:
        abort(400)

    users = request.json['users']
    id  = request.json['id']
    name =  request.json['name']
    platform = request.json['platform']
    type = request.json['type']
    saveExternalConversation(id, name, platform, type, users);
    return "success"

@mod_api.route('/api/message', methods=['POST'])
def new_message():
    if not request.json:
        abort(400)
    roomOriginalPlatform = request.json['roomOriginalPlatform']
    roomId = request.json['roomId']
    senderId = request.json['senderId']
    senderPlatform = request.json['senderPlatform']
    text = request.json['text']
    "guardar el mensaje en la base y forwardear. no anda la parte del forwardear"
    saveAndSendMessageToInternalUsers(roomOriginalPlatform, roomId, senderId, senderPlatform, text);
    return "success"



