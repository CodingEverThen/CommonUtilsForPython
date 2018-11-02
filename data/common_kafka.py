#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/7/9
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_kafka.py.py
    @Software: PyCharm
    @Description: kafka-python 的消费者和生产者模型，支持数据写入
"""
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import json

class kafkaproducer():
    '''
    使用kafka的生产模块
    '''

    def __init__(self, kafkahost, kafka_topic):
        '''
        :param kafkahost: 请求地址，数组
        :param kafkatopic: topic地址
        '''
        self.kafkatopic = kafka_topic
        self.producer = KafkaProducer(bootstrap_servers=kafkahost)

    def sendjsondata(self, params):
        try:
            parmas_message = json.dumps(params)
            producer = self.producer
            futur = producer.send(self.kafkatopic, parmas_message.encode('utf-8'))
            res = futur.get(timeout=60)
            producer.flush()
            return res
        except KafkaError as e:
            print(e)


class kafkaconsumer():
    '''
    使用Kafka—python的消费模块
    '''

    def __init__(self, kafkahost, kafkaport, kafkatopic, groupid):
        self.kafkaHost = kafkahost
        self.kafkaPort = kafkaport
        self.kafkatopic = kafkatopic
        self.groupid = groupid
        self.consumer = KafkaConsumer(self.kafkatopic, group_id = self.groupid,
                                      bootstrap_servers = '{kafka_host}:{kafka_port}'.format(
            kafka_host=self.kafkaHost,
            kafka_port=self.kafkaPort ))

    def consume_data(self):
        try:
            for message in self.consumer:
                # print json.loads(message.value)
                yield message
        except KeyboardInterrupt as e:
            print(e)

if __name__ == '__main__':
    test = {
        "name":"zhangfei"
    }
    # producer = Kafka_producer(["http://192.168.158.172:9092"],"test")
    producer = kafkaproducer(["10.25.245.192:9092"],"nori-log")
    res = producer.sendjsondata(test)
    print res
    # custom = Kafka_consumer("http://192.168.158.172","9092","test","")
    custom = kafkaconsumer("10.25.245.192","9092","nori-log","")
    response = custom.consume_data()
    print(response)