# -*- coding: utf-8 -*-
# Project  : app
# File     : config.py
# Author   : csc
# Version  : v1.0
# Email    : chenshuchuan@xroom.net
# Date     : 2022-06-17 11:51
# Remarks  :
import multiprocessing
from app import settings

# 监听内网端口8000
bind = f"{settings.app.host}:{settings.app.port}"
# 并行工作进程数
# workers = multiprocessing.cpu_count() * 2 + 1
workers = 2
# 每个进程开启的线程数
threads = 2
# 监听队列
backlog = 2048
# 工作模式协程。
worker_class = "uvicorn.workers.UvicornWorker"
# 设置守护进程,将进程交给supervisor管理
daemon = 'false'
# worker_connections最大客户端并发数量，默认情况下这个值为1000。
worker_connections = 2048
# 设置日志记录水平
loglevel = 'info'
