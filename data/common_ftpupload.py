#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Time    : 2018/5/17
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_ftpupload.py
    @Software: PyCharm
    @Description: ftp自动下载、自动上传脚本，可以递归目录操作
'''

from ftplib import FTP
import os
import sys
import time
import socket


# 本地日志存储路径
local_log_path = "log.txt"

class MyFTP():
    def __init__(self, host, port):
        """
            初始化 ftp 客户端
                参数:
                    host:ip地址
                    port:端口号
        """
        # print("__init__()---> host = %s ,port = %s" % (host, port))

        self.host = host
        self.port = port
        self.ftp = FTP()
        # 重新设置下编码方式避免上传中文文件失败
        self.ftp.encoding = 'utf-8'
        # 设置日志log.txt生成路径，不设置默认在当前目录下
        self.log_file = open(local_log_path, "a")
        self.file_list = []
        # python的默认ftplib启用passive（被动模式），因为被动模式会启用1024之后的端口，所以就会出现问题，把passive模式取消后，就没问题了
        self.ftp.set_pasv(False)

    def login(self, username, password):
        """
            初始化 ftp 客户端
                参数:
                    username: 用户名
                    password: 密码
            """
        try:
            # 设置超时时间60s
            timeout = 60
            socket.setdefaulttimeout(timeout)
            # 0主动模式 1 #被动模式
            self.ftp.set_pasv(1)
            # 打开调试级别2，显示详细信息
            self.ftp.set_debuglevel(2)

            print('开始连接到 %s' % self.host)
            self.ftp.connect(self.host, self.port)
            print('成功连接到 %s' % self.host)

            print('开始登录到 %s' % self.host)
            self.ftp.login(username, password)
            print('成功登录到 %s' % self.host)

            print(self.ftp.welcome)
        except Exception as err:
            self.deal_error("ftp 连接或登录失败 ，错误描述为：%s " % err)
            print("ftp 连接或登录失败 ，错误描述为：%s " % err)
            pass

    def is_same_size(self, local_file, remote_file):
        """
            判断远程文件和本地文件大小是否一致
                参数:
                    local_file: 本地文件
                    remote_file: 远程文件
        """
        try:
            remote_file_size = self.ftp.size(remote_file)
        except Exception as err:
            self.debug_print("is_same_size() 错误描述为：%s" % err)
            remote_file_size = -1

        try:
            local_file_size = os.path.getsize(local_file)
        except Exception as err:
            self.debug_print("is_same_size() 错误描述为：%s" % err)
            local_file_size = -1

        print('local_file_size:%d  , remote_file_size:%d' % (local_file_size, remote_file_size))
        if remote_file_size == local_file_size:
            # return 1
            return
        else:
            return 0

    def download_file(self, local_file, remote_file):
        """
            从ftp下载文件
                参数:
                    local_file: 本地文件
                    remote_file: 远程文件
        """
        self.debug_print("download_file()---> local_path = %s ,remote_path = %s" % (local_file, remote_file))

        if self.is_same_size(local_file, remote_file):
            self.debug_print('%s 文件大小相同，无需下载' % local_file)
            return
        else:
            try:
                self.debug_print('>>>>>>>>>>>>下载文件 %s ... ...' % local_file)
                buf_size = 1024
                file_handler = open(local_file, 'wb')
                self.ftp.retrbinary('RETR %s' % remote_file, file_handler.write, buf_size)
                file_handler.close()
            except Exception as err:
                self.debug_print('下载文件出错，出现异常：%s ' % err)
                return

    def download_file_tree(self, local_path, remote_path):
        """
            从远程目录下载多个文件到本地目录
                参数:
                    local_path: 本地路径
                    remote_path: 远程路径
        """
        print("download_file_tree()--->  local_path = %s ,remote_path = %s" % (local_path, remote_path))
        try:
            self.ftp.cwd(remote_path)
        except Exception as err:
            self.debug_print('远程目录%s不存在，继续...' % remote_path + " ,具体错误描述为：%s" % err)
            return

        if not os.path.isdir(local_path):
            self.debug_print('本地目录%s不存在，先创建本地目录' % local_path)
            os.makedirs(local_path)

        self.debug_print('切换至目录: %s' % self.ftp.pwd())

        self.file_list = []
        # 方法回调
        self.ftp.dir(self.get_file_list)

        remote_names = self.file_list
        self.debug_print('远程目录 列表: %s' % remote_names)
        for item in remote_names:
            file_type = item[0]
            file_name = item[1]
            local = os.path.join(local_path, file_name)
            if file_type == 'd':
                print("download_file_tree()---> 下载目录： %s" % file_name)
                self.download_file_tree(local, file_name)
            elif file_type == '-':
                print("download_file()---> 下载文件： %s" % file_name)
                self.download_file(local, file_name)
            self.ftp.cwd("..")
            self.debug_print('返回上层目录 %s' % self.ftp.pwd())
        return True

    def upload_file(self, local_file, remote_file):
        """
            从本地上传文件到ftp
                参数:
                    local_path: 本地文件
                    remote_path: 远程文件
        """

        if not os.path.isdir(local_file):
            buf_size = 1024
            file_handler = open(local_file, 'rb')
            self.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
            size = os.path.getsize(local_file)
            file_handler.close()
            self.debug_print('上传: %s' % local_file + " 成功!文件大小： "+ str(size) +" Bytes.")
        else:
            print('%s 不是文件' % local_file)
            return
        if self.is_same_size(local_file, remote_file):
            print('跳过相等的文件: %s' % local_file)
            return


    def upload_All_file(self, local_path, remote_path):
        """
            从本地上传指定文件夹下的所有文件到ftp
                参数:
                    local_path: 本地文件路径
                    remote_path: 远程文件路径
        """
        if len(os.listdir(local_path)) == 0:
            print len(os.listdir(local_path))
            self.debug_print("指定的目录不存在或为空：%s" %local_path)
            print("指定的目录不存在或为空：%s" % local_path)
        else:
            for files in os.listdir(local_path):
                self.upload_file(local_path+"/"+files,remote_path+"/"+files)
                # self.upload_file(local_path + "\\" + files, remote_path + "/" + files)



    def upload_file_tree(self, local_path, remote_path):
        """
            从本地上传目录下多个文件到ftp
                参数:
                    local_path: 本地路径
                    remote_path: 远程路径
        """
        if not os.path.isdir(local_path):
            self.debug_print('本地目录 %s 不存在' % local_path)
            return

        self.ftp.cwd(remote_path)
        self.debug_print('切换至远程目录: %s' % self.ftp.pwd())

        local_name_list = os.listdir(local_path)
        for local_name in local_name_list:
            src = os.path.join(local_path, local_name)
            if os.path.isdir(src):
                try:
                    self.ftp.mkd(local_name)
                except Exception as err:
                    self.debug_print("目录已存在 %s ,具体错误描述为：%s" % (local_name, err))
                self.debug_print("upload_file_tree()---> 上传目录： %s" % local_name)
                self.upload_file_tree(src, local_name)
            else:
                self.debug_print("upload_file_tree()---> 上传文件： %s" % local_name)
                self.upload_file(src, local_name)
        self.ftp.cwd("..")

    def close(self):
        """
            退出ftp
        """
        print("close()---> FTP退出")
        self.ftp.quit()
        self.log_file.close()

    def debug_print(self, s):
        """
            打印日志
        """
        self.write_log(s)

    def deal_error(self, e):
        """
            处理错误异常
                参数：
                    e：异常
        """
        log_str = '发生错误: %s' % e
        self.write_log(log_str)
        sys.exit()

    def write_log(self, log_str):
        """
            记录日志
                参数：
                    log_str：日志
        """
        time_now = time.localtime()
        date_now = time.strftime('%Y-%m-%d %H:%M:%S', time_now)
        format_log_str = "%s ---> %s \r\n" % (date_now, log_str)
        print(format_log_str)
        self.log_file.write(format_log_str)

    def get_file_list(self, line):
        """
            获取文件列表
                参数：
                    line：
        """
        file_arr = self.get_file_name(line)
        # 去除  . 和  ..
        if file_arr[1] not in ['.', '..']:
            self.file_list.append(file_arr)

    def get_file_name(self, line):
        """
            获取文件名
                参数：
                    line：
        """
        pos = line.rfind(':')
        while (line[pos] != ' '):
            pos += 1
        while (line[pos] == ' '):
            pos += 1
        file_arr = [line[0], line[pos:]]
        return file_arr

    # 删除指定的ftp上的文件
    def remove_log(self,path):
        self.ftp.delete(path)

    # upload log.txt
    def upload_log_file(self, local_file, remote_file):
        """
            从本地上传文件到ftp
                参数:
                    local_path: 本地文件
                    remote_path: 远程文件
        """

        if not os.path.isdir(local_file):
            buf_size = 1024
            file_handler = open(local_file, 'rb')
            self.ftp.storbinary('STOR %s' % remote_file, file_handler, buf_size)
            size = os.path.getsize(local_file)
            file_handler.close()
            print('上传: %s' % local_file + " 成功!文件大小： "+ str(size) +" Bytes.\n")
        else:
            print('%s 不是文件' % local_file)
            return
        if self.is_same_size(local_file, remote_file):
            print('跳过相等的文件: %s' % local_file)
            return

    # 判断ftp服务器上是否存在指定的文件夹,不存在则创建
    def ftp_dirs_exists(self,root_path, dir_name):
        # 遍历目标地址下所有文件信息
        ftplist = self.ftp.nlst(root_path)
        # 拼接需要的路径地址
        real_path_dir = root_path + "/" + dir_name
        # 判断该路径地址下是否存在文件夹，若不存在则创建指定格式的文件夹
        if len(ftplist) == 0:
            self.ftp.mkd(real_path_dir)
        else:
            # 遍历指定路径下非空文件夹下的所有文件信息
            for dirs_name in ftplist:
                # 如果指定路径下的文件夹信息和规定的文件夹信息一致，则不操作
                if dirs_name == (real_path_dir):
                    return
                else:
                    # 否则创建规定的文件夹
                    self.ftp.mkd(real_path_dir)

if __name__ == '__main__':
    my_ftp = MyFTP("10.25.246.58",21)
    my_ftp.login("migulog","migulog")
    my_ftp.ftp_dirs_exists("/ftproot/migulog/data","20180528")

