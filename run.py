# Run a test server.
import sys, argparse
from flask_socketio import SocketIO

from config import DEBUG, APP_PORT, APP_HOST, APP_NAME, APP_TOKEN
import config, os

# Parsing args
parser = argparse.ArgumentParser(
  description='Ejecuta un chat con el nombre y el puerto que le pases o \
  con el que figura en el archivo de configuación.')
parser.add_argument('-n', '--name', type=str, default=APP_NAME, required=False,
                    help='Un nombre para la app. Default BuasApp')
parser.add_argument('-p','--port', type=str, default=APP_PORT, required=False,
                    help='Un puerto para la app. Default {}'.format(APP_PORT))
parser.add_argument('-t','--token', type=str, default=APP_TOKEN, required=False,
                    help='El token de la app. Default {}'.format(APP_TOKEN))

args = parser.parse_args()

# Modifico el config
config.SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(config.BASE_DIR, '{}.db'.format(args.name))


# Inicializo la app con el config modificado
from app import app, socketio, login_manager
app.config.appName =  args.name
app.config.appToken = args.token

login_manager.init_app(app)
socketio.init_app(app)

from app.mod_api.integrator import importAll
importAll()


# IMPORTANTE: Si le quitan la opcion de use_reloader, lanza dos procesos y 
# eso hace que explote el importAll() porque deja 'abierta' la conexion (o algo asi).

socketio.run(app, host=APP_HOST, port=int(args.port), debug=DEBUG,
            log_output=True, ssl_context=('app/cert.pem', 'app/key.pem'),
            use_reloader=False)
