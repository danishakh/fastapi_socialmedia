from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from . import models
from .database import engine, get_db


# this should create our tables when we run our app
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# create class to keep a pydantic model of a Post and what it should have
class Post(BaseModel):
    title: str
    content: str
    published: bool = True  # when not sent in the body of req, it will default to True
    


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


# decorator that turns the function to a path operation for fastAPI
@app.get("/")
def root():
    return {"message": "API Scene is ON!"}

# test route
# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     return {"status":"success"}


#  get all posts
@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"data": posts}


# add new post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(**post.dict())
    new_post = models.Post(**post.dict())
    # add to db
    db.add(new_post)
    db.commit()
    # retrieve the new post we just created
    db.refresh(new_post)
    return {"data": new_post}


# get a post by id
@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
    return {"data": post}


# delete a post by id
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")

    # synchronize_session=False is some default config, just got it from documentation
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update a post by id
@app.put("/posts/{id}")
def updatePost(id: int, post: Post, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"data": update_query.first()}
