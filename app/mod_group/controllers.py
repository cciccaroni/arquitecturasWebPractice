from flask import Blueprint, render_template, request, json
from werkzeug.utils import redirect

from app import db
from app.appModel.models import User, Group
from flask_login import login_required, current_user

mod_group = Blueprint('group', __name__)

@mod_group.route('/addGroup', methods=['POST'])
@login_required
def addGroup():
    a=1
    # jsonData = json.loads(request.get_json())
    # return render_template('list.html',
    #                         users=User.query.filter(User.id != current_user.id).all(),
    #                         actual_user=current_user,
    #                         groups=Group.query.filter(Group.users.any(User.id == current_user.id)).all())
