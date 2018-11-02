#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/5/31
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_pymysql.py
    @Software: PyCharm
    @Description: 使用pyMySQL包创建mysql链接并对数据进行操作，包含增删改查
"""
import pymysql
from datetime import datetime,date,timedelta

def properties():
    config = {
                'host': '127.0.0.1',
                'port': 3306,
                'user': 'root',
                'password': 'rot',
                'db': 'employees',
                'charset': 'utf8mb4',
                'cursorclass': pymysql.cursors.DictCursor,
            }
    return config


class mysqlconnection():
    # 初始化数据库链接
    def __init__(self):
        # 通过配置文件修改配置，在执行文件中直接获取相应的配置信息
        config = properties()

        # Connect to the database
        self.connection = pymysql.connect(**config)

    """
    执行sql语句前需要获取cursor，因为配置默认自动提交，故在执行sql语句后需要主动commit，最后不要忘记关闭连接。
    """
    def insertdata(self):
        """
            插入
        """
        # 获取明天的时间
        tomorrow = datetime.now().date() + timedelta(days=1)

        # 执行sql语句
        try:
            with self.connection.cursor() as cursor:
                # 执行sql语句，插入记录
                sql = 'INSERT INTO employees (first_name, last_name, hire_date, gender, birth_date) VALUES (%s, %s, %s, %s, %s)'
                cursor.execute(sql, ('Robin', 'Zhyea', tomorrow, 'M', date(1989, 6, 14)));
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            self.connection.commit()
        except Exception as e:
            print e
            # 出现异常执行回滚操作
            self.connection.rollback()
        finally:
            self.connection.close()

    def selectdata(self):
        """
            查询
        """
        # 获取雇佣日期
        hire_start = datetime.date(1999, 1, 1)
        hire_end = datetime.date(2016, 12, 31)

        # 执行sql语句
        try:
            with self.connection.cursor() as cursor:
                # 执行sql语句，进行查询
                sql = 'SELECT first_name, last_name, hire_date FROM employees WHERE hire_date BETWEEN %s AND %s'
                cursor.execute(sql, (hire_start, hire_end))
                # 获取查询结果
                result = cursor.fetchone()
                print(result)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            self.connection.commit()
        except Exception as e:
            print e
            # 出现异常执行回滚操作
            self.connection.rollback()
        finally:
            self.connection.close()

    def deletedata(self):
        """
            删除
        """
        hire_date = ""
        # 执行sql语句
        try:
            with self.connection.cursor() as cursor:
                # 执行sql语句，进行删除
                sql  = "DELETE FROM employees WHERE hire_date = %s"
                cursor.execute(sql,hire_date)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            self.connection.commit()
        except Exception as e:
            print e
            # 出现异常执行回滚操作
            self.connection.rollback()
        finally:
            self.connection.close()

    def uploaddata(self):
        """
            修改
        """
        hire_date = ""
        # 执行sql语句
        try:
            with self.connection.cursor() as cursor:
                # 执行sql语句，进行删除
                sql = "UPDATE employees SET hire_date = %s"
                cursor.execute(sql, hire_date)
            # 没有设置默认自动提交，需要主动提交，以保存所执行的语句
            self.connection.commit()
        except Exception as e:
            print e
            # 出现异常执行回滚操作
            self.connection.rollback()
        finally:
            self.connection.close()