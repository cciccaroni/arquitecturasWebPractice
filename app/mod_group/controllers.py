from flask import Blueprint, render_template, request, json
from werkzeug.utils import redirect

from app import db, app
from app.appModel.models import User, Group
from flask_login import login_required, current_user

from app.mod_integrator.exporter import exportGroup
from app.mod_conversation.conversation_api import conversation_manager
#to decode form data
import unicodedata

# Import module forms
from app.mod_group.forms import CreateGroupForm

mod_group = Blueprint('group', __name__)

@mod_group.route('/addGroup', methods=['POST'])
@login_required
def addGroup():
    friends = User.query.filter(User.id != current_user.id).all()
    form = CreateGroupForm(request.form)
    form.set_members(friends)
    
    if form.validate_on_submit():
        name = form.name.data
        members = form.members.data + [current_user.id]
        users = User.query.filter(User.id.in_(members)).all()

        if len(users)>1:
          group = Group(name, users)
          db.session.add(group)
          db.session.flush()
          db.session.commit()
          conversation = conversation_manager.startGroupConversation(group.id)
          thereIsAnExternalUser = False
          for user in users:
              if user.platform_id != app.config.platformId:
                  thereIsAnExternalUser = True

          if thereIsAnExternalUser:
              exportGroup(group, conversation)


          return redirect('/?tab=grupos')


    return render_template('list.html',
                            active_tab= 'grupos',
                            users=friends,
                            actual_user=current_user,
                            groups=Group.query.filter(Group.users.any(User.id == current_user.id)).all(),
                            form=form)



