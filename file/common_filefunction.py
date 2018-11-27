# -*-encoding:utf-8 -*-
'''
    @Time    : 2018/5/16
    @Author  : LiuXueWen
    @Site    :
    @File    : fileoperation_common.py
    @Software: PyCharm
    @Description: 对路径进行的一些操作。包含以下功能：1.判断路径是否存在 2.判断文件夹是否为空 3.是否创建文件夹 4.复制文件夹内容 5.重命名文件夹或文件
'''

import os
import getpass
import shutil
import time

# 获取当前系统用户名
# user_name = getpass.getuser()
# 获取系统桌面目录
# desktop_dir = 'C:\Users\\' + user_name + '\Desktop'

# path = desktop_dir + '\\new'

# 判断路径是否存在
def isexists(path):
   if os.path.exists(path):
      print('你的电脑桌面存在名为new文件夹')
   else:
      print('你的电脑桌面不存在名为new文件夹')

# 判断文件夹是否为空
def isListdir(path):
   if len(os.listdir(path)) == 0:
      print('empty')
   else:
      print('not empty')

# 是否创建文件夹
def isMakedir(path):
   os.mkdir(path)

# 复制内容到新的文件夹下
def isCopy(desktop_dir):
   # 待复制的文件夹路径
   src = desktop_dir + '\old'
   # 新的复制后的文件夹路径
   dst = desktop_dir + '\new'
   # 执行复制功能
   # shutil.copytree(src, dst, symlinks=False, ignore=None)
   shutil.copytree(src, dst)

# 重命名文件夹或文件
def renameDir(desktop_dir):
   old = desktop_dir + '\old.txt'
   new = desktop_dir + '\new.txt'
   os.renames(old, new)

# 移动目录或文件
def moveDirOrFile(desktop_dir):
   src = desktop_dir + '\old.txt'
   dst = desktop_dir + '\new'
   shutil.move(src, dst)

# 清空指定的非空目录
def removeFile(path):
   for root, dirs, files in os.walk(path, False):
      for name in files:
         os.remove(os.path.join(root, name))
      for name in dirs:
         os.rmdir(os.path.join(root, name))


# 清空指定的目录树（包含子目录结构）
def removeAllFile(path):
   # shutil.rmtree(path[, ignore_errors[, onerror]])
   shutil.rmtree(path)

# 清空指定目录下的所有文件及文件夹，但保留文件夹结构
def removeFiles(path):
   if os.path.getsize(path) == 0:
      return
   else:
      # 遍历当前路径下的所有内容
      for files in os.listdir(path):
         fileFullPath = path + "/" + files
         # 判断如果当前路径是文件则执行删除文件操作
         if os.path.isfile(fileFullPath):
            os.remove(fileFullPath)
         elif os.path.isdir(fileFullPath):
            # 判断当前路径是文件夹的时候则执行删除文件夹的操作
            shutil.rmtree(fileFullPath)

def getfileinfo(path):
    """
    获取文件信息 文件名，文件大小，文件行数，日期，文件创建日期
    :param path: 完整文件路径
    :return: 文件信息对象
    """
    # 获取文件名
    filename = os.path.basename(path)
    # 获取文件大小
    filesize = os.path.getsize(path)
    # 获取文件行数
    count = 0
    thefile = open(path, 'rb')
    while True:
        buffer = thefile.read(8192 * 1024)
        if not buffer:
            break
        count += buffer.count('\n')
    thefile.close()
    # 获取文件生成日期
    timeStruct = time.localtime(os.path.getmtime(path))
    filecreatdate = time.strftime('%Y%m%d%H%M%S', timeStruct)
    fileinfo = {}
    fileinfo["filename"] = filename
    fileinfo["filesize"] = filesize
    fileinfo["filecount"] = count
    fileinfo["filecreatdate"] = filecreatdate
    return fileinfo