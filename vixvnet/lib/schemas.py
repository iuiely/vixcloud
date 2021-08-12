from typing import List,Dict
from pydantic import BaseModel

###-------- Network -------------###
class NetName(BaseModel):
  network:str

class RespNetInfo(BaseModel):
  code:int
  message:str = None
  data:List[NetName] = None
  class Config:
    orm_mode = True

class CreateNetwork(BaseModel):
  name: str
  zone:int
  mode: str
  vlanid: int = None
  swmode: int = None
  addr: str
  gateway: str
  dhcpool: str = None

class NetUser(BaseModel):
    id : int
    user:str

class NetPerm(BaseModel):
    id:int
    perm: str

class NetState(BaseModel):
    id:int
    state: str

class Networks(BaseModel):
  id:int
  name: str
  mode: str
  addr: str
  perm: str
  state: str
  run:str
  class Config:
    orm_mode = True

class RespNetworks(BaseModel):
  count:int
  data:List[Networks] = None
  class Config:
    orm_mode = True

class RespNetsList(BaseModel):
  id:int
  name: str
  class Config:
    orm_mode = True

class IpMac(BaseModel):
  ip:str
  mac:str
  class Config:
    orm_mode = True

class AssignIPMAC(BaseModel):
  name: str
  brname:str
  vlanid:int
  mode:str
  gateway:str
  ipmac:List[IpMac] = None
  class Config:
    orm_mode = True

class VmUsedNet(BaseModel):
    name: str
    brname:str
    vlanid:int
    mode:str
    gateway:str
    class Config:
        orm_mode = True

class RecycleIp(BaseModel):
    brname:str
    ip:str

class NetworkDetail(BaseModel):
  id: int
  name: str
  user: str
  mode: str
  vlanid: int
  addr: str
  gateway: str
  brname: str
  nsname: str
  vethi: str
  vetho: str
  dhcpool: str = None
  dhcptb: str
  perm: str
  run: str
  state: str
  create_time: str
