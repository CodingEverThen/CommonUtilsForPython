#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/7/4
    @Author  : LiuXueWen
    @Site    : 
    @File    : Test_common_elasticsearch.py
    @Software: PyCharm
    @Description: 对elasticsearch数据的操作，包括获取数据，发送数据
"""
import elasticsearch
import json

# import iniconfig_common

class elasticsearchdata():
    def __init__(self,hosts,username,password,maxsize,is_ssl):
        '''
        :param hosts: 请求地址
        :param username:登录用户名
        :param password:登录密码
        :param maxsize:最大连接数
        :param is_ssl:是否开启ssl加密
        '''
        # 初始化ini操作脚本，获取配置文件
        try:
            # 判断请求方式是否ssl加密
            if is_ssl == "true":
                # 获取证书地址
                # cert_pem = iniconfig_common.get_ini("config.ini").get_key_value("certs", "certs")
                es_ssl = elasticsearch.Elasticsearch(
                    # 地址
                    hosts=hosts,
                    # 用户名密码
                    http_auth=(username,password),
                    # 开启ssl
                    use_ssl=True,
                    # 确认有加密证书
                    verify_certs=True,
                    # 对应的加密证书地址
                    # client_cert=cert_pem
                )
                self.es = es_ssl
            elif is_ssl == "false":
                # 创建普通类型的ES客户端
                es_ordinary = elasticsearch.Elasticsearch(hosts, http_auth=(username, password), maxsize=int(maxsize))
                self.es = es_ordinary
        except Exception as e:
            print(e)


    def query_data(self,keywords_list,date,size):
        '''
        :param keywords_list: list格式，搜索关键字词
        :param date: 当前时间的过去时间范围，字符串，"30m"
        :param size: 返回数据的条数
        :return: 执行搜索使用的完整语句
        '''
        gte = "now-"+str(date)
        gte = str(gte)
        query_data = {
            "size":size,
            # 查询语句
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": keywords_list,
                                "analyze_wildcard": True
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": gte,
                                    "lte": "now",
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        }
        return query_data

    # 从es获取数据
    def get_datas_by_query(self,index_name,keywords_list,param,date,size):
        '''
        :param index_name: 索引名称
        :param keywords: 关键字词，数组
        :param param: 需要数据条件，例如_source
        :param date: 过去时间范围,字符串格式，例如过去30分钟内数据，"30m"
        :param size: 返回数据的条数
        :return: all_datas 返回查询到的所有数据（已经过param过滤）
        '''

        all_datas = []
        # 遍历所有的查询条件
        for keywords in keywords_list:
            # DSL语句
            query_data = self.query_data(keywords,date,size)
            res = self.es.search(
                index=index_name,
                body=query_data
            )
            for hit in res['hits']['hits']:
                # 获取指定的内容
                response = hit[param]
                # 添加所有数据到数据集中
                all_datas.append(response)
        # 返回所有数据内容
        return all_datas

    # 当索引不存在创建索引
    def create_index(self,index_name):
        '''
        :param index_name: 索引名称
        :return:如果创建成功返回创建结果信息，试过已经存在创建新的index失败返回index的名称
        '''
        # 获取索引的映射
        # index_mapping = IndexMapping.index_mapping
        # # 判断索引是否存在
        # if self.es.indices.exists(index=index_name) is not True:
        #     # 创建索引
        #     res = self.es.indices.create(index=index_name,body=index_mapping)
        #     # 返回结果
        #     return res
        # else:
        #     # 返回索引名称
        #     return index_name
        pass

    # 插入指定的单条数据内容
    def insert_single_data(self,index_name,doc_type,data):
        '''
        :param index_name: 索引名称
        :param doc_type: 文档类型
        :param data: 需要插入的数据内容
        :return: 执行结果
        '''
        res = self.es.index(index=index_name,doc_type=doc_type,body=data)
        return res

    # 向ES中新增数据,批量插入
    def insert_datas(self,index_name):
        '''
        :desc 通过读取指定的文件内容获取需要插入的数据集
        :param index_name: 索引名称
        :return: 插入成功的数据条数
        '''
        insert_datas = []
        # 判断插入数据的索引是否存在
        self.createIndex(index_name=index_name)
        # 获取插入数据的文件地址
        data_file_path = self.ini.get_key_value("datafile","datafilepath")
        # 获取需要插入的数据集
        with open(data_file_path,"r+") as data_file:
            # 获取文件所有数据
            data_lines = data_file.readlines()
            for data_line in data_lines:
                # string to json
                data_line = json.loads(data_line)
                insert_datas.append(data_line)
        # 批量处理
        res = self.es.bulk(index=index_name,body=insert_datas,raise_on_error=True)
        return res

    # 从ES中在指定的索引中删除指定数据（根据id判断）
    def delete_data_by_id(self,index_name,doc_type,id):
        '''
        :param index_name: 索引名称
        :param index_type: 文档类型
        :param id: 唯一标识id
        :return: 删除结果信息
        '''
        res = self.es.delete(index=index_name,doc_type=doc_type,id=id)
        return res

    # 根据条件删除数据
    def delete_data_by_query(self,index_name,doc_type,param,gt_time,lt_time):
        '''
        :param index_name:索引名称，为空查询所有索引
        :param doc_type:文档类型，为空查询所有文档类型
        :param param:过滤条件值
        :param gt_time:时间范围，大于该时间
        :param lt_time:时间范围，小于该时间
        :return:执行条件删除后的结果信息
        '''
        # DSL语句
        query_data = {
            # 查询语句
            "query": {
                "bool": {
                    "must": [
                        {
                            "query_string": {
                                "query": param,
                                "analyze_wildcard": True
                            }
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": gt_time,
                                    "lte": lt_time,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        }
        res = self.es.delete_by_query(index=index_name,doc_type=doc_type,body=query_data,_source=True)
        return res

    # 指定index中删除指定时间段内的全部数据
    def delete_all_datas(self,index_name,doc_type,gt_time,lt_time):
        '''
        :param index_name:索引名称，为空查询所有索引
        :param doc_type:文档类型，为空查询所有文档类型
        :param gt_time:时间范围，大于该时间
        :param lt_time:时间范围，小于该时间
        :return:执行条件删除后的结果信息
        '''
        # DSL语句
        query_data = {
            # 查询语句
            "query": {
                "bool": {
                    "must": [
                        {
                            "match_all": {}
                        },
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": gt_time,
                                    "lte": lt_time,
                                    "format": "epoch_millis"
                                }
                            }
                        }
                    ],
                    "must_not": []
                }
            }
        }
        res = self.es.delete_by_query(index=index_name, doc_type=doc_type, body=query_data, _source=True)
        return res

    # 修改ES中指定的数据
    def update_data_by_id(self,index_name,doc_type,id,data):
        '''
        :param index_name: 索引名称
        :param doc_type: 文档类型，为空表示所有类型
        :param id: 文档唯一标识编号
        :param data: 更新的数据
        :return: 更新结果信息
        '''
        res = self.es.update(index=index_name,doc_type=doc_type,id=id,body=data)
        return res