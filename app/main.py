from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
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
    rating: Optional[int] = None    # this will act as an optional field


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

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    return {"status":"success"}


@app.get("/posts")
def get_posts():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    print(new_post)
    # commit the staged changes
    conn.commit()
    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, res: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    post = cursor.fetchone()
    if not post:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    deleted_post = cursor.fetchone()
    conn.commit()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def updatePost(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")

    return {"message": updated_post}
