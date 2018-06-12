from app.appModel.models import *

def getUsersJson():
    result = []
    users = User.query.filter(User.platform_id == 1)
    for user in users:
        result.append({'id': user.id, 'name': user.name})
    return result
