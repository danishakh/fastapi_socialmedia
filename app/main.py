from fastapi import FastAPI
from . import models
from .database import engine
from .routers import user, post, auth


# this should create our tables when we run our app
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# this is how we setup our fastAPI router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# decorator that turns the function to a path operation for fastAPI
@app.get("/")
def root():
    return {"message": "Welcome to my Posts API built using FastAPI!"}



