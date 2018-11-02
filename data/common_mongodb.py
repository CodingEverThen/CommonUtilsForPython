#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/7/18
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_mongodb.py
    @Software: PyCharm
    @Description: 对 mangodb 数据库的一些操作
"""
import pymongo

class mongodbclient():
    # 初始化数据库
    def __init__(self,hosts,dbname,col):
        try:
            '''
            :param hosts: 链接数据库地址，mongodb://[username:password@]host1[:port1][,host2[:port2],...[,hostN[:portN]]][/[database][?options]]
            :param dbname:数据库名称
            :param col:数据库中的表名称
            '''
            mgclient = pymongo.MongoClient(hosts)
            dbclient = mgclient[dbname]
            # 创建表，数据库需要在表创建后才能创建
            self.mycol = dbclient[col]
        except Exception as e:
            print("初始化数据库错误：{}".format(str(e)))

    # 增加一条数据
    def insertdata(self,data):
        '''
        :param data: dict格式，不指定插入的文档编号则自动生成唯一编号，{key:value}
        :return:
        '''
        try:
            res = self.mycol.insert_one(data)
            return "数据成功插入的文档id：{}".format(res.inserted_id)
        except Exception as e:
            print("插入单条数据异常：".format(str(e)))

    # 批量增加数据
    def insertmanydata(self,data):
        '''
        :param data: 数据格式，不指定插入id则自动生成唯一编号，[{key:value},{key:value},{key:value}]
        :return:
        '''
        try:
            res = self.mycol.insert_many(data)
            return "数据成功插入的文档的所有 id ：{}".format(res.__inserted_ids)
        except Exception as e:
            print("插入批量数据异常：".format(str(e)))

    # 插入指定 _id 的多个文档
    def insertmanydatabyid(self,data):
        '''
        :param data: 数组格式，其中_id为必须，代表指定插入的文档的编号
                    [
                        {
                            '_id':1,
                            key:value
                        }
                    ]
        :return:
        '''
        try:
            res = self.mycol.insert_many(data)
            print("插入指定 _id 的多个文档成功！")
        except Exception as e:
            print()

    # 删除单个文档
    def deletedata(self,data):
        '''
        :param data:  { "name": "Taobao" }
        :return: 删除数据后的数据集合
        '''
        try:
            res_full = []
            res = self.mycol.delete_one(data)
            for x in res:
                res_full.append(x)
            return res_full
        except Exception as e:
            print("删除单个文档异常：{}".format(str(e)))

    # 根据条件删除文档
    def deletedata_by_query(self,query):
        '''
        :param query:
                        使用正则表达式删除多条数据
                        query= { "name": {"$regex": "^F"} }
                        query等于空{}的时候删除全部数据
                        query = {}
        :return:返回删除的文档数量
        '''
        try:
            res = self.mycol.delete_many(query)
            return res
        except Exception as e:
            print("根据条件删除文档异常：{}".format(str(e)))

    # 删除集合
    def dropcollection(self):
        '''
        :return: 删除该集合
        '''
        try:
            res = self.mycol.drop()
            return res
        except Exception as e:
            print("删除集合异常：{}".format(str(e)))

    # 修改第一条记录
    def updat_firstedata(self,old_query,new_query):
        '''
        :param old_query: 查询条件 { "alexa": "10000" }
        :param new_query: 修改数据 { "$set": { "alexa": "12345" } }
        :return:修改后的数据集合
        '''
        try:
            new_res = []
            self.mycol.update_one(old_query,new_query)
            for x in self.mycol.find():
                new_res.append(x)
            return new_res
        except Exception as e:
            print("修改记录异常：{}".format(str(e)))

    # 批量修改记录
    def updat_firstedata(self, old_query, new_query):
        '''
        :param old_query: 查询条件，可以使用正则表达式等 { "name": { "$regex": "^F" } }
        :param new_query: 修改条件  { "$set": { "alexa": "123" } }
        :return: 修改的文档数量
        '''
        try:
            res = self.mycol.update_many(old_query,new_query)
            return res
        except Exception as e:
            print("批量修改记录异常：{}".format(str(e)))

    # 查询第一条数据
    def search_firstdata(self):
        try:
            res = self.mycol.find_one()
            return res
        except Exception as e:
            print("查询第一条数据异常：{}".format(str(e)))

    # 根据条件查询数据
    def search_databyquery(self,query,limite,sort_key):
        '''
        :param query:
                    指定字段查询。除了 _id 你不能在一个对象中同时指定 0 和 1，如果你设置了一个字段为 0，则其他都为 1，反之亦然。0、1为布尔值判断，不是实际的参数值。
                    { "_id": 0, "name": 1, "alexa": 1 }
                    普通条件筛选
                    { "name": "RUNOOB" }
                    查询的条件语句中，我们还可以使用修饰符。
                    { "name": { "$gt": "H" } }
                    我们还可以使用正则表达式作为修饰符。正则表达式修饰符只用于搜索字符串的字段。
                    { "name": { "$regex": "^R" } }
        :param limite:指定返回条数
        :param sort_key:排序规则,str
        :return:返回查询结果
        '''
        try:
            fullres = []
            if sort_key == '' or sort_key == None:
                # 判断是否使用限制
                if limite == '' or limite == None:
                    # 没有指定查询条件则查询所有数据
                    if query == '' or query == None:
                        allres = self.mycol.find()
                        for x in allres:
                            fullres.append(x)
                    else:
                        # 根据条件查询
                        reslist = self.mycol.find(query)
                        for res in reslist:
                            fullres.append(res)
                else:
                    if query == '' or query == None:
                        allres = self.mycol.find().limit(limite)
                        for x in allres:
                            fullres.append(x)
                    else:
                        # 根据条件查询
                        reslist = self.mycol.find(query).limit(limite)
                        for res in reslist:
                            fullres.append(res)
            else:
                # 没有指定查询条件则查询所有数据
                if query == '' or query == None:
                    allres = self.mycol.find().sort(sort_key)
                    for x in allres:
                        fullres.append(x)
                else:
                    # 根据条件查询
                    reslist = self.mycol.find(query).sort(sort_key)
                    for res in reslist:
                        fullres.append(res)
            # 返回查询结果
            return fullres
        except Exception as e:
            print("条件查询数据异常：{}".format(str(e)))