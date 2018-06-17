from flask import Blueprint, session, render_template
from flask_login import login_required, current_user

from werkzeug.utils import redirect

from app.appModel.models import Conversation, User, Group
from app.mod_conversation.conversation_api import conversation_manager

from app.mod_database import db

mod_chat = Blueprint('chat', __name__, url_prefix='/chat', template_folder='../templates/chat')

@mod_chat.route('/<user_id>', methods=['GET'])
@login_required
def chatWithUser(user_id):
    fromUser = session['user_id']
    toUser = user_id
    conversation = conversation_manager.startConversation(fromUser, toUser)
    return render_template("chat.html",
                           chatTitle=conversation.title,
                           actual_user=current_user,
                           recipientsList=conversation.recipientList,
                           conversation=conversation,
                           imageAndAudioAvailable=not thereIsExternalUserIn(conversation))


def thereIsExternalUserIn(conversation):
    return any(
        User.query.filter(User.id == userdto.id).first().platform_id != 1 for userdto in conversation.recipientList)


# TODO
@mod_chat.route('/group/<group_id>', methods=['GET'])
@login_required
def chatWithGroup(group_id):

    conversation = conversation_manager.startGroupConversation(group_id)

    return render_template("chat.html",
                           chatTitle=conversation.title,
                           actual_user=current_user,
                           recipientsList=conversation.recipientList,
                           conversation=conversation,
                           imageAndAudioAvailable=not thereIsExternalUserIn(conversation))

