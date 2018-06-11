# Run a test server.
import sys, argparse
from flask_socketio import SocketIO

from app import app, socketio, login_manager
from config import DEBUG, APP_PORT, APP_HOST, APP_NAME

# Parsing args
parser = argparse.ArgumentParser(
  description='Ejecuta un chat con el nombre y el puerto que le pases o \
  con el que figura en el archivo de configuación.')
parser.add_argument('-n', '--name', type=str, default=APP_NAME, required=False,
                    help='Un nombre para la app. Default BuasApp')
parser.add_argument('-p','--port', type=str, default=APP_PORT, required=False,
                    help='Un puerto para la app. Default {}'.format(APP_PORT))
args = parser.parse_args()

app.config.appName =  args.name

login_manager.init_app(app)
socketio.init_app(app)

socketio.run(app, host=APP_HOST, port=args.port, debug=DEBUG, 
            log_output=True, ssl_context=('app/cert.pem', 'app/key.pem'))
