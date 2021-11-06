from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg2.extras import RealDictCursor
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}/{settings.db_name}'

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

# run until we get a successful connection
# while True:
#     # connect to an existing database
#     try:
#         conn = psycopg2.connect(host='localhost', dbname='posts_fastapi_db', user='postgres', password='Dybala10!', cursor_factory=RealDictCursor)
#         # create the cursor object which will be used to execute our SQL queries
#         cursor = conn.cursor()
#         print('Database Connection to Postgres was successful!')
#         break
#     except Exception as error:
#         print('Database Connection Failed!')
#         print('Error: ', error)
#         # since it will try to reconnect immediately, lets put a timer
#         time.sleep(2)