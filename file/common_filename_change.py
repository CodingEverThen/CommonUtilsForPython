#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/6/28
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_filename_change.py
    @Software: PyCharm
    @Description:批量修改指定路径下所有文件的指定位置的名称
"""
import os
class filenamechange():
    '''
        path: 指定需要修改文件名称的路径
        str:指定修改的位置上需要替换的字符串内容
        index:指定需要修改的位置（下标）
    '''
    def __init__(self,path):
        self.path = path

    '''
        name_split:指定文件名称拆分的规则
    '''
    def change_name(self,str,index,name_split):
        for file_list in os.listdir(self.path):
            file_name_split = file_list.split(name_split)
            file_name_split[index] = str
            for i in range(len(file_name_split)):
                new_file_name = "_".join(file_name_split)
                print(new_file_name)
            os.rename(os.path.join(self.path,file_list),os.path.join(self.path,new_file_name))

    def change_name_by_name(self,index,name_splite,fix_name,buf_name):
        for file_list in os.listdir(self.path):
            file_name_splits = file_list.split(name_splite)
            for file_name_split in file_name_splits:
                if file_name_split == fix_name:
                    file_name_split = buf_name
                    file_name_splits[index] = file_name_split
            for i in range(len(file_name_splits)):
                new_file_name = "_".join(file_name_splits)
            print(new_file_name)
            os.rename(os.path.join(self.path,file_list),os.path.join(self.path,new_file_name))

if __name__ == '__main__':
    filenamechange("C:\Users\Carol\Desktop\\tmp").change_name("20180819",3,"_")
    # filenamechange("C:\Users\Carol\Desktop\\tmp_ns").change_name_by_name(2,"_","pageview","00051")