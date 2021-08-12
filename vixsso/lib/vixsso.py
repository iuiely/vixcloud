# coding: utf-8

import jwt,psutil
from jwt import *
from time import strftime,gmtime
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse, Response
from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List,Optional,Union
from .database import engine,mysqlsession,redis_session
from . import schemas,models

#token set conf
SECRET_KEY = "7d6d5304c0fd0c228ba7afa784ff6e6604e453b97a2ab41fb391a3f4abb4dae9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 400

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

#db models create table
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="vixsso",docs_url=None,redoc_url=None)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def checkprocess(processname):
  pl = psutil.pids()
  for pid in pl:
    if psutil.Process(pid).name() == processname:
      return pid

def get_db():
    try:
        db = mysqlsession()
        yield db
    finally:
        db.close()

def create_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    _token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return _token
'''
def check_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = token_decode.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    get_store_token = redis_session.hgetall(username)
    if get_store_token is None or get_store_token['token'] != token:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"sub":username},expires_delta=access_token_expires)
    in_redis = {"token":access_token,"priv":get_store_token['priv']}
    redis_session.hmset(username,in_redis)
    redis_session.expire(username,18000)
    return {"access_token":access_token,"token_type": "bearer","priv":get_store_token['priv']}
'''

def check_token(token: str = Depends(oauth2_scheme)):
  credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
  try:
    token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = token_decode.get("sub")
    if username is None:
      raise credentials_exception
  except PyJWTError:
    raise credentials_exception
  get_store_token = redis_session.hgetall(username)
  #if get_store_token is None or get_store_token['token'] != token:
  if get_store_token is None :
    raise credentials_exception
  return {"username":username,"priv":get_store_token['priv']}

class MyException(Exception):
    def __init__(self,code:int,message:str):
        self.code=code
        self.message=message

@app.exception_handler(MyException)
def exception_handler(request: Request, exc:MyException):
    return JSONResponse(status_code=exc.code,content={'code':exc.code,'message':exc.message})

def resp_400(code,data,message):
  return {'code': code,'data': data,"message":message}

def resp_200(data):
  return {'code': 200,'data': data,"message":"success"}

##---------------------------------------------------------------------------------------##    
@app.get("/users")
async def display_users(skip:int = 0, limit:int = 20, db:Session = Depends(get_db)):
  users = models.Get_All_Users(db,skip=skip, limit=limit)
  if users is None:
      raise HTTPException(status_code=404, detail="User not found")
  return users

@app.get("/privs")
async def display_privs(skip:int = 0, limit:int = 20, db:Session = Depends(get_db)):
    privs = models.Get_All_Privs(db,skip=skip,limit=limit)
    return privs

@app.get("/users/{user_id}", response_model=List[schemas.UserOut])
async def display_user_id(user_id: int, db:Session = Depends(get_db)):
    user = models.GetUser_ById(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/userlist")
async def display_user_list(db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.List_User(db, user = username['username'])

@app.post("/users")
async def register(user:schemas.CreateUser,db:Session = Depends(get_db)):
    check_result = models.GetUser_ByName(db,username=user.username)
    if check_result :
        return {"code":404,"message":"User already registered"}
    crud.Add_User(db, user=user)
    return resp_200({"username":user.username,"password":user.password})

@app.post("/setpwd")
async def set_password(mf_pwd: schemas.PwdUpdate, db:Session = Depends(get_db)):
    pwd_update = models.Update_pwd(db,update_pwd=mf_pwd)
    if pwd_update is None:
        raise HTTPException(status_code=404, detail="User not found")
    return resp_200({"username":pwd_update['username']})

@app.post("/setpriv",response_model=schemas.PrivUpdate)
async def set_priv(mf_priv:schemas.PrivUpdate,db:Session = Depends(get_db)):
    priv_update = models.Update_priv(db,update_priv=mf_priv)
    if priv_update is None :
        raise HTTPException(status_code=404, detail="User not found")
    return priv_update

@app.post("/deleteuser/{user_id}")
async def delete_user(user_id:int,db:Session = Depends(get_db)):
    del_user = models.Del_User(db,user_id=user_id)
    if del_user is None:
        return {"code":404,"message":"User not found"}
    return resp_200({"id":del_user['id']})

@app.post("/login")
async def user_login(user: schemas.Login, db: Session = Depends(get_db)):
    login_result = models.Login_ByName(db,user=user)
    if login_result is None or login_result == False:
        return {"code":404,"message":"User not found OR Password error"}
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"sub":user.username},expires_delta=access_token_expires)
    in_redis = {"token":access_token,"priv":login_result['priv']}
    redis_session.hmset(user.username,in_redis)
    redis_session.expire(user.username,28000)
    return resp_200({"access_token": access_token, "token_type": "bearer","priv":login_result['priv']})

@app.get("/access_token")
async def access_token(request:Request,token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"}) 
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = token_decode.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    get_store_token = redis_session.hgetall(username)
    if get_store_token is None or get_store_token['token'] != token:
        raise credentials_exception
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(data={"sub":username},expires_delta=access_token_expires)
    in_redis = {"token":access_token,"priv":get_store_token['priv']}
    redis_session.hmset(username,in_redis)
    redis_session.expire(username,900)
    return {"access_token":access_token,"token_type": "bearer","priv":get_store_token['priv']}
