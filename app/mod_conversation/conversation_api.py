from app.appModel.models import *

class UserDTO:
    def __init__(self, userID):
        self.id = userID
        self.name = User.query.filter(User.id == userID).first().name

class MessageDTO:
    def __init__(self, fromUserID,message):
        self.fromUser = UserDTO(fromUserID)
        self.message = message


class ConversationDTO:
    def __init__(self, conversation,fromUserID,toUserID):
        self.id = conversation.id
        self.fromUser = UserDTO(fromUserID)
        self.toUser = UserDTO(toUserID)
        self.messages = map(lambda message: MessageDTO(message),list(conversation.messages))


class EmptyConversationDTO(object):
    def __init__(self, conversation,fromUserID, toUserID):
        self.id = conversation.id
        self.fromUser = UserDTO(fromUserID)
        self.toUserName = UserDTO(toUserID)
        self.messages = []


class ConversationManager(object):
    def __init__(self, db):
        self.db = db
        self.users = User.__table__

    def startConversation(self, fromUserID, toUserID):
        fromUser = User.query.filter(User.id == fromUserID).first()
        toUser = User.query.filter(User.id == toUserID).first()
        conversations = fromUser.conversations
        users_conversation = list(
            filter(lambda conversation: fromUser in conversation.users and toUser in conversation.users and len(conversation.users) == 2,
                   conversations))
        if not users_conversation or len(users_conversation) == 0:
            conversation = Conversation([fromUser, toUser])
            db.session.add(conversation)
            db.session.commit()
            return EmptyConversationDTO(conversation, fromUserID, toUserID)
        else:
            return ConversationDTO(users_conversation[0], fromUserID, toUserID)



conversation_manager = ConversationManager(db)
