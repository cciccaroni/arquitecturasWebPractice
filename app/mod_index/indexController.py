# Import flask dependencies
from flask import Blueprint, request, render_template, \
                  flash, session, redirect
from jinja2 import nodes
from jinja2.ext import Extension

mod_index = Blueprint('index', __name__, url_prefix='/index')

@mod_index.route('/', methods=['GET'])
def index():
    if not 'user_id' in session or session['user_id'] == 0:
        return redirect("auth/signin")

    #de alguna forma llamar a la base y llenar este json
    user = {'username': 'Miguel'}
    conversations = [
        {
            'id': 1,
            'title': 'Conversacion con juan',
            'messages': [{ 'from' : {'name' : 'juan'}, 'message' : {'type' : 'text', 'text': 'hola'}}, { 'from' : {'name' : 'juan'}, 'message' : {'type' : 'text', 'text': 'hola2'}} ]
        },
        {
            'id': 2,
            'title': 'Conversacion con juan y pedro',
            'messages': [{ 'from' : {'name' : 'juan'}, 'message' : {'type' : 'text', 'text': 'hola'}}, { 'from' : {'name' : 'pedro'}, 'message' : {'type' : 'text', 'text': 'hola2'}} ]

        }
    ]
    return render_template('index/index.html', title='Home', user=user, conversations=conversations)

