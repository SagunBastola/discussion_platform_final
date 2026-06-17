from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    title: str
    content: str

class PostOut(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True  
class Tokens(BaseModel):
    access_token: str
    token_type: str  

class CommentCreate(BaseModel):
    content: str
    post_id: int  # The target post the comment is being attached to

class CommentOut(BaseModel):
    id: int
    content: str
    post_id: int
    created_at: datetime
    author: UserOut  # Automatically nests the user's public info (id, username)

    class Config:
        from_attributes = True