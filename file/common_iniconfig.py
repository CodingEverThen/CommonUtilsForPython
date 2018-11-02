#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/6/22
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_iniconfig.py
    @Software: PyCharm
    @Description: ini配置文件操作工具类
        1.读取.ini配置文件
        2.修改.ini配置文件
        [section]
        option:value
"""
import ConfigParser

'''
    基础读取配置文件
        -read(filename)         直接读取文件内容
        -sections()             得到所有的section，并以列表的形式返回
        -options(section)       得到该section的所有option
        -items(section)         得到该section的所有键值对
        -get(section,option)    得到section中option的值，返回为string类型
        -getint(section,option) 得到section中option的值，返回为int类型，还有相应的getboolean()和getfloat() 函数。
'''
class iniconfig_reade():

    # 初始化配置文件对象
    def __init__(self,path):
        # 实例化
        self.cf = ConfigParser.ConfigParser()
        # 读取配置文件
        self.cf.read(path)

    # 获取所有的sections
    def get_sections(self):
        sections = self.cf.sections()
        return sections

    # 获取section下的所有key
    def get_options(self,section):
        opts = self.cf.options(section=section)
        return opts

    # 获取section下的所有键值对
    def get_kvs(self,section):
        kvs = self.cf.items(section=section)
        return kvs

    # 根据section和option获取指定的value
    def get_key_value(self,section,option):
        opt_val = self.cf.get(section=section,option=option)
        return opt_val

    # 更新指定section的option下的value
    # def update_section_option_val(self,section,option,value,path,module):
    #     self.cf.set(section=section,option=option,value=value)
    #     with open(path,module) as f:
    #         self.cf.write(f)

'''
    基础写入配置文件
        -write(fp)                         将config对象写入至某个 .init 格式的文件  Write an .ini-format representation of the configuration state.
        -add_section(section)              添加一个新的section
        -set(section, option, value)       对section中的option进行设置，需要调用write将内容写入配置文件 ConfigParser2
        -remove_section(section)           删除某个 section
        -remove_option(section, option)    删除某个 section 下的 option
'''
class iniconfig_write():

    def __init__(self,path,module):
        # 实例化配置对象
        self.cf = ConfigParser.ConfigParser()
        # 获取写入文件路径，若采用w+方式则该文件可以不存在
        self.path = path
        # 配置写入方式，写入方式"w+"清空写
        self.module = module

    # 写入配置文件
    def write_ini_file(self):
        with open(self.path,self.module) as f:
            self.cf.write(f)

    # 新增section
    def add_section(self,section):
        self.cf.add_section(section=section)
        self.write_ini_file()

    # 删除某个 section
    def remove_section(self,section):
        self.cf.remove_section(section=section)
        self.write_ini_file()

    # 删除某个 section 下的 option
    def remove_option(self,section,option):
        self.cf.remove_option(section=section,option=option)
        self.write_ini_file()

if __name__ == '__main__':
    pass
























