from app.mod_database import db
from sqlalchemy.sql import *

# esta tabla es necesaria para las relaciones muchos a muchos
user_group = db.Table('user_group',
                      db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
                      )

user_conversation = db.Table('user_conversation',
                             db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                             db.Column('conversation_id', db.Integer, db.ForeignKey('conversation.id'),
                                       primary_key=True)
                             )

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

# Define a User model
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    conversations = db.relationship('Conversation', secondary=user_conversation, lazy='subquery',
                                    back_populates='users')
    groups = db.relationship('Group', secondary=user_group, lazy='subquery',
                             back_populates='users')

    # Identification Data: email & password
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(192), nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password

    def addConversation(self, conversation):
        self.conversations.append(conversation)

    def __repr__(self):
        return '<User %r>' % (self.name)
    
    def getLoggedUser(self):
        return LoggedUser(self)


class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', lazy=True,
                               backref='conversation')
    users = db.relationship('User', secondary=user_conversation, lazy='subquery',
                            back_populates='conversations')
    group = db.relationship('Group', lazy=True,
                            backref='conversation', uselist=False)

    def __init__(self, users=[], group=None):
        self.users = users
        self.group = group

    def __repr__(self):
        return '<Conversation %r>' % (self.id)


class Message(db.Model):
    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    def __init__(self, message, user_id, conversation_id):
        self.message = message
        self.user_id = user_id
        self.conversation_id = conversation_id

    def __repr__(self):
        return '<Message %r>' % (self.message)


class Group(db.Model):
    __tablename__ = 'group'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    users = db.relationship('User', secondary=user_group, lazy='subquery',
                            back_populates='groups')
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))

    def __init__(self, name, users):
        self.name = name
        self.users = users

    def __repr__(self):
        return '<Group %r>' % (self.name)





