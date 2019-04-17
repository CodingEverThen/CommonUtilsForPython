#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2019/4/15
    @Author  : LXW
    @Site    : 
    @File    : LoggerUtil.py
    @Software: PyCharm
    @Description: 日志工具，默认保存文件在当前文件夹下
"""
import time
import sys
import os

def write(message):
    today = time.strftime("%Y%m%d", time.localtime(time.time()))
    file_name = "loggerInfo-"+today+".log"
    full_name = os.path.join(os.getcwd(), "logs", file_name)
    if not os.path.exists(os.path.dirname(full_name)):
        os.makedirs(os.path.dirname(full_name))
    if not os.path.exists(full_name):
        logfile = open(full_name, "w")
    else:
        logfile = open(full_name, "a")
    logfile.write(message+"\n")
    print(message)

def info(info):
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    message = "{time} INFO >>>>>> {desc}".format(time=str(today), desc=info)
    write(message)

def error(info):
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    message = "{time} ERROR >>>>>> {desc}".format(time=str(today), desc=info)
    write(message)

def debug(info):
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    message = "{time} DEBUG >>>>>> {desc}".format(time=str(today), desc=info)
    write(message)