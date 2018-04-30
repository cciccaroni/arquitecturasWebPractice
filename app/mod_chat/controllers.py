from flask import Blueprint, request, session, render_template
from werkzeug.utils import redirect

from app.appModel.models import Conversation, User
from app.mod_database import db

mod_chat = Blueprint('chat', __name__, url_prefix="/chat")


@mod_chat.route('/<user_id>', methods=['GET'])
def chat(user_id):
    actual_user = User.query.filter(User.id == session['user_id']).first()
    if not actual_user:
      return redirect("auth/signin")

    adressee_user = User.query.filter(User.id == user_id).first()
    conversations = actual_user.conversations
    users_have_conversation = len(list(filter(lambda conversation: actual_user in conversation.users and adressee_user in conversation.users, conversations))) > 0
    if not users_have_conversation:
        conversation = Conversation([actual_user, adressee_user])
        db.session.add(conversation)
        db.session.commit()


    return render_template("chat/chat.html", adressee=adressee_user, actual_user = actual_user)

