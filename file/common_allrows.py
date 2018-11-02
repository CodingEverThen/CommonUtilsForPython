#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/7/4
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_allrows.py
    @Software: PyCharm
    @Description: 统计指定路径下的所有文件的总行数
"""
import os

class allrows():
    def __init__(self,path):
        # 获取统计代码的文件夹路径
        self.path = path

    def count(self):
        count_num = 0
        for file in os.listdir(self.path):
            # 获取完整的文件路径
            full_file_path = os.path.join(self.path,file)
            # 遍历打开文件
            with open(full_file_path,"r+") as f:
                file_readlines = f.readlines()
                i = 0
                for line in file_readlines:
                    i = i+1
                count_num = count_num + i
        print(count_num)

if __name__ == '__main__':
    allrows("C:\\Users\Carol\Desktop\code").count()