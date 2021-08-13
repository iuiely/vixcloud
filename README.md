# <p align="center">Vix-Cloud</p>
  Vix-Cloud Platform 是一个开源的基础私有云平台软件。  
  支持简单的虚拟机、虚拟网络、计算节点、系统镜像等统计功能  
  支持创建资源区域、虚拟网络、系统镜像、虚拟机等功能  
  演示视频地址： https://www.bilibili.com/video/BV1so4y1U7xL
## 环境要求
  redis > 5.0.10  
  mysql > 8.0.20  
  python 3.6  
## 快速使用 ： 安装和配置
##### 1、安装kvm依赖
  用centos8.x为例  
```
yum -y install qemu-kvm libvirt qemu-kvm-common virt-manager virt-viewer virt-install libcgroup libcgroup-tools python3 python36-devel libvirt-devel ncurses-compat-libs
```
##### 2、下载云平台软件
```
git clone https://github.com/iuiely/vixcloud.git  
```
##### 3、安装和创建mysql数据库  
```
create database vixsso default character set utf8mb4 collate utf8mb4_bin;  
create database vixvnet default character set utf8mb4 collate utf8mb4_bin;  
create database vixdhcp default character set utf8mb4 collate utf8mb4_bin;  
create database vixcore default character set utf8mb4 collate utf8mb4_bin;  
```
##### 4、安装和配置redis数据库
  略  
##### 5、安装python依赖包
```
pip3 install -r requirement.txt  
```
##### 6、安装nodejs和pm2及pm2启动脚依赖包(可选）
```
npm install -g express --registry=https://registry.npm.taobao.org  
npm install -g compression --registry=https://registry.npm.taobao.org  
npm install -g chalk --registry=https://registry.npm.taobao.org  
切换到vixportal目录
npm link  express
npm link compression
npm link chalk
```
##### 7、配置libvirt（libvirt必须启动）
  略
##### 8、配置vixsso
  vixsso是云平台的用户认证管理模块，在mysql数据库初始化完成后才能执行  
  1. 添加超级管理员步骤  
  编辑vixsso目录中的admin-user文件， 
```
export USERNAME=admin  
export PASSWORD=123456  
export DOMAIN_NAME=default  
export SSO_DB=mysql+pymysql://root:123456@192.168.100.55:3306/  
```
  USERNAME是超级管理员的用户名  
  PASSWORD是超级管理员的密码  
  DOMAIN_NAME在基础版中可忽略  
  SSO_DB是mysql数据库的连接地址  
  执行脚本  
```
  python3 init-vixsso  
```
  2. 修改conf/vixsso.conf文件，配置SSO访问  
```
[database]  
connection = mysql+pymysql://root:123456@192.168.100.55:3306/vixsso?charset=utf8mb4  

[redis]  
connection = redis://:123456@192.168.100.55:6379  

[logs]  
file = logs/vixsso.log  

```
  [database]的connection是用户登录的mysql数据库连接地址  
  [redis]的connection是用户登录的redis数据库连接地址  
  [logs]的file是日志文件保存位置  
##### 9、配置vixcore  
  vixcore是云平台的资源调度模块，在mysql数据库初始化完成后才能运行  
  修改conf/vixcore.conf文件，配置资源调度  
```
[database]  
connection = mysql+pymysql://root:123456@192.168.100.55:3306/vixcore?charset=utf8mb4  

[redis]  
redis_connection = redis://:123456@192.168.100.55:6379  

[image]  
store = /opt/vixstack/vixcloud/vixcore/store  
cache = /cloud/cache  

[vnet]  
url = http://192.168.100.55:4203  

[store]  
mode = local  

[console]  
listen = 0.0.0.0  
port = 6080  

[netdevice]  
keydir = netdevice/key  
cmdir = netdevice/cmd  

[logs]  
file = /opt/vixstack/vixcloud/vixcore/logs/vixcore.log  
```
  [database]的connection是连mysql的连接地址  
  [redis]的redis_connection是redis的连接地址  
  [image]的store是系统镜像的存储路径目录  
  [image]的cache是系统镜像在计算节点的缓存存储路径  
  [vnet]的url是虚拟网络模块的连接地址  
  [console]的listen是控制台的代理监听地址  
  [console]的port是控制台的代理监听端口  
  其它选项不要修改，已写死  
##### 10、配置vixnet  
  vixvnet是云平台的虚拟网络模块，虚拟网络分为server端和agent端，在mysql数据库初始化完成后才能运行  
  修改conf/vixvnet.conf文件，配置虚拟网络  
