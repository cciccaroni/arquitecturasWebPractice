from app.appModel.models import User, Group, Platform

def friends(currentUserId):
    platforms = Platform.query.all()
    allUsers = User.query.filter(User.id != currentUserId).all()
    for user in allUsers:
        for platform in platforms:
            if user.platform_id == platform.id:
                user.platformName = platform.name

    return allUsers
