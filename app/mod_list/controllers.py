from flask import Blueprint, session, render_template
from werkzeug.utils import redirect

from app import db
from app.appModel.models import User, Group
from flask_login import login_required

mod_list = Blueprint('list', __name__)


@mod_list.route('/', methods=['GET'])
@login_required
def chat():
    actual_user = User.query.filter(User.id == session['user_id']).first()
    if actual_user:
        return render_template("contacts/list.html", 
                                users=User.query.filter(User.id != actual_user.id).all(),
                                actual_user=actual_user,
                                groups=Group.query.filter(Group.users.any(User.id == actual_user.id)).all())
    
    return redirect("auth/signin")
