from flask import Blueprint, session, render_template
from werkzeug.utils import redirect

from app.appModel.models import Conversation, User
from app.mod_conversation import conversation_api, login_api
from app.mod_conversation.conversation_api import conversation_manager
from app.mod_conversation.login_api import login_manager
from app.mod_database import db

mod_chat = Blueprint('chat', __name__, url_prefix="/chat")


@mod_chat.route('/<user_id>', methods=['GET'])
def chat(user_id):
    fromUser = session['user_id']
    if not login_manager.isAuthorized(fromUser):
      return redirect("auth/signin")

    toUser = user_id

    conversation = conversation_manager.startConversation(fromUser, toUser)

    return render_template("chat/chat.html", adressee=conversation.toUser, actual_user=conversation.fromUser,messages = conversation.messages)

