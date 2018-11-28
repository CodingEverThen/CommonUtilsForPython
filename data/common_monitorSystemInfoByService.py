#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/11/27
    @Author  : LXW
    @Site    : 
    @File    : common_monitorSystemInfoByService.py
    @Software: PyCharm
    @Description: 监控指定服务的所有进程的相关系统信息并写入到文件中
"""
import os
import psutil
import traceback
import threading
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool
import time
import sys
import json

# 兼容python2.7上多线程的bug，不加上下面的反代理程序不能正常执行
def proxy(cls_instance):
    return cls_instance.multiprocess_thread()
def proxy2(cls_instance, pid):
    return cls_instance.monitorInfo(pid)

def getCurrentTime():
    today = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    return today

class PidMonitor():
    def __init__(self, root_path, res_path):
        """
        初始化
        :param root_path: 监控的服务所在目录的路径
        :param res_path: 生成的信息保存路径文件夹
        """
        # 初始化进程号数组
        self.pids = []
        # 构造字典保存对应信息
        self.name_pid = {}
        # 扫描指定路径下全部的pid文件中的第一行进程号信息并保存在pids数组中
        for dirs in os.listdir(root_path):
            dir_path = os.path.join(root_path, dirs)
            if os.path.isdir(dir_path):
                for files in os.listdir(dir_path):
                    f_p = str(files).split(".")
                    if len(f_p) == 2 and f_p[1] == "pid" and os.path.isfile(os.path.join(dir_path, files)):
                        with open(os.path.join(dir_path, files), "rb+") as rf:
                            rb = rf.readline()
                            self.name_pid[rb.replace("\n", "")] = f_p[0]
                            self.pids.append(int(rb))
        # 创建文件夹
        if not os.path.exists(res_path):
            os.makedirs(res_path)
        self.res_path = res_path
        self.info = psutil.virtual_memory()


    # 多进程执行程序
    def multiProcessingMonitorPid_main(self):
        try:
            # 创建进程池
            p = Pool()
            # 参数末尾必须加上逗号
            p.apply_async(proxy, args=(self,))
            p.close()
            p.join()
        except Exception as e:
            traceback.print_exc()

    # 每个进程下的多线程执行，线程数等于当前机器的核数
    def multiprocess_thread(self):
        try:
            # 创建线程锁
            lock = threading.RLock()
            lock.acquire()
            # 获取每个文件
            for pid in self.pids:
                # 多线程
                p = ThreadPool()
                # 执行线程
                p.apply_async(proxy2, args=(self, pid,))
                p.close()
                p.join()
        except Exception as e:
            traceback.print_exc()
        finally:
            # 释放线程锁
            lock.release()

    # 每个进程的监控信息
    def monitorInfo(self, pid):
        """
        监控每个进程号的相关内存和CPU使用信息
        :param pid: 进程号
        """
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
        self.saveInfoToLocal(info=res, pid=pid)

    # 保存监控信息到本地
    def saveInfoToLocal(self, info, pid):
        """
        存储监控的信息到指定的路径下对应的进程号文件中
        :param info: 监控信息
        :param pid: 进程号
        """
        filename = self.name_pid.get(str(pid)) + ".log"
        fullPath = os.path.join(self.res_path, filename)
        # 创建对应服务名文件
        if not os.path.exists(fullPath):
            afile = open(fullPath, "wb+")
            afile.close()
        with open(fullPath, "ab+") as wf:
            wf.write(info+"\n")

if __name__ == '__main__':
    try:
        # 扫描路径 /data/v/app/app.pid
        root_path = "/data/v"
        # 生成信息保存路径
        res_path = "/data/v/PidMonitor/monitorLog"
        # 循环执行300次，每次间隔1秒
        for i in range(0, 300):
            PidMonitor(root_path=root_path, res_path=res_path).multiProcessingMonitorPid_main()
            time.sleep(1)
    except Exception as e:
        print(e)
        traceback.print_exc()
    finally:
        sys.exit(0)

