from flask import Blueprint, session, render_template
from flask_login import login_required

from werkzeug.utils import redirect

from app.appModel.models import Conversation, User
from app.mod_conversation import conversation_api, login_api
from app.mod_conversation.conversation_api import conversation_manager
from app.mod_conversation.login_api import login_manager
from app.mod_database import db

mod_chat = Blueprint('chat', __name__, url_prefix="/chat")


@mod_chat.route('/<user_id>', methods=['GET'])
@login_required
def chatWithUser(user_id):
    fromUser = session['user_id']
    if not login_manager.isAuthorized(fromUser):
        return redirect("auth/signin")

    toUser = user_id
    conversation = conversation_manager.startConversation(fromUser, toUser)

    return render_template("chat/chat.html",
                           chatTitle=conversation.toUser,
                           actual_user=conversation.fromUser,
                           recipientsList=[conversation.toUser,conversation.fromUser],
                           conversation=conversation)


# TODO
@mod_chat.route('/group/<group_id>', methods=['GET'])
@login_required
def chatWithGroup(group_id):
    actual_user = User.query.filter(User.id == session['user_id']).first()
    return
