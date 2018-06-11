# Import flask and template operators
import os
from flask import Flask, render_template, send_from_directory, current_app


# Define the WSGI application object
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
# with app.app_context():
#     current_app.config.appName = "BuatsApp"
    
socketio = SocketIO(engineio_logger=True)

# Login Manager configuration.
login_manager = LoginManager()
login_manager.login_view = '/auth/signin/'

# Configurations
app.config.from_object('config')
# app.config.appName = "BuatsApp"

# Browser static (os) favicon
@app.route('/img/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# Sample HTTP error handling
@app.errorhandler(404)
def not_found(error):
    return render_template('auth/404.html'), 404

#init db
from app.mod_database.database import init_db
from app.appModel.models import *
init_db()


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module
from app.mod_list.controllers import mod_list
from app.mod_chat.controllers import mod_chat
from app.mod_group.controllers import mod_group
from app.mod_api.controllers import mod_api
# Register blueprint(s)
app.register_blueprint(auth_module)
app.register_blueprint(mod_list)
app.register_blueprint(mod_chat)
app.register_blueprint(mod_group)
app.register_blueprint(mod_api)
# app.register_blueprint(xyz_module)
# ..
