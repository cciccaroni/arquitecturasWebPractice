from flask import Blueprint, render_template, request, json
from werkzeug.utils import redirect

from app import db
from app.appModel.models import User, Group
from flask_login import login_required, current_user

from wtforms.validators import ValidationError

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
        name = unicodedata.normalize('NFKD', form.name.data).encode('ascii', 'ignore')
        members = form.members.data + [current_user.id]
        users = User.query.filter(User.id.in_(members)).all()

        if len(users)>1:
          group = Group(name, users)
          db.session.add(group)
          db.session.commit()
          return redirect('/')
        
        # TODO: Add a custom validation to the members field of the form
        # raise ValidationError('Have you selected enough members to the group?')

    return render_template('list.html',
                            users=friends,
                            actual_user=current_user,
                            groups=Group.query.filter(Group.users.any(User.id == current_user.id)).all(),
                            form=form)
