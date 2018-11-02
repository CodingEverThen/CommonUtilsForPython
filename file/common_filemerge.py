# -*-encoding:utf-8 -*-

'''
    @Time    : 2018/5/16
    @Author  : LiuXueWen
    @Site    :
    @File    : mergefile.py
    @Software: PyCharm
    @Description: 文件合并功能模块（合并指定路径下当前日期前一天的文件夹中的文件）
'''

import os
import common_filefunction
import time

class properties():
    fileFullPath3 = ""
    local_path = ""

# import properties

# 设置需要合并的文件路径
# 手动输入目标地址路径
# fileFullPath = r"%s" % raw_input("File base path: ").strip("\"")
# 指定读取输入和输出目标路径地址
fileFullPath3 = properties.fileFullPath3
local_path = properties.local_path
# 设置需要合并的本地文件路径
# fileFullPath3 = "/root/LXW/new/"
# # 设置本地文件合并后的输出路径
# local_path = "/root/LXW/dat/"
# print len(os.listdir(fileFullPath3))
# 当前时间节点的时间戳
todaytrim = time.time()
# 生成13位毫秒级的时间戳
current_milli_time = int(round(time.time() * 1000))

# 获取当前日期并格式化
todaydate = time.strftime("%Y%m%d", time.localtime())
# todaydate = "20180516"

# 读取文件整体大小
def getFileSize(file):
    file.seek(0, os.SEEK_END)

    fileLength = file.tell()

    file.seek(0, 0)
    # print("文件总长度：" + str(fileLength))
    # 返回文件总长度
    return fileLength

# 查找实际文件路径，文件总数
def rebuildFile():
    '''
        @files: fileFullPath3 下的所有文件和文件夹名称
        @file2: files集合下遍历的每一个名称
        @file3:
        @file4: 当file2 是文件夹的情况下，遍历该文件夹下的所有文件
        @fileFullPath: 遍历所有情况下得到的实际目标路径地址（\new\'realpath'）
        @fileFullPath3: 设置需要合并的源目标路径
        @local_path: 设置合并后的目标路径
    '''

    # 判断指定的\new文件夹下是否为空，为空则不处理
    if len(os.listdir(fileFullPath3)) == 0:
        print("null")
    else:
        # 若文件夹不为空则执行以下操作
        # 得到文件夹下的所有文件或文件夹的名称
        files = os.listdir(fileFullPath3)
        # print(files)
        for file2 in files:  # 遍历文件夹
            # 如果是文件夹则加上该地址成为实际路径
            # 获取实际需要读取的目标路径
            fileFullPath = fileFullPath3 + file2
            # print "fileFullPath:" + fileFullPath
            # 判断是否为文件夹，若为文件夹则执行下一步，否则跳过
            if os.path.isdir(fileFullPath):
                # 循环读取所有文件夹下的文件
                # print("fileFullPath----"+fileFullPath)
                #  获取文件的数量
                divideTotalPartsCount = len(os.listdir(fileFullPath))

                for file4 in os.listdir(fileFullPath):
                    # print("file4----"+file4)
                    # 设置读取的文件名称格式为utf-8
                    # file = file.decode('utf-8')
                    # 判断文件名是否符合要求，文件名一致的则执行合并功能
                    # 以_下划线拆分成不同的字段，匹配字段值是否一致，根据匹配的字段值进行下一步操作
                    filelist = file4.split("_")
                    # print(filelist)
                    # 将文件列表、文件数量、实际路径地址返回到外部
                    return filelist,divideTotalPartsCount,fileFullPath,file4
            # 判断如果是文件类型则直接删除
            elif os.path.isfile(fileFullPath):
                common_filefunction.removeFile(fileFullPath)

# 判断文件类型和名称是否一致并操作
def ChoiseRes():
    res = rebuildFile()
    filelist = res[0]
    # print(res)
    divideTotalPartsCount = res[1]
    # 循环判断当前文件夹下所有的文件，判断结束  所有的文件后退出循环
    # 根据指定的格式判断是否为同一个类型的文件，若为一致则执行合并操作，否则返回false
    for i in range(0, divideTotalPartsCount):
        # 系统中心
        if (filelist[0] == "i" or filelist[0] == "a") and filelist[1] == "xtzx" and filelist[3] == todaydate:
            MergeFile()
            print("xtzx Merge successed !")
        # 渠道中心
        elif (filelist[0] == "i" or filelist[0] == "a") and filelist[1] == "qdzx" and filelist[3] == todaydate:
            MergeFile()
            print("qdzx Merge successed !")
        # 产品中心
        elif (filelist[0] == "i" or filelist[0] == "a") and filelist[1] == "cpzx" and filelist[3] == todaydate:
            MergeFile()
            print("cpzx Merge successed !")
        # 企业发展部
        elif (filelist[0] == "i" or filelist[0] == "a") and filelist[1] == "qyfz" and filelist[3] == todaydate:
            MergeFile()
            print("qyfz Merge successed !")
        # 内容中心
        elif (filelist[0] == "i" or filelist[0] == "a") and filelist[1] == "nrzx" and filelist[3] == todaydate:
            MergeFile()
            print("nrzx Merge successed !")
        # 运营中心
        elif (filelist[0] == "i" or filelist[0] == "a") and filelist[1] == "yyzx" and filelist[3] == todaydate:
            MergeFile()
            print("yyzx Merge successed !")
        # 若全部不满足则执行下面的语句
        else:
            print("没有满足条件的文件")
            return False

# 合并功能操作代码
def MergeFile():

    res = rebuildFile()
    filelist = res[0]
    divideTotalPartsCount = res[1]
    fileFullPath = res[2]

    fileNewName = filelist[0] + "_" + filelist[1] + "_" + filelist[2] + "_" + todaydate + "_" + filelist[4] + "_" + str(current_milli_time) + ".dat"

    # 读取文件操作
    file = open(local_path + fileNewName, "wb")

    for i in range(0,divideTotalPartsCount):

        # 控制合并文件的后缀名
        filePartName = filelist[0] + "_" + filelist[1] + "_" + filelist[2] + "_" + todaydate + "_" + filelist[4] + "_." + str(i)

        # 注意：linux系统下拼接该路径不需要加/，在Windows下需要加上\\
        filePart = open(fileFullPath + "/" + filePartName, "rb")

        filePartSize = getFileSize(filePart)

        lengthWritten = 0

        # 循环读取规定格式的.dat文件并执行写入操作
        while lengthWritten < filePartSize:
            # 每次读取1k
            bufLen = 1024
            buf = filePart.read(bufLen)
            file.write(buf)
            lengthWritten += len(buf)

        # 判断文件是否存在，如果不存在则执行判断文件名的操作，否则继续合并
        if os.path.exists(fileFullPath + filePartName):
            continue
        filePart.close()
    # 返回生成的文件名用于判断
    return fileNewName
    file.close()
