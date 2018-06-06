from flask import Blueprint, jsonify, request, abort

mod_api = Blueprint('api', __name__)

users = [
    {
        'id': 1,
        'name': u'pablo'
    },
    {
        'id': 2,
        'name': u'ivan'
    },
    {
        'id': 3,
        'name': u'christian'
    },
    {
        'id': 4,
        'name': u'gustavo'
    },
    {
        'id': 5,
        'name': u'marcelo'
    }
]


@mod_api.route('/api/users', methods=['GET'])
def getUsers():
    return jsonify({'users': users})

@mod_api.route('/api/user', methods=['POST'])
def new_user():
    if not request.json:
        abort(400)
    id = request.json['id']
    name = request.json['name']
    platform = request.json['platform']
    return "success"

@mod_api.route('/api/room', methods=['POST'])
def new_room():
    if not request.json:
        abort(400)
    users = request.json['users']
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