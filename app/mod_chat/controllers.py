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
                           chatTitle=conversation.toUser,
                          #  actual_user=conversation.fromUser,
                           actual_user=current_user,
                           recipientsList=[conversation.toUser,conversation.fromUser],
                           conversation=conversation)


# TODO
@mod_chat.route('/group/<group_id>', methods=['GET'])
@login_required
def chatWithGroup(group_id):
    toGroup = Group.query.filter(Group.id == group_id).first()
    conversation = toGroup.conversation
    if not conversation:
        conversation = Conversation(group=toGroup)
        db.session.add(conversation)
        db.session.commit()

    return render_template("chat.html",
                           chatTitle=toGroup,
                           actual_user=current_user,
                           recipientsList=conversation.group.users,
                           conversation=conversation)