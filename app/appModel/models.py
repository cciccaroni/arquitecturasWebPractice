from app.mod_database import db


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
        backref='users')
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

class Conversation(db.Model):
    __tablename__ = 'conversation'

    id = db.Column(db.Integer, primary_key=True)
    messages = db.relationship('Message', lazy='subquery',
                                 backref='conversation')

    def __repr__(self):
        return '<Conversation %r>' % (self.name)



class Message(db.Model):

    __tablename__ = 'message'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(128), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))


    def __repr__(self):
        return '<Message %r>' % (self.name)



