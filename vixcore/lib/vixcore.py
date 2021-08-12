# coding: utf-8

import jwt,json,random,os,aiofiles,psutil
from jwt import *
from time import strftime,gmtime
from datetime import datetime, timedelta
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from fastapi import Depends, FastAPI, HTTPException,status,Form, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response,FileResponse
from sqlalchemy.orm import Session
from werkzeug.security import generate_password_hash, check_password_hash
from typing import List,Optional
from .database import engine,localmysqlsession,sso_redis_session,core_redis_session
from . import models, schemas
from .config import *

#token set conf
SECRET_KEY = "7d6d5304c0fd0c228ba7afa784ff6e6604e453b97a2ab41fb391a3f4abb4dae9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="")
auth_failed = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Permissions error",headers={"WWW-Authenticate": "Bearer"})

#db models create table
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title = "vixcore",docs_url=None,redoc_url=None)
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

def ran_char(num):
  C = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
  result = ''
  for i in range(num):
    result += random.choice(C)
  return result

def resp_400(code,data,message):
  return {'code': code,'data': data,"message":message}

def resp_200(data):
  return {'code': 200,'data': data,"message":"success"}

###------------------------------ Pool API ----------------------------------------------###
@app.get("/zones",response_model=schemas.RespZones)
async def display_zones(skip:int = 0, limit:int = 20, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.All_Zones(db,skip=skip, limit=limit)

@app.get("/zonelist")
async def zone_list(db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  zones = models.List_Zones(db)
  return zones

@app.post("/zone",response_model=schemas.RespZoneInfo)
async def create_zone(zone:schemas.NewZone,db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Create_Zone(db,zone=zone)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setzonestate",response_model=schemas.RespZoneInfo)
async def set_zone_state(zone: schemas.SetZoneState, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Zone_State(db, zone = zone)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setzonepool")
async def set_zone_pool(pool: schemas.SetZonePool, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Zone_Pool(db, pool = pool)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/deletezone/{id}",response_model=schemas.RespZoneInfo)
async def delete_zone(id:int,db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Del_Zone(db,id = id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

###------------------------------ Node API ----------------------------------------------###
@app.get("/listagentnodes")
async def list_nodes(db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  nodes = models.List_AgentNodes(db)
  return nodes

@app.get("/nodes")
async def display_nodes(skip:int = 0, limit:int = 20, db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  nodes = models.All_Nodes(db,skip=skip, limit=limit)
  return nodes

@app.get("/nodes/{zone}" ,response_model =schemas.RespZoneNodes)
async def display_zone_nodes(zone: str, skip:int = 0, limit:int = 20, db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.Zone_Nodes(db ,zone = zone ,skip=skip, limit=limit)

#@app.get("/node/{id}" , response_model=schemas.Nodes)
@app.get("/node/{id}" )
async def display_node_id(id:int, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.Node_ById(db,id = id)

@app.get("/listnodevm/{id}")
async def list_node_vm(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.List_Node_Vm(db, id = id, user = username['username'], priv = username['priv'])
  return result

@app.get("/nodecpuperf/{id}")
async def display_nodecpu_perf(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.NodeCpuPerf_ById(db, id = id)

@app.get("/nodememperf/{id}")
async def display_nodemem_perf(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.NodeMemPerf_ById(db, id = id)

@app.post("/node", response_model = schemas.RespNodeInfo)
async def create_node(node:schemas.CreateNode,db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Create_Node(db,nodes = node)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnodecpu", response_model = schemas.RespNodeInfo)
async def set_node_cpu(cpu: schemas.SetNodeCpu, db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Node_Cpu(db,cpu = cpu)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnodemem", response_model = schemas.RespNodeInfo)
async def set_node_mem(mem: schemas.SetNodeMem, db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Node_Mem(db,mem = mem)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnodepoolsize", response_model = schemas.RespNodeInfo)
async def set_node_pool_size(pools: schemas.SetNodePoolSize, db:Session = Depends(get_db)):
#async def set_node_mem(mem: schemas.SetNodeMem, db:Session = Depends(get_db),username: str = Depends(check_token)):
  #if int(username['priv']) != 1:
  #  return resp_400(400,[],"The user's permissions error")
  result = models.Set_Node_Pool_Size(db, pools = pools)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnodedel/{addr}")
async def set_node_del(addr:str, db:Session = Depends(get_db)):
  result = models.Set_Node_Delete(db, addr = addr)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnodestate", response_model = schemas.RespNodeInfo)
async def set_node_state(nodestat: schemas.SetNodeState, db: Session = Depends(get_db)):
  result = models.Set_Node_State(db,nodestat = nodestat)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,"",result['message'])

@app.post("/deletenode/{id}", response_model = schemas.RespNodeInfo)
async def delete_node(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Delete_Node(db, id = id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

###------------------------ Network Devices API -----------------------------------------###
@app.get("/netdevs")
async def display_network_devices(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  netdevs = models.All_NetDevices(db,skip=skip, limit=limit)
  return netdevs

@app.get("/netdevs/{zone}")
async def display_zone_network_devices(zone: str, skip:int = 0, limit:int = 20, db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.Zone_NetDevices(db ,zone = zone ,skip=skip, limit=limit)

@app.get("/netdev/{id}")
async def display_network_device_id(id:int, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.NetDevice_ById(db,id = id)

@app.get("/netdevcmds/{addr}")
async def display_device_cmd_addr(addr: str, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.NetDeviceCmd_ByAddr(db,addr = addr)

@app.get("/listnetdevcmds", response_model = List[schemas.RespVlanCmds])
async def list_device_cmd_addr(zone: int, action: str, db:Session = Depends(get_db)):
  result = models.List_VlanCmds(db, zone = zone, action = action)
  return result

@app.get("/listcorenetdevcmds", response_model = List[schemas.RespVlanCmds])
async def list_device_cmd_addr(zone: int, action: str, db:Session = Depends(get_db)):
  result = models.List_CoreVlanCmds(db, zone = zone, action = action)
  return result

@app.get("/netdevcmd/{id}", response_model = schemas.RespNetDeviceCmdContent)
async def display_device_cmd_id(id: int, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  return models.NetDeviceCmd_ById(db, id = id)

@app.post("/netdev", response_model = schemas.RespNetworkDevice)
async def create_network_device(netdev: schemas.CreateNetDevice, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Create_NetDevice(db,netdev = netdev)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnetdevstate", response_model = schemas.RespNetworkDevice)
async def set_network_device_state(netdevstat: schemas.SetNetDevState, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_NetDev_State(db, netdevstat = netdevstat)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnetdevpwd", response_model = schemas.RespNetworkDevice)
async def set_network_device_pwd(netdevpwd: schemas.SetNetDevPwd, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_NetDev_Pwd(db, netdevpwd = netdevpwd)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/netdevicecmd", response_model = schemas.RespNetworkDevice)
async def create_network_device_cmd(devcmd: schemas.DeviceCmd, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Create_NetDevice_Cmd(db, devcmd = devcmd)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setnetdevcmd")
async def set_network_device_cmd(devcmd: schemas.DeviceCmd, db:Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_NetDevice_Cmd(db, devcmd = devcmd)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/deletedevcmd/{id}", response_model = schemas.RespNetworkDevice)
async def delete_network_device_cmd(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Delete_NetDeviceCmd(db, id = id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/deletenetdev/{id}", response_model = schemas.RespNetworkDevice)
async def delete_network_device(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Delete_NetDevice(db, id = id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])


###----------------------------- OS Image API -------------------------------------------###
@app.get("/images" , response_model=schemas.RespOSImages)
async def display_images(skip:int = 0, limit:int = 20, db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    images = models.All_Images(db,skip=skip, limit=limit)
  else:
    images = models.User_Images(db,user = username['username'],skip=skip,limit=limit)     
  return images

@app.get("/image/{id}", response_model=schemas.RespImage)
async def display_image(id:int, db:Session = Depends(get_db), username: str = Depends(check_token)):
  image = models.Image_ById(db,id=id)
  return image

@app.get("/imageslist")
async def images_list(db:Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    images = models.List_AllImages(db)
  else:
    images = models.List_UserImages(db,user=username['username'])
  return images

@app.post("/image", response_model=schemas.RespImageInfo)
async def create_image(request: Request,files:UploadFile= File(...),name:str = Form(...),size:int=Form(...),desc:str=Form(...),
			db:Session = Depends(get_db),username: str = Depends(check_token)):
  sn = 'image-'+ran_char(24)
  path = config.get("vixcore.image.store")
  if not os.path.exists(path):
    os.makedirs(path)
  if path[-1] == '/':
    filepath=path+sn
  else:
    filepath=path+'/'+sn
  upfile = await files.read()
  with open(filepath,'wb') as f:
    f.write(upfile)
  fsize = os.path.getsize(filepath)
  if fsize == size:
    check = models.Image_ByUserImageName(db,user = username['username'],image = name)
    if check :
      return {"message":"Image already exists"}
    result = models.Create_OsImage(db,name=name,size=size,desc=desc,sn=sn,filepath=filepath,user = username['username'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,"",result['message'])

@app.post("/setimageperm", response_model=schemas.RespImageInfo)
async def set_image_perm(perm:schemas.ImagePerm, db: Session = Depends(get_db),username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Image_Perm(db,perm = perm)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,"",result['message'])

@app.post("/setimageuser",response_model=schemas.RespImageInfo)
async def set_image_user(user: schemas.ImageUser, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    return resp_400(400,[],"The user's permissions error")
  result = models.Set_Image_User(db,user = user)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,"",result['message'])

@app.post("/deleteimage/{id}", response_model=schemas.RespImageInfo)
async def delete_image(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    result = models.Super_Delete_Image(db,id = id)
  else:
    result = models.Delete_image(db,id = id, user = username['username'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,"",result['message'])

@app.get("/downloadfile/{id}")
async def download_iamge(id:int,db: Session = Depends(get_db)):
    image = models.Image_ById(db,id = id)
    imagefile = image['path']
    return FileResponse(imagefile,filename=image['sn'])

###-----------------------------  POOLS API -------------------------------------------###
@app.get("/listzonepools/{id}")
async def list_zone_pools(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    resp_400(400,[],"The user's permissions error")
  return models.List_ZonePool(db, id = id)

@app.get("/zonepools/{zone}")
async def zone_pools(zone: str, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    resp_400(400,[],"The user's permissions error")
  return models.FetchZonePool_ByName(db, zone = zone)

@app.get("/zonepoolpath/{id}")
async def zone_pool_path(id:int,db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) != 1:
    resp_400(400,[],"The user's permissions error")
  return models.FetchPoolPath_ById(db, id = id)

###----------------------------- Volume  API --------------------------------------------###
@app.get("/nodevmlist/{node}")
async def display_node_vm_list(node: str, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Node_Vm_List(db,node=node,user=username['username'])
  return result

@app.get("/volumes", response_model = schemas.respVolumes)
async def display_all_volumes(skip: int=0, limit: int=20, db: Session = Depends(get_db), username: str = Depends(check_token)):
  if int(username['priv']) == 1:
    result = models.All_Volumes(db,skip=skip,limit=limit)
  else:
    result = models.User_Volumes(db,user = username['username'], skip = skip,limit = limit)
  return result

@app.get("/volume/{id}")
async def display_volume(id:int, db: Session = Depends(get_db),username: str = Depends(check_token)):
  result = models.One_Volume_ById(db,id = id, user = username['username'], priv = username['priv'])
  return result

@app.post("/setvolumetovm")
async def volume_to_vm(volume: schemas.SetVolToVm, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Attach_Vm_Disk(db,volume = volume, user = username['username'], priv = username['priv'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,"",result['message'])
    
@app.post("/deletevolume/{id}")
async def delete_volume(id:int, db: Session = Depends(get_db),username: str = Depends(check_token)):
  result = models.Delete_Volume_ById(db,id = id, user = username['username'], priv = username['priv'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,"",result['message'])

###----------------------------- Vms  API --------------------------------------------###
@app.get("/vms")
async def display_vms(skip:int = 0, limit:int = 20, db:Session = Depends(get_db)):
  vms = models.All_Vms(db,skip=skip, limit=limit)
  return vms

@app.get("/vm/{id}")
async def display_vm(id:int, db:Session = Depends(get_db)):
  vm = models.One_Vm(db,id = id)
  return vm

@app.get("/nodecpumemdisk/{id}")
async def display_nodecpumemdisk(id:int, db:Session = Depends(get_db)):
  vmnode = models.Node_Cpu_Mem_Disk(db,id = id)
  return vmnode

@app.get("/vmnet/{vm_id}",response_model = schemas.ReVmUsedNets)
async def vm_used_net(vm_id: int,db: Session = Depends(get_db)):
  vmusednet = models.Get_Vm_Used_Net(db,vm_id=vm_id)
  if vmusednet["message"] == "success":
    return resp_200(vmusednet['data'])
  else:
    return resp_400(404,[],vmusednet["message"])

@app.post("/createvm", response_model = schemas.RespVmInfo)
async def create_vm(vm:schemas.CreateVM,db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Create_Vm(db,vm = vm,user = username['username'])
  if result["message"] == "success":
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/rmvm/{id}" ,response_model = schemas.RespVmInfo)
async def delete_vm(id:int,db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Delete_Vm_ById(db,id = id)
  if result['message'] =='success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/delvmname/{vm}" ,response_model = schemas.RespVmInfo)
async def delete_vmname(vm:str, db: Session = Depends(get_db)):
  result = models.Delete_Vm_ByName(db,vm = vm)
  if result['message'] =='success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setvcpu", response_model = schemas.RespVmInfo)
async def set_vm_vcpu(vcpu: schemas.VmVcpu, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Set_Vm_Vcpu(db, vcpu = vcpu)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/setvmem", response_model = schemas.RespVmInfo)
async def set_vm_vmem(vmem: schemas.VmVmem, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Set_Vm_Vmem(db, vmem = vmem)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/setdisksize", response_model = schemas.RespVmInfo)
async def set_vm_disksize(disksize: schemas.VmDiskSize, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Set_Vm_Disksize(db, disksize = disksize)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/webconsole/{id}", response_model = schemas.RespConsoleInfo)
async def webconsole(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Webconsole(db, id = id)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/addvmnet")
async def add_vm_net(vm_net: schemas.AddVmNet, db: Session = Depends(get_db), username : str = Depends(check_token)):
  result = models.Add_Vm_Net(db,vm_net=vm_net)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/delvmnet")
async def del_vm_net(del_vm_net: schemas.DelVmNet,db: Session = Depends(get_db), username : str = Depends(check_token)):
  result = models.Del_Vm_Net(db ,del_vm_net = del_vm_net)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/addvmdisk")
async def add_vm_disk(disk: schemas.AddVmDisk, db: Session = Depends(get_db), username : str = Depends(check_token)):
  result = models.Add_Vm_Disk(db,disk = disk,user = username['username']) 
  if result['message'] =='success':
    return resp_200(result['data'])
  else:
    return resp_400(400,[],result['message'])

@app.post("/rmvmdisk")
async def rm_vm_disk(vmdisk: schemas.RmVmDisk, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Rm_Vm_Disk(db,vmdisk=vmdisk)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,"",result['message'])

@app.post("/setsyspwd", response_model = schemas.RespVmInfo)
async def set_system_password(syspwd: schemas.VmSysPwd, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Set_Sys_Password(db,syspwd=syspwd,user=username['username'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/runvm/{id}", response_model = schemas.RespVmInfo)
async def run_vm(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Run_Vm_ById(db,id = id)
  if result['message'] =='success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/stopvm/{id}", response_model = schemas.RespVmInfo)
async def stop_vm(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Stop_Vm_ById(db,id = id)
  if result['message'] =='success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/shutvm/{id}", response_model = schemas.RespVmInfo)
async def shut_vm(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Shut_Vm_ById(db,id = id)
  if result['message'] =='success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/vmconvertimage", response_model = schemas.RespVmInfo)
async def vm_convert_image(vmtoimage:schemas.VmConvertImage, db: Session = Depends(get_db), token: str = Depends(get_token)):
  result = models.Vm_To_Image(db, vmtoimage = vmtoimage,token=token)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.get("/goodnode/{id}")
async def fetch_good_node(id: int, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Fetch_Good_Node(db, id = id ,user = username['username'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/migrationvm", response_model = schemas.RespVmInfo)
async def migration_vm(vm:schemas.MigrateVm, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Migrate_Vm(db,migratevm=vm,user=username['username'])
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

@app.post("/setvmstate", response_model = schemas.RespVmInfo)
async def set_vm_stat(vmstat: schemas.SetVmState, db: Session = Depends(get_db)):
  result = models.Set_Vm_State(db ,vmstat = vmstat)
  if result['message'] == 'success':
    return resp_200(result['data'])
  else:
    return resp_400(404,[],result['message'])

#---------------------------------statistics API-----------------------------
@app.get("/getvmnetotal/{id}")
async def fetch_vmnet_total(id: str, db: Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Fetch_Vmnet_Total(db ,id = id)
  return result

@app.get("/statistic/{zone}")
async def fetch_statistic(zone: str, db:Session = Depends(get_db), username: str = Depends(check_token)):
  result = models.Fetch_Statistic(db,  user = username['username'], priv = int(username['priv']), zone = zone)
  return result
