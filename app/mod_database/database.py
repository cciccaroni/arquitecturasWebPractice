#http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/
from app.mod_database import Base, engine

def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    import app.mod_auth.models
    Base.metadata.create_all(bind=engine)
