#!/usr/bin/env python3
# coding: utf-8

import os,sys,multiprocessing

path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

debug = True
daemon = True

bind = '0.0.0.0:4203'      # 绑定ip和端口号
backlog = 512                # 监听队列
chdir = path  # gunicorn要切换到的目的工作目录
timeout = 30      # 超时

worker_class = 'uvicorn.workers.UvicornWorker'

workers = 1  # 进程数
threads = 4 #指定每个进程开启的线程数
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# 如果使用service启动，这里的pid路径应与service的pid路径保持一致，否则无法启动

pidfile = 'logs/vixvnet.pid'
accesslog = 'logs/access.log'
errorlog = 'logs/error.log'
