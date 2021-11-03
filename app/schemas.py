from datetime import datetime
from pydantic import BaseModel, EmailStr

from app.database import Base

# create class to keep a pydantic model of a Post and what it should have
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # when not sent in the body of req, it will default to True

# class CreatePost(BaseModel):
#     title: str
#     content: str
#     published: bool = True

# class UpdatePost(BaseModel):
#     title: str
#     content: str
#     published: bool


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
    # extra config for pydantic models to convert the sqlalchemy model to a pydantic model
    class Config:
        orm_mode = True


# class for users
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    created_at: datetime
    # extra config for pydantic models to convert the sqlalchemy model to a pydantic model
    class Config:
        orm_mode = True