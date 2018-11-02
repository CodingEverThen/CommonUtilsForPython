#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/7/16
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_csvconfig.py
    @Software: PyCharm
    @Description:
        对csv配置文件的读写操作
        配置内容采用 key:value 模式
"""
import csv

class csvconfig():
    def __init__(self,path,pip):
        '''
        :param path: 配置文件路径
        :param pip: 分隔符
        '''
        # 获取文件路径
        self.path = path
        # 注册文件分隔符
        csv.register_dialect("pipes",delimiter=pip)

    def get_json_value(self,keyword):
        '''
        :Description json 格式的配置文件数据获取
        :param keyword: 获取的指定 key 名称
        :return:
            1.指定 key 下的数据
            2.提示信息
        '''
        with open(self.path,"r") as cf:
            rows = csv.reader(cf,dialect="pipes")
            # 获取所有说句
            for row in rows:
                # 格式化json
                data = {
                    row[0]:row[1]
                }
                # 遍历 key
                for key in data:
                    # 判断 key 名称
                    if key == keyword:
                        # 返回对应的名称
                        return data[keyword]
                    else:
                        pass
            return "没有对应key的值!"

    def get_value(self):
        '''
        :return: 配置文件中所有信息组成的数组
        '''
        full_data = []
        with open(self.path,"r") as cf:
            rows = csv.reader(cf,dialect="pipes")
            # 获取所有说句
            for row in rows:
                full_data.append(row)
            return full_data

if __name__ == '__main__':
    name = csvconfig("test.csv",":").get_json_value("name")
    print(name)
    str = csvconfig("test.csv",":").get_value()
    print(str[0])