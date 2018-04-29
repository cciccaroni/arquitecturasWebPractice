from flask import Flask, request
from flask_socketio import SocketIO, send, emit
import json

socketIOApp = Flask(__name__)
socketIOApp.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(socketIOApp)
users = {}

@socketio.on('joined')
def handleNewUser(name):
	users[str(name)] = request.sid;
	emit('new user', list(users.keys()), broadcast=True)
	print('new user: ' + str(name))

@socketio.on('text')
def handle_my_custom_event(jsonMessage):
    print('received json: ' + str(jsonMessage))
    print('session: ' + request.sid)
    send(str(json.loads(json.dumps(jsonMessage))), broadcast=True, room=users[(json.loads(json.dumps(jsonMessage))['to'])] )

if __name__ == '__main__':
	socketio.run(socketIOApp)
