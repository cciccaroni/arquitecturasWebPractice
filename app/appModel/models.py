from app.mod_database import db
from sqlalchemy.sql import *


# esta tabla es necesaria para las relaciones muchos a muchos
user_conversation = db.Table('user_conversation',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'), primary_key=True)
)

# Define a User model
class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),  nullable=False)
    conversations = db.relationship('Conversation', secondary=user_conversation, lazy='subquery',
                                    back_populates='users')
    # Identification Data: email & password
    email = db.Column(db.String(128),  nullable=False, unique=True)
    password = db.Column(db.String(192),  nullable=False)


    # New instance instantiation procedure
    def __init__(self, name, email, password):
        self.name     = name
        self.email    = email
        self.password = password

    def addConversation(self, conversation):
        self.conversations.append(conversation)

    def __repr__(self):
        return '<User %r>' % (self.name)

    # Required for login
    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', lazy=True,
                                 backref='conversation')
    users = db.relationship('User', secondary=user_conversation, lazy='subquery',
                            back_populates='conversations')

    def __init__(self, users):
        self.users = users


    def __repr__(self):
        return '<Conversation %r>' % (self.name)


class ConversationName(db.Model):
    __tablename__ = 'conversation_name'

    id = db.Column(db.Integer, primary_key=True)
    conversation = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    name = db.Column(db.String(128), nullable=False)

    def __init__(self,conversation,name):
        self.conversation = conversation
        self.name = name

    def __repr__(self):
        return '<ConversationName %r>' % (self.name)


class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    def __init__(self,message,user_id,conversation_id):
        self.message = message
        self.user_id = user_id
        self.conversation_id = conversation_id


    def __repr__(self):
        return '<Message %r>' % (self.name)




