from flask import Blueprint, request, session, render_template

from app.appModel.models import Conversation, User

mod_chat = Blueprint('chat', __name__, url_prefix="/chat")


@mod_chat.route('/<user_id>', methods=['GET'])
def chat(user_id):
    actual_user = User.query.filter(User.id == session['user_id']).first()
    adressee_user = User.query.filter(User.id == user_id).first()
    if not actual_user.conversations:
        conversation = Conversation()
        actual_user.addConversation(conversation)
        adressee_user.addConversation(conversation)


    return render_template("chat/chat.html", adressee=adressee_user)
