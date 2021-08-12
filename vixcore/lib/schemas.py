from typing import List,Dict
from pydantic import BaseModel

###-------- Zone -------------###
class NewZone(BaseModel):
  zone: str
  desc: str = None

  class Config:
    orm_mode = True

class SetZoneState(BaseModel):
  id:int
  state:int

class SetZonePool(BaseModel):
  id:int
  zone:str
  mode:str
  path:str

class Zone(BaseModel):
  id:int
  zone:str
  nodes:int
  state:int
  
class Zones(BaseModel):
  id:int
  nodes:int
  zone:str
  state:int
  mode:str
  class Config:
    orm_mode = True

class RespZones(BaseModel):
  count:int
  data:List[Zones] = None
  class Config:
    orm_mode = True

class ZoneInfo(BaseModel):
  zone:str = None
  class Config:
    orm_mode = True

class RespZoneInfo(BaseModel):
  code:int
  data:List[ZoneInfo] = None
  message:str
  class Config:
    orm_mode = True

###-------- Node -------------###
class CreateNode(BaseModel):
  addr:str
  zone:str

class SetNodeState(BaseModel):
  id: int = None
  addr:str = None
  state:str

class SetNodeCpu(BaseModel):
  id:int
  cpu:int

class SetNodeMem(BaseModel):
  id:int
  mem:int

class SetNodePoolSize(BaseModel):
  addr:str
  pool:str
  size:int

class ZoneNodes(BaseModel):
  id:int
  node:str
  addr:str
  state:str
  status:str

class RespZoneNodes(BaseModel):
  count:int
  data:List[ZoneNodes] = None

class Nodes(BaseModel):
  id:int = None
  zone:str
  node:str = None
  addr:str
  state:str
  cpu:str
  mem:int
  class Config:
    orm_mode = True

class Node(BaseModel):
  addr:str

class RespNodeInfo(BaseModel):
  code:int
  message:str
  data:List[Node] = None

###----- Network Device ------###
class CreateNetDevice(BaseModel):
  mfrs:str
  addr:str
  devmode:str
  authmode:str
  devport:int = None
  authuser:str
  authpwd:str = None
  authkey:str = None
  zone:str

class SetNetDevState(BaseModel):
  id: int = None
  addr:str = None
  state:str

class SetNetDevPwd(BaseModel):
  id:int = None
  addr:str
  authuser:str
  authmode:str
  authpwd:str = None
  authkey:str = None

class DeviceCmd(BaseModel):
  id:int = None
  addr:str = None
  cmdmode:str = None
  cmd:str

class RespNetDeviceCmdContent(BaseModel):
  addr:str
  cmd:List = None
  cmdfile:str  

class NetworkDevice(BaseModel):
  addr:str
class RespNetworkDevice(BaseModel):
  code:int
  message:str
  data:List[NetworkDevice] = None
  class Config:
    orm_mode = True

class Cmds(BaseModel):
  cmds:List = None

class RespVlanCmds(BaseModel):
  mfrs:str
  addr:str
  port:int
  authmode:str
  authuser:str
  authpwd:str = None
  authfile:str = None
  cmds:List = None

###-------- Image ------------###
class ImagePerm(BaseModel):
  id:int
  perm:str

class Image(BaseModel):
  image:str

class RespImageInfo(BaseModel):
  code:int
  message:str
  data:List[Image] = None

class OSImages(BaseModel):
  id:int
  image:str
  sn:str
  desc:str
  perm:str = None

class RespOSImages(BaseModel):
  count:int
  data: List[OSImages] = None
  class Config:
    orm_mode = True

class RespImage(BaseModel):
  user:str
  image:str
  sn:str
  perm:str
  size:int
  path:str
  desc:str
  create_time:str
  class Config:
    orm_mode = True   

class ImageUser(BaseModel):
    id:int
    user:str

###-------- Pool ---------###
class ZonePool(BaseModel):
  zone:str

