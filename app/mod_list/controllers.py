from flask import Blueprint, render_template
from werkzeug.utils import redirect

from app import db
from app.appModel.models import User, Group
from flask_login import login_required, current_user

from app.mod_group.forms import CreateGroupForm

mod_list = Blueprint('list', __name__, template_folder='../templates/contacts')

@mod_list.route('/', methods=['GET'])
@login_required
def chat():
    friends = User.query.filter(User.id != current_user.id).all()
    form = CreateGroupForm()
    print(form.name)
    form.set_members(friends)

    return render_template('list.html', 
                            form=form,
                            users=friends,
                            actual_user=current_user,
                            groups=Group.query.filter(Group.users.any(User.id == current_user.id)).all())
