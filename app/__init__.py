# Import flask and template operators
import os
from flask import Flask, render_template, send_from_directory

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')


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
init_db()


# Import a module / component using its blueprint handler variable (mod_auth)
from app.mod_auth.controllers import mod_auth as auth_module

# Register blueprint(s)
app.register_blueprint(auth_module)
# app.register_blueprint(xyz_module)
# ..
