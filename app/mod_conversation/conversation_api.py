from app.appModel.models import *
from app.mod_api.exporter import exportConversation
from app import app

class UserDTO:
    def __init__(self, userID):
        self.id = userID
        self.name = User.query.filter(User.id == userID).first().name

class MessageDTO:
    def __init__(self, fromUserID,message, type):
        self.fromUser = UserDTO(fromUserID)
        self.payload = message
        self.type = type


class ConversationDTO:
    def __init__(self, conversation, title):
        self.id = conversation.id
        self.title = title
        self.recipientList = list(map(lambda user: UserDTO(user.id),conversation.obtainUsersInConversation()))
        self.messages = list(map(lambda message: MessageDTO(message.user_id, message.message, message.type),list(conversation.messages)))


class EmptyConversationDTO:
    def __init__(self, conversation,title):
        self.id = conversation.id
        self.title = title
        self.messages = []
        self.recipientList = list(map(lambda user: UserDTO(user.id),conversation.obtainUsersInConversation()))



class ConversationManager:
    def __init__(self, db):
        self.db = db
        self.users = User.__table__

    def startConversation(self, fromUserID, toUserID):
        fromUser = User.query.filter(User.id == fromUserID).first()
        toUser = User.query.filter(User.id == toUserID).first()
        users_conversation = self.conversationBetweenUsers(fromUser, toUser)
        
        app.logger.debug('Starting conversation: {} :: {}'.format(fromUser, toUser))
        if not users_conversation or len(users_conversation) == 0:
            conversation = self.createNewConversation(fromUser, toUser)
            if self.isExternal(toUser):
                app.logger.debug('With an external user')
                exportConversation(conversation.id, fromUser, toUser)
            return conversation
        else:
            return ConversationDTO(users_conversation[0], toUser.name)

    def startGroupConversation(self, groupID, platform_id=1, external_id=1):
        group = Group.query.filter(Group.id == groupID).first()
        conversation = group.conversation
        if not conversation:
            return self.createNewGroupConversation(group, platform_id=platform_id, external_id=external_id)
        else:
            return ConversationDTO(conversation, group.name)

    def createNewGroupConversation(self, group, platform_id=None, external_id=None):
        if platform_id is None:
            platform_id = 1
        if external_id is None:
            external_id = 1
        conversation = Conversation(group=group, platform_id=platform_id, external_id=external_id)
        db.session.add(conversation)
        db.session.flush()
        new_conversation = EmptyConversationDTO(conversation, group.name)
        db.session.commit()
        return new_conversation

    def createNewConversation(self, fromUser, toUser):
        conversation = Conversation([fromUser, toUser])
        db.session.add(conversation)
        db.session.flush()
        new_conversation = EmptyConversationDTO(conversation, toUser.name)
        db.session.commit()
        return new_conversation

    def conversationBetweenUsers(self, fromUser, toUser):
        conversations = fromUser.conversations
        users_conversation = list(
            filter(lambda conversation: toUser in conversation.users, conversations))
        return users_conversation

    #TODO: improve error conditions when the userid doesnt match with the conversation
    def log_message(self,fromUserID,message,conversationID, type):
        fromUser = User.query.filter(User.id == fromUserID).first()
        if not fromUser:
            return

        conversation = Conversation.query.filter(Conversation.id == conversationID).first()
        if fromUser not in conversation.users and fromUser not in conversation.group.users:
            return

        new_message = Message(message,fromUserID,conversationID, type)
        db.session.add(new_message)
        conversation.messages.append(new_message)
        db.session.commit()
        return

    def isExternal(self, user):
        return user.platform_id != 1


conversation_manager = ConversationManager(db)
