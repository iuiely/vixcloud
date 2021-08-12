from typing import List
from datetime import datetime
from pydantic import BaseModel

class UserBase(BaseModel):
    username:str

class CreateUser(UserBase):
    id:int = None
    password:str
    priv:int
    create_time:datetime = None

class PwdUpdate(UserBase):
    password:str

class PrivUpdate(UserBase):
    priv:int

class DelUser(BaseModel):
    id:int
    
    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    priv:int

    class Config:
        orm_mode = True

class Login(UserBase):
    password:str

class UserPriv(BaseModel):
    id:int
    username:str
    priv:str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class UserOut(UserBase):
    id: int
    priv:str
    create_time:str

    class Config:
        orm_mode = True
