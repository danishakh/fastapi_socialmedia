from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint

from app.database import Base
from app.models import User


# schema for users
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

# response schema for /users api
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    # extra config for pydantic models to convert the sqlalchemy model to a pydantic model
    class Config:
        orm_mode = True


# schema used to send /login request
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# create class to keep a pydantic model of a Post and what it should have
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # when not sent in the body of req, it will default to True

# lets extend the PostBase class, which means it will inherit everything in PostBase
class PostCreate(PostBase):
    pass
# not creating a PostUpdate since it is essentially going to be the same as PostCreate w.r.t properties passed


# class for the response of /posts apis
# extends our PostBase class
class Post(PostBase):
    # only need to specify the new columns since others are inherited from PostBase
    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    # extra config for pydantic models to convert the sqlalchemy model to a pydantic model
    class Config:
        orm_mode = True

# creating this to include likes for each post
class PostOut(BaseModel):
    Post: Post
    likes: int

    class Config:
        orm_mode = True

# schema used to verify our user is still logged in - using JWT
# token will be sent alongside requests by user for protected resources
class Token(BaseModel):
    access_token: str
    token_type: str

# schema for the data embedded into our access token
class TokenData(BaseModel):
    id: Optional[str]


class Like(BaseModel):
    post_id: int
    dir: conint(le=1)   # this will restrict the passed in values to be <= 1 (includes -ve numbers but dont know yet how to overcome that validation here)