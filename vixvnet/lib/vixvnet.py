# coding: utf-8

import jwt,json
from jwt import *
from time import strftime,gmtime
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi import Depends, FastAPI, HTTPException,status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response
from sqlalchemy.orm import Session
from typing import List,Optional
from .database import engine,localmysqlsession,sso_redis_session,vnet_redis_session
from . import models, schemas

#token set conf
SECRET_KEY = "7d6d5304c0fd0c228ba7afa784ff6e6604e453b97a2ab41fb391a3f4abb4dae9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
auth_failed = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Permissions error",headers={"WWW-Authenticate": "Bearer"})

#db models create table
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "vixvnet",docs_url=None,redoc_url=None)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    try:
        db = localmysqlsession()
        yield db
    finally:
        db.close()

def get_token(token: str = Depends(oauth2_scheme)):
  return token

def check_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not validate credentials",headers={"WWW-Authenticate": "Bearer"})
    try:
        token_decode = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = token_decode.get("sub")
        if username is None:
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception
    get_store_token = sso_redis_session.hgetall(username)
    #if get_store_token is None or get_store_token['token'] != token:
    if get_store_token is None :
        raise credentials_exception
    return {"username":username,"priv":get_store_token['priv']}

def resp_400(code,data,message):
    return {'code': code,'data': data,"message":message}

def resp_200(data):
    return {'code': 200,'data': data,"message":"success"}

###------------------------------ Vnet API ----------------------------------------------###
@app.get("/vnetotal/{zone}")
async def fetch_vnet_total(zone:str, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Vnet_Total(db, user = username['username'], priv=int(username['priv']),zone=zone)
  return result

@app.get("/networks", response_model = schemas.RespNetworks)
async def display_networks(skip:int = 0, limit:int = 20, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    nets = models.All_Nets(db,skip=skip,limit=limit)
  else:
    nets = models.User_Nets(db,user=username['username'],skip=skip,limit=limit)   
  return nets

@app.get("/netslist", response_model = List[schemas.RespNetsList])
async def nets_list(db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    nets = models.AllNets_List(db)
  else:
    nets = models.UserNets_List(db,user=username['username'])
  return nets

@app.get("/assignip/{id}",response_model = schemas.AssignIPMAC)
async def assign_ip(id:int,limit:int = 1,db:Session = Depends(get_db)):
  result = models.Assign_IpMac(db,id = id,limit = limit)
  return result

@app.get("/vmusednet/{id}",response_model = schemas.VmUsedNet)
async def vm_used_net(id:int,db:Session = Depends(get_db)):
  net = models.Network_ById(db,id = id)
  return net

@app.get("/network/{id}", response_model = schemas.NetworkDetail)
async def display_network(id:int, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    network = models.Network_ById(db,id = id)
  else:
    network = models.Network_ByUserId(db,user=username['username'],id=id)
  return network

@app.post("/recycleip/",response_model = schemas.RespNetInfo)
async def recycle_ip(nets: schemas.RecycleIp, db: Session = Depends(get_db)):
  result = models.Recycle_DHCP_Ip(db,nets = nets)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/network", response_model = schemas.RespNetInfo)
async def create_network(network: schemas.CreateNetwork, db:Session = Depends(get_db) ,username: str = Depends(check_token)):
  if network.mode == 'flat':
    flatnet = models.FlatNet(db)
    if flatnet:
      return resp_400(400,[],"General network already exist")
  if int(username['priv']) == 1:
    result = models.Create_Network(db, network = network, user = username['username'], priv = username['priv'])
    if result['message'] == 'success':
      return resp_200(result['data'])
    else:
      return resp_400(400,[],result["message"])
  else:
    return resp_400(401,[],"The user's permissions error")

@app.post("/setnetworkstate", response_model = schemas.RespNetInfo)
async def set_network_state(netstate: schemas.NetState, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(401,[],"The user's permissions error")
  result = models.Set_Net_State(db,netstate = netstate)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])


@app.post("/setnetworkprem",response_model = schemas.RespNetInfo)
async def set_network_prem(netperm: schemas.NetPerm, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Net_Perm(db,netperm = netperm)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnetworkuser" ,response_model = schemas.RespNetInfo)
async def set_network_user(netuser: schemas.NetUser, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Net_User(db,netuser = netuser)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/deletenetwork/{id}", response_model = schemas.RespNetInfo)
async def delete_network(id:int,db:Session = Depends(get_db), username: str= Depends(check_token), token: str = Depends(get_token)):
  result = models.Delete_network(db,id=id, user = username['username'], token = token)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/removenetwork/{id}", response_model = schemas.RespNetInfo)
async def delete_network(id: int, db:Session = Depends(get_db), username: str= Depends(check_token)):
  result = models.Remove_Network(db,id=id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/stopnetwork/{id}",response_model = schemas.RespNetInfo)
async def stop_network(id: int,db:Session = Depends(get_db), username: str= Depends(check_token), token: str = Depends(get_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Stop_Network(db,id=id, token = token)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/startnetwork/{id}", response_model = schemas.RespNetInfo)
async def start_network(id: int,db:Session = Depends(get_db), username: str= Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Start_Network(db,id=id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/startnetworks")
async def start_networks(db:Session = Depends(get_db), username: str= Depends(check_token)):
    if int(username['priv']) != 1:
        return resp_400(400,[],"The user's permissions error")
    nets = models.Start_All_Nets(db)
    if nets is None:
        return resp_400(400,"","启动网络出错")
    return resp_200(nets)

