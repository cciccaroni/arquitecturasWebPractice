from app.appModel.models import *

class LoginManager:
    def isAuthorized(self,user):
        return User.query.filter(User.id == user).first() is not None


login_manager = LoginManager()
