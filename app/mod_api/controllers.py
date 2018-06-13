from flask import Blueprint, jsonify, request, abort
from app.mod_api.integration_models import *
from app import socketio
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
    "guardar el mensaje en la base"
    dataForSocket = saveAndSendMessageToInternalUsers(roomOriginalPlatform, roomId, senderId, senderPlatform, text);

    "TODO: mandar un socket a los clientes, no estoy pudiendo hacerlo desde aca porque no estoy dentro de un event handler de socket io." \
    "hay que buscar la forma. en dataForSocket junto con la variable text tengo todos los datos que necesito para poder llama a la funcion setupAndSendEvent " \
    "que esta en chatEvents.py, pero no funciona porque no estamos en el contexto de socket io"

    return "success"



