# -*-encoding:utf-8 -*-
'''
    @Time    : 2018/5/16
    @Author  : LiuXueWen
    @Site    :
    @File    : fileoperation_common.py
    @Software: PyCharm
    @Description: 文件拆分功能。用于拆分单个文件为多个子文件
'''


import os

import sys

import threading
 
# 获取文件整体大小
def getFileSize(file):

    file.seek(0, os.SEEK_END)

    fileLength = file.tell()

    file.seek(0, 0)

    return fileLength
 

def divideFile():
    
    # 控制需要拆分的文件的绝对路径位置
    fileFullPath = r"%s" % raw_input("File path: ").strip("\"")

    # 控制拆分文件的数量大小
    divideTotalPartsCount = int(raw_input("How many parts do you like to divide?: "))

    if os.path.exists(fileFullPath):

        file = open(fileFullPath, 'rb')

        fileSize = getFileSize(file)

        file.close()

        # send file content

        for i in range(divideTotalPartsCount):

            filePartSender = threading.Thread(target=seperateFilePart, args=(fileFullPath, divideTotalPartsCount, i + 1, fileSize))

            filePartSender.start()

        for i in range(divideTotalPartsCount):

            sem.acquire()

        os.remove(fileFullPath)

    else:

        print "File doesn't exist"
 

def seperateFilePart(fileFullPath, divideTotalPartsCount, threadIndex, fileSize):

    try:

        # calculate start position and end position

        filePartSize = fileSize / divideTotalPartsCount

        startPosition = filePartSize * (threadIndex - 1)

        # print "Thread : %d, startPosition: %d" % (threadIndex, startPosition)

        endPosition = filePartSize * threadIndex - 1

        if threadIndex == divideTotalPartsCount:

            endPosition = fileSize - 1

            filePartSize = fileSize - startPosition

        file = open(fileFullPath, "rb")

        file.seek(startPosition)

        filePartName = fileFullPath + ".part" + str(threadIndex)

        filePart = open(filePartName, "wb")

        lengthWritten = 0

        while lengthWritten < filePartSize:

            bufLen = 1024

            lengthLeft = filePartSize - lengthWritten

            if lengthLeft < 1024:

                bufLen = lengthLeft

            buf = file.read(bufLen)

            filePart.write(buf)

            lengthWritten += len(buf)

        filePart.close()

        file.close()

        sem.release()

        print "Part %d finished, size %d" % (threadIndex, filePartSize)

    except Exception, e:

        print e
    

sem = threading.Semaphore(0)

while True:

    divideFile()
