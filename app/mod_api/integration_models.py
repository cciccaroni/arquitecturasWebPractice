from app.appModel.models import *

def getUsersJson():
    result = []
    users = User.query.filter(User.platform_id == 1)
    for user in users:
        result.append({'id': user.id, 'name': user.name})
    return result

def saveExternalUser(id, name, platformName):
    platform = Platform.query.filter(Platform.name == platformName).first()
    if platform:
        email = name + "@" + platformName
        newUser = User(name, email, 'bla', platform.id, id)
        db.session.add(newUser)
        db.session.commit()


