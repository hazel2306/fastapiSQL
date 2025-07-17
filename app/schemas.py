from pydantic import BaseModel, EmailStr
from datetime import datetime 
from typing import Optional
from enum import IntEnum
# from pydantic.types import conint

##the schema / structure

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut

    # currently a SQLalchemy model
    # we need pydantic to convert it back to a regular pydantic model
    model_config = {
        "from_attributes": True
    }
# class Vote(BaseModel):
#     post_id: int
#     dir: conint(ge=0)

class PostOut(BaseModel):
    Post: Post
    votes: int
    
class Choices(IntEnum):
    remove = 0
    add = 1

class Vote(BaseModel):
    post_id: int
    dir: Choices