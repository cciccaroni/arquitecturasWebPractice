#http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/
from app.mod_database import db

def init_db():
    db.create_all()
