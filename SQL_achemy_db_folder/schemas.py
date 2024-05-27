from pydantic import BaseModel,EmailStr
from datetime import datetime


class UserResponse(BaseModel):
    email:str
    created_at:datetime
    class Config:
        orm_mode = True

class User(BaseModel):
    email:EmailStr
    password:str



class PostResponse(BaseModel):
    title:str
    content:str
    published:bool
    created_at:datetime
    class Config:
        orm_mode = True

class Post(BaseModel):
    title:str
    content:str
    published:bool 

class CreatePost(BaseModel):
    title:str
    content:str
    published:bool

class UpdatePost(BaseModel):
    published:bool

