from app.appModel.models import *

class UserDTO:
    def __init__(self, userID):
        self.id = userID
        self.name = User.query.filter(User.id == userID).first().name

class MessageDTO:
    def __init__(self, fromUserID,message):
        self.fromUser = UserDTO(fromUserID)
        self.payload = message


class ConversationDTO:
    def __init__(self, conversation, fromUserID, toUserID):
        self.id = conversation.id
        self.fromUser = UserDTO(fromUserID)
        self.toUser = UserDTO(toUserID)
        self.messages = list(map(lambda message: MessageDTO(message.user_id,message.message),list(conversation.messages)))


class EmptyConversationDTO:
    def __init__(self, conversation,fromUserID, toUserID):
        self.id = conversation.id
        self.fromUser = UserDTO(fromUserID)
        self.toUser = UserDTO(toUserID)
        self.messages = []


class ConversationManager:
    def __init__(self, db):
        self.db = db
        self.users = User.__table__

    def startConversation(self, fromUserID, toUserID):
        fromUser = User.query.filter(User.id == fromUserID).first()
        toUser = User.query.filter(User.id == toUserID).first()
        conversations = fromUser.conversations
        users_conversation = list(
            filter(lambda conversation: toUser in conversation.users, conversations))
        if not users_conversation or len(users_conversation) == 0:
            conversation = Conversation([fromUser, toUser])
            db.session.add(conversation)
            db.session.flush()
            new_conversation = EmptyConversationDTO(conversation, fromUser.id, toUser.id)
            db.session.commit()
            return new_conversation
        else:

            return ConversationDTO(users_conversation[0], fromUser.id, toUser.id)

    #TODO: improve error conditions when the userid doesnt match with the conversation
    def log_message(self,fromUserID,message,conversationID):
        fromUser = User.query.filter(User.id == fromUserID).first()
        if not fromUser:
            return

        conversation = Conversation.query.filter(Conversation.id == conversationID).first()
        if fromUser not in conversation.users:
            return

        new_message = Message(message,fromUserID,conversationID)
        db.session.add(new_message)
        conversation.messages.append(new_message)
        db.session.commit()
        return


conversation_manager = ConversationManager(db)
