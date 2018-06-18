from flask import Blueprint, render_template
from werkzeug.utils import redirect

from app import db
from app.appModel.models import User, Group, Platform
from flask_login import login_required, current_user

from app.mod_group.forms import CreateGroupForm
from app.mod_list.listModels import friends

mod_list = Blueprint('list', __name__, template_folder='../templates/contacts')

@mod_list.route('/', methods=['GET'])
@login_required
def chat():
    myFriends = friends(current_user.id)
    form = CreateGroupForm()
    form.set_members(myFriends)



    return render_template('list.html',
                            active_tab= 'usuarios',
                            form=form,
                            users=myFriends,
                            actual_user=current_user,
                            groups=Group.query.filter(Group.users.any(User.id == current_user.id)).all())
