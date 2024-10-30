# app/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, Annotated
from pydantic.types import conint

class PostBase(BaseModel):
  title: str
  content: str
  published: bool = True

# Here, `pass` means it's just going to accept whatever `PostBase`. So, `PostCreate` is essentially same thing as `PostBase`. 
# Schema for Request
class PostCreate(PostBase):
  pass

# Schema for Resposne
class UserOut(BaseModel):
  id: int
  email: EmailStr
  created_at: datetime

# Schema for Resposne 
class Post(PostBase):
  id: int
  created_at: datetime
  owner_id: int
  owner: UserOut

class PostOut(BaseModel):
  Post: Post
  votes: int

# Schema for Request
class UserCreate(BaseModel):
  email: EmailStr
  password: str

class UserLogin(BaseModel):
  email: EmailStr
  password: str

class Token(BaseModel):
  access_token: str
  token_type: str

class TokenData(BaseModel):
  id: int  # Store user ID as an integer

class Vote(BaseModel):
  post_id: int
  dir: Annotated[int, conint(le=1)]  # Using Annotated to apply constraints