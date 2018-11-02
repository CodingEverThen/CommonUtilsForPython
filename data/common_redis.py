#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Time    : 2018/5/23
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_redis.py
    @Software: PyCharm
    @Description: 链接redis数据库，对数据进行增删改查操作，支持多语句同时执行
'''

import redis


class redisdata():
    # 初始化redis链接
    def __init__(self, host, port, db, password):
        # redis 链接地址
        self.host = host
        # redis 链接端口
        self.port = port
        # redis 库名，redis默认从db0-db15
        self.db = db
        # 链接redis的密码，若无则设置为空值 passwordd = ""
        self.passwd = password
        # 创建redis 连接池
        # 加上decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
        RedisPool = redis.ConnectionPool(host=self.host, port=self.port, password=self.passwd, db=self.db, decode_responses=True)
        # 获取redis 链接
        self.conn = redis.Redis(connection_pool=RedisPool)
        # Pipelines是Redis类的一个子类，支持缓存多个命令，然后作为单个请求发送。通过减少TCP请求次数来达到提供性能的目的。
        # self.pipe = self.r.pipeline(transaction=True)

    """
        string类型 {'key':'value'} redis操作
    """

    # 更新对象内容
    def setredis(self, key, value, time=None):
        # 非空即真非0即真
        if time:
            res = self.conn.setex(key, value, time)
        else:
            res = self.conn.set(key, value)
        return res

    # 获取对象值
    def getRedis(self, key):
        res = self.conn.get(key).decode()
        return res

    # 删除对象
    def delRedis(self, key):
        res = self.conn.delete(key)
        return res

    """
    hash类型，{'name':{'key':'value'}} redis操作
    """

    # 更新hash数据
    def setHashRedis(self, name, key, value):
        res = self.conn.hset(name, key, value)
        return res

    # 获取hash数据
    def getHashRedis(self, name, key=None):
        # 判断key是否我为空，不为空，获取指定name内的某个key的value; 为空则获取name对应的所有value
        if key:
            res = self.conn.hget(name, key)
        else:
            res = self.conn.hgetall(name)
        return res

    # 删除hash数据
    def delHashRedis(self, name, key=None):
        if key:
            res = self.conn.hdel(name, key)
        else:
            res = self.conn.delete(name)
        return res


if __name__ == '__main__':
    r = redisdata("127.0.0.1", 6379, 0, "")
    r.setredis("test1", "testvalue1")
    res = r.getRedis("test1")
    print("res:" + res)
