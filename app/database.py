#from flask.ext.sqlalchemy import create_engine
#from flask.ext.sqlalchemy.orm import scoped_session, sessionmaker
#from flask.ext.sqlalchemy.ext.declarative import declarative_base
#from app.configuration import DATABASE_URI

#engine = create_engine(DATABASE_URI, convert_unicode=True)
#db_session = scoped_session(sessionmaker(autocommit=False,
#                                         autoflush=False,
#                                         bind=engine))
#Base = declarative_base()
#Base.query = db_session.query_property()

#def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
#    import app.models
#    Base.metadata.create_all(bind=engine)