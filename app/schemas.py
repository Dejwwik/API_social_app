print(f"app/schemas.py package: {__package__}")
from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

#Template for classed below
class UserBase(BaseModel):
    email: EmailStr

#Template for creating/updating user
class UserCreate(UserBase):
    password: str

#Response user model
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True #same as orm_mode before, isnead orm_mode=True is this. 

class UserLogin(BaseModel):
    email: EmailStr
    password: str

#Template for classed below
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None

#Template for creating/updating post
class PostCreate(PostBase):
    pass

#Response for model before added voting. After voting there is Post: there is this Post type, and vote: int
class Post(PostBase):
    id: int
    created_at: datetime
    owner: UserResponse

    class Config:
        from_attributes = True

#This is final output for post
class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir: bool