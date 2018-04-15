from sqlalchemy import Column, Integer, String
from app.mod_database import Base



# Define a User model
class User(Base):

    __tablename__ = 'auth_user'

    id = Column(Integer, primary_key=True)

    # User Name
    name    = Column(String(128),  nullable=False)

    # Identification Data: email & password
    email    = Column(String(128),  nullable=False, unique=True)
    password = Column(String(192),  nullable=False)


    # New instance instantiation procedure
    def __init__(self, name, email, password):

        self.name     = name
        self.email    = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.name)
