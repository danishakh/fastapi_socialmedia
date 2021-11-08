from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import models
from .database import engine
from .routers import user, post, auth, like


# this should create our tables when we run our app
# after alembic setup - we do not need this anymore as alembic will be in charge of creating all our tables based on our models
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,   # which domains should be able to talk to our api
    allow_credentials=True,  
    allow_methods=["*"],
    allow_headers=["*"],
)



# this is how we setup our fastAPI router
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(like.router)

# decorator that turns the function to a path operation for fastAPI
@app.get("/")
def root():
    return {"message": "Welcome to my Posts API built using FastAPI!"}



