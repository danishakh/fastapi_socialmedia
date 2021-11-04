from sys import addaudithook
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post, auth



# this should create our tables when we run our app
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# run until we get a successful connection
while True:
    # connect to an existing database
    try:
        conn = psycopg2.connect(host='localhost', dbname='posts_fastapi_db', user='postgres', password='Dybala10!', cursor_factory=RealDictCursor)
        # create the cursor object which will be used to execute our SQL queries
        cursor = conn.cursor()
        print('Database Connection to Postgres was successful!')
        break
    except Exception as error:
        print('Database Connection Failed!')
        print('Error: ', error)
        # since it will try to reconnect immediately, lets put a timer
        time.sleep(2)


# this is how we setup our fastAPI router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# decorator that turns the function to a path operation for fastAPI
@app.get("/")
def root():
    return {"message": "API Scene is ON!"}



