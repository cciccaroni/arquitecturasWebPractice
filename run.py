# Run a test server.
from flask_socketio import SocketIO

from app import app, socketio, login_manager
from config import DEBUG, APPLICATION_PORT

login_manager.init_app(app)
socketio.init_app(app)

socketio.run(app, host='0.0.0.0', port=APPLICATION_PORT, debug=DEBUG, log_output=True, ssl_context=('app/cert.pem', 'app/key.pem'))
