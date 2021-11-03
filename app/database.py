from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Dybala10!@localhost/posts_fastapi_db'

# engine is responsible for sqlalchemy to connect to postgres
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# we have to make use of a session when talking to the db
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# all of our models that we are going to be creating as our tables in the db, will be extending this base class
Base = declarative_base()

# Dependency (copy/pasted from fastAPI docs)
# this will be passed into each api path function so that it creates a session with the db, and closes it out once its done
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()