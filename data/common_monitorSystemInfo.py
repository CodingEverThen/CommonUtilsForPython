#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/11/27
    @Author  : LXW
    @Site    : 
    @File    : common_monitorSystemInfo.py
    @Software: PyCharm
    @Description: 监控指定的pid进程的相关系统信息并写入到文件中
"""
import os
import psutil
import traceback
import threading
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import time
import sys

# 兼容python2.7上多线程的bug，不加上下面的反代理程序不能正常执行
def proxy(cls_instance, path):
    return cls_instance.multiprocess_thread(path)
def proxy2(cls_instance, pid, path):
    return cls_instance.monitorInfo(pid, path)

def getCurrentTime():
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return today

class PidMonitor():
    def __init__(self, *args):
        self.pids = []
        for arg in args:
            self.pids.append(arg)
        self.info = psutil.virtual_memory()

    # 多进程执行程序
    def multiProcessingMonitorPid_main(self, path):
        try:
            # 创建进程池
            p = Pool()
            # 参数末尾必须加上逗号
            p.apply_async(proxy, args=(self, path,))
            p.close()
            p.join()
        except Exception as e:
            traceback.print_exc()

    # 每个进程下的多线程执行，线程数等于当前机器的核数
    def multiprocess_thread(self, path):
        try:
            # 创建线程锁
            lock = threading.RLock()
            lock.acquire()
            # 获取每个文件
            for pid in self.pids:
                # 多线程
                p = ThreadPool()
                # 执行线程
                p.apply_async(proxy2, args=(self, pid, path,))
                p.close()
                p.join()
        except Exception as e:
            traceback.print_exc()
        finally:
            # 释放线程锁
            lock.release()

    # 每个进程的监控信息
    def monitorInfo(self, pid, path):
        psClient = psutil.Process(pid=pid)
        memery_total = "内存总量:{memeryTotal} MB".format(memeryTotal=self.info.total/(1024*1024))
        memery_use = "内存使用量:{memeryUse} MB".format(memeryUse=psClient.memory_info().rss/(1024*1024))
        memery_percent = "内存使用率:{memeryPercent}%".format(memeryPercent=self.info.percent)
        cpu_total = "CPU总数:{cpu_total} 核".format(cpu_total=psutil.cpu_count())
        cpu_percent = "CPU使用率:{cpu_percent}%".format(cpu_percent=psutil.cpu_percent())
        info = "{memery_total}, {memery_use}, {memery_percent}, {cpu_total}, {cpu_percent}".format(
            memery_total=memery_total,
            memery_use=memery_use,
            memery_percent=memery_percent,
            cpu_total=cpu_total,
            cpu_percent=cpu_percent)
        res = ("{currentTime} PID:{pid} >>>>>> {memeryInfo}".format(currentTime=getCurrentTime(), pid=pid, memeryInfo=info))
        print(res)
        self.saveInfoToLocal(path=path, info=res, pid=pid)

    # 保存监控信息到本地
    def saveInfoToLocal(self, path, info, pid):
        filename = str(pid)+".log"
        fullPath = os.path.join(path, filename)
        if not os.path.exists(path):
            os.makedirs(path)
        elif not os.path.exists(fullPath):
            afile = open(fullPath, "wb+")
            afile.close()
        with open(fullPath, "ab+") as wf:
            wf.write(info+"\n")

if __name__ == '__main__':
    try:
        for i in range(0, 600):
            PidMonitor(7611, 7737).multiProcessingMonitorPid_main("/data/v/PidMonitor/monitorLog")
            time.sleep(1)
    except Exception as e:
        traceback.print_exc()
    finally:
        sys.exit(0)

