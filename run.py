# Run a test server.
from flask_socketio import SocketIO

from app import app, socketio, login_manager

login_manager.init_app(app)
socketio.init_app(app)

socketio.run(app, host='0.0.0.0', port=8080, debug=True, log_output=True)
