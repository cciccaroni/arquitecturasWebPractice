from flask import Flask, request
from flask_socketio import SocketIO, send, emit
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)
users = {}

@socketio.on('new user')
def handleNewUser(jsonUser):
	users[(json.loads(json.dumps(jsonUser))['name'])] = request.sid;
	emit('new user', list(users.keys()), broadcast=True)
	print('new user: ' + str(jsonUser))

@socketio.on('new message')
def handle_my_custom_event(jsonMessage):
	print('received json: ' + str(jsonMessage))
	print('session: ' + request.sid)
	send(str(json.loads(json.dumps(jsonMessage))), broadcast=True, room=users[(json.loads(json.dumps(jsonMessage))['to'])
] )

if __name__ == '__main__':
	socketio.run(app)
