from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from sqlalchemy.sql.sqltypes import TIMESTAMP
from starlette.status import HTTP_201_CREATED
from . import models, schemas, utils
from .database import engine, get_db



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


# decorator that turns the function to a path operation for fastAPI
@app.get("/")
def root():
    return {"message": "API Scene is ON!"}

# ------------ POSTS ROUTES ----------------

#  get all posts
@app.get("/posts", response_model=List[schemas.Post])   # imported List from Optional since we are returning a list of Post objects
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


# add new post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    # print(**post.dict())
    new_post = models.Post(**post.dict())
    # add to db
    db.add(new_post)
    db.commit()
    # retrieve the new post we just created
    db.refresh(new_post)
    return new_post


# get a post by id
@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # res.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with id: {id} was not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found!")
    return post


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
@app.put("/posts/{id}", response_model=schemas.Post)
def updatePost(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist!")

    update_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return update_query.first()



# ------------ USERS ROUTES -----------------

# add new user
@app.post("/users", status_code=HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the pass
    hashed_pass = utils.hash_password(user.password)
    user.password = hashed_pass

    new_user = models.User(**user.dict())
    # add to db
    db.add(new_user)
    db.commit()
    # retrieve the new post we just created
    db.refresh(new_user)
    return new_user