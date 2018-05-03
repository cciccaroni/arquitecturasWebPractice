from flask import Blueprint, session, render_template
from flask_login import login_required

from werkzeug.utils import redirect

from app.appModel.models import Conversation, User, Group
from app.mod_conversation.conversation_api import conversation_manager
# from app.mod_conversation.login_api import login_manager
from app.mod_database import db

mod_chat = Blueprint('chat', __name__, url_prefix="/chat")


@mod_chat.route('/<user_id>', methods=['GET'])
@login_required
def chatWithUser(user_id):
    fromUser = session['user_id']
    # ESTO no deberia ser necesario con el login_required.
    # if not login_manager.isAuthorized(fromUser):
    #     return redirect("auth/signin")

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
    fromUserID = session['user_id']
    # ESTO no deberia ser necesario con el login_required.
    # if not login_manager.isAuthorized(fromUser):
    #     return redirect("auth/signin")

    fromUser = User.query.filter(User.id == fromUserID).first()
    toGroup = Group.query.filter(Group.id == group_id).first()
    conversation = toGroup.conversation
    if not conversation:
        conversation = Conversation(group=toGroup)
        db.session.add(conversation)
        db.session.commit()


    return render_template("chat/chat.html",
                           chatTitle=toGroup,
                           actual_user=fromUser,
                           recipientsList=conversation.group.users,
                           conversation=conversation)