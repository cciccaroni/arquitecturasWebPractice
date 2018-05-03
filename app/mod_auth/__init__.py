from app.appModel.models import *
from app import login_manager

class LoggedUser():
    '''
      This class is used to represent logged users.
    '''
    def __init__(self, user):
          #: A factory function that produces an user representation 
          #: which is stored in current_user when someone is logged in.
          self.name = user.name
          self.email = user.email
          self.id = user.id
    
    def is_authenticated(self):
        #: This property should return True if the user is authenticated
        #: Only authenticated users will fulfill the criteria of login_required
        return True

    def is_active(self):
        #: This property should return True if this is an active user - in 
        #: addition to being authenticated, they also have activated their 
        #: account. Inactive accounts may not log in.
        return True

    def is_anonymous(self):
        #: This property should return True if this is an anonymous user.
        return False

    def get_id(self):
        #: This method must return a unicode that uniquely identifies this 
        #: user. It can be used to load the user from the user_loader callback.
        return self.id

@login_manager.user_loader
def user_loader(user_id):
    '''
      This sets the callback for reloading a user from the session. 
      The function you set should take a user ID (a unicode) and 
      return a user object, or None if the user does not exist.
    '''
    user = User.query.filter_by(id=user_id).first()
    return None if not user else LoggedUser(user)