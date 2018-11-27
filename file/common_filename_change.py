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
    def __init__(self, path):
        """
            设置需要修改的文件夹路径
            :param path: 文件夹路径
        """
        self.path = path

    def change_name(self, str, index, name_split):
        """
            根据文件名下标修改文件名
            :param str: 修改后的字符串
            :param index: 需要修改的位置下标
            :param name_split: 拆分文件名的规则
        """
        for file_list in os.listdir(self.path):
            file_name_split = file_list.split(name_split)
            file_name_split[index] = str
            for i in range(len(file_name_split)):
                new_file_name = "_".join(file_name_split)
            print(new_file_name)
            os.rename(os.path.join(self.path,file_list),os.path.join(self.path, new_file_name))

    def change_name_by_name(self, index, name_splite, fix_name, buf_name):
        """
            :param index: 需要修改的字符串的位置
            :param name_splite: 拆分文件名的规则
            :param fix_name: 需要修改的字符串
            :param buf_name: 修改后的字符串
        """
        for file_list in os.listdir(self.path):
            file_name_splits = file_list.split(name_splite)
            for file_name_split in file_name_splits:
                if file_name_split == fix_name:
                    file_name_split = buf_name
                    file_name_splits[index] = file_name_split
            for i in range(len(file_name_splits)):
                new_file_name = "_".join(file_name_splits)
            print(new_file_name)
            os.rename(os.path.join(self.path, file_list), os.path.join(self.path, new_file_name))

if __name__ == '__main__':
    # filenamechange("C:\Users\Carol\Desktop\\tmp").change_name("20180819",3,"_")
    # filenamechange("C:\Users\Carol\Desktop\\tmp_ns").change_name_by_name(2,"_","pageview","00051")
    filenamechange("C:\Users\Carol\Desktop\\test").change_name("201810", 3, "_")
    filenamechange("C:\Users\Carol\Desktop\\test").change_name("dat", 1, ".")