```
[vnetdatabase]  
connection = mysql+pymysql://root:123456@192.168.100.55:3306/vixvnet?charset=utf8mb4  

[dhcpdatabase]  
connection = mysql+pymysql://root:123456@192.168.100.55:3306/vixdhcp?charset=utf8mb4  

[redis]  
connection = redis://:123456@192.168.100.55:6379  
 
[vnet]  
url = http://192.168.100.55:4203  

[core]  
url = http://192.168.100.55:4202  

[nic]  
physical_nic = enp3s0  
my_ip = 192.168.100.55  

[logs]  
server = logs/vixvnet-server.log  
agent = logs/vixvnet-agent.log  
```
  [vnetdatabase]的connection是虚拟网络的网络基本信息的mysql连接地址  
  [dhcpdatabase]的connection是虚拟网络的dhcp地址信息的mysql连接地址  
  [redis]的connection是虚拟网络的redis连接地址  
  [vnet]的url是虚拟网络的api访问地址  
  [core]的url是云平台的调度api访问地址  
  [nic]的physical_nic是虚拟网络节点的物理网卡监听设备  
  [nic]的my_ip是虚拟网络节点的物理网卡的IP地址  
  这2个配置选项决定了虚拟网络的地址，在当前的基础版本中只能创建普通网络，也就是傻瓜网络  
  [logs]的2个配置选项是日志文件保存地址  
##### 11、配置vixagnet  
  vixagent是云平台的计算节点代理服务程序，所有的计算节点都需要启动这个代理程序  
  修改conf/agent.conf文件，配置虚拟网络  
```
[redis]
connection = redis://:123456@192.168.100.55:6379

[nic]
physical_nic = enp3s0
my_ip = 192.168.100.55

[core]
url = http://192.168.100.55:4202

[ceph]
#mode open|close
mode = close
conf = /etc/ceph/ceph.conf
user = libvirt
secret = 6d5a42d6-ddde-42bf-b027-85722c22be47

[migrate]
pvkey = certificate/ssh_rsa
pwd = 
user = 
port = 

[logs]
file = logs/vixagent.log
```
  [redis]的connection是代理程序连接的redis服务器，云平台的所有redis服务器从理论上是同1个  
  [nic]的physical_nic是计算节点的物理网卡监听地址，所有的虚拟机的网络都要从这个网卡通过  
  [nic]的my_ip是计算节点的物理网卡IP地址  
  [core]的url配置是代理节点访问调度服务的地址  
  [ceph]的所有配置在基础版中无法使用，必须关闭  
  [migrate]的所有配置在基础版中无法使用，无须修改  
  [logs]的配置是agent的日志文件位置  
##### 12、配置vixportal
  vixportal是云平台的门户入口  
  修改portal/url.config.js文件，配置访问地址
```
url = {
  vneturl : "http://192.168.100.55:4203",
  coreurl : "http://192.168.100.55:4202",
  ssourl : "http://192.168.100.55:4201",
  vncproxy : "192.168.100.55",
  vncport : "6080",
}
```
  vneturl是虚拟网络的API接口地址  
  coreurl是调度程序的API接口地址  
  ssourl是用户认证的API接口地址  
  vncproxy和vncport是控制台的API接口地址
  
## 快速使用 ： 启动服务
##### 1、启动vixportal
  1. pm2启动  
```
  cd /{dir}/vixcloud/vixportal  
  pm2 start portal  
  
  访问端口：4210
```
  2. nginx或apache启动  
  略  
##### 2、启动vixsso
```
  cd /{dir}/vixcloud/vixsso  
  python3 bin/vixsso start -d  
```
##### 3、启动vixcore
```
  cd /{dir}/vixcloud/vixcore  
  python3 bin/vix-core start -d  
```
##### 4、启动vixconsole
```
  cd /{dir}/vixcloud/vixcore  
  python3 bin/vix-console start -d 
```
##### 5、启动vixvnet-server
```
  cd /{dir}/vixcloud/vixvnet  
  python3 bin/vixvnet-server start -d  
```
##### 6、启动vixvnet-agent
```
  cd /{dir}/vixcloud/vixvnet  
  python3 bin/vixvnet-agent start 
```
##### 7、启动vixagent
```
  cd /{dir}/vixcloud/vixagent
  python3 bin/vixagent start
```

  
 
