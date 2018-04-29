# Run a test server.
from flask_socketio import SocketIO

from app import app, socketio

socketio.run(app, host='127.0.0.1', port=8080, debug=True)