###-------- Volume ------------###
class CreateVolume(BaseModel):
    nodepool:str
    storepool:str
    vol_size:int

class UpdateVolSize(BaseModel):
    id:int
    vol_size:int
class UpdateVolVms(BaseModel):
    id:int
    vms:str

class SetVolToVm(BaseModel):
  id:int
  vm:str

class Re_Sup_Vol_a(BaseModel):
    id:int
    vol_name:str = None
    nodepool:str = None
    storepool:str = None
    vol_size:int = None
    vol_user:str = None
    vol_path:str = None
    vol_mode:str = None
    vol_format:str = None
    
    class Config:
        orm_mode = True

class Re_Gue_Vol_a(BaseModel):
    id:int
    vol_name:str = None
    nodepool:str = None
    storepool:str = None
    vol_size:int = None
    vol_user:str = None
    vol_mode:str = None
    vol_format:str = None
    
    class Config:
        orm_mode = True

class Volumes(BaseModel):
  id:int
  node:str = None
  volume:str = None
  dev:str = None
  size:int = None
  mode:str = None
  vm:str = None
  class Config:
    orm_mode = True

class respVolumes(BaseModel):
  count:int
  data:List[Volumes] = None
  class Config:
    orm_mode = True

class ReCreateDelVol(BaseModel):
    id:int

    class Config:
        orm_mode = True

#----------- VM ---------------#
class CreateVM(BaseModel):
  desc:str
  zone:int
  vcpu:int
  vmem:int
  image:int
  network:int
  ossize:int
  datasize:int = None

class AddVmNet(BaseModel):
  vmid:int
  network:int

class DelVmNet(BaseModel):
  id:int
  netname:str
  brname:str

class Vmconfig(BaseModel):
  id:int
  vm_name:str
  vm_des:str
  vm_osdisk_size:int
  vm_vcpu:int
  vm_vmem:int

class VmVcpu(BaseModel):
  id:int
  vcpu:int

class VmVmem(BaseModel):
  id:int
  vmem:int

class VmDiskSize(BaseModel):
  id:int
  dev:str
  disksize:int

class ReDelVm(BaseModel):
  id:int
  vm_name:str
  class Config:
    orm_mode = True

class VmUsedNets(BaseModel):
  id:int
  netname:str
  brname:str
  class Config:
    orm_mode = True

class ReVmUsedNets(BaseModel):
  code:int
  data:List[VmUsedNets]
  message:str
  class Config:
    orm_mode = True

class AddVmDisk(BaseModel):
  id:int
  disksize:int

class VolDev(BaseModel):
  dev:str

class ResponseVolDev(BaseModel):
  code:int
  message:str
  data:List[VolDev] = None
  class Config:
    orm_mode = True

class ResponseVmDisk(BaseModel):
  id:int
  vol_name:str
  vol_size:int
  vol_user:str
  vol_dev:str
  vol_format:str
  vm:str
  class Config:
    orm_mode = True

class RmVmDisk(BaseModel):
  id:int
  dev:str

class AttachVmDisk(BaseModel):
  id:int
  vm:str
  
class VmConvertImage(BaseModel):
  id:int
  desc:str
  image:str
  
class VmSysPwd(BaseModel):
  id:int
  pwd:str

class MigrateVm(BaseModel):
  id:int
  mode:str
  node:str

class SetVmState(BaseModel):
  vm:str
  node:str
  port:int = None
  state:int

class ConsoleInfo(BaseModel):
  vm:str
  vncpwd:str
  uuid:str

class RespConsoleInfo(BaseModel):
  code:int
  message:str
  data:List[ConsoleInfo] = None
  class Config:
    orm_mode = True

class VmInfo(BaseModel):
  vm:str = None

class RespVmInfo(BaseModel):
  code:int
  data:List[VmInfo] = None
  message:str
  class Config:
    orm_mode = True

