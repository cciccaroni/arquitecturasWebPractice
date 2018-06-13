from flask import Blueprint, jsonify, request, abort

from app.mod_api.integration_models import *

mod_api = Blueprint('api', __name__)


@mod_api.route('/api/users', methods=['GET'])
def getUsers():
    return jsonify({'users': getUsersJson()})

@mod_api.route('/api/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)
    id = request.json['id']
    name = request.json['name']
    platform = request.json['platform']
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
    return "success"
