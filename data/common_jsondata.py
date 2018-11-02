#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    @Time    : 2018/5/24
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_jsondata.py
    @Software: PyCharm
    @Description:
        1.对指定的 url 地址上的 json 数据进行增删和获取操作
        2.输入指定的key值获取对应的value信息
'''

import urllib2
import json
import codecs


class jsondataget():

    # 输入对象地址和参数,datahe user_agent为可选参数，若无则填写为空
    def __init__(self, *args):
        # self.headers = {'User-Agent': **kwargs}
        """
            :param args: 包含url、data信息，data数据可选
            :param kwargs: 包含头部验证信息，可选。结构：{'User-Agent': }
        """
        try:
            self.req = urllib2.Request(*args)
            self.res = urllib2.urlopen(self.req)
            self.response = self.res.read()
        except Exception as e:
            print("出现了一些问题，提示如下：" + str(e))

    # 获取指定地址上的数据，并将数据写入到指定的文件中
    def write_json(self, log_path):
        file = open(log_path, 'wb')
        file.write(self.response)
        print(self.response)

    # 根据指定的key值获取对应的value信息，三层结构,最终根据获取的数据形成新的 k-v 结构数据
    # 不同结构的json数据需要重写下面不同的数据获取结构，请注意验证每层结构的数据类型
    def get_key(self, key, result, data1, data2,req_file_name):
        """
            {
                key:{
                    key:{
                        key:{}
                    }
                }
            }
            1.key：
            2.result：
            3.data1：需要查询的第一个数据
            4.data2：需要查询的第二个数据
            5.req_file_name：需要保存的文件名（包含路径，若不写路径则保存在当前文件夹下）
        """
        res = json.loads(self.response)
        # print len(res[key])
        for i in range(0, len(res[key][result])):
            # 获取需要的第一个数据作为我们的key
            res_req1 = res[key][result][i][data1]
            # 获取需要的第二个数据作为我们需要的value
            res_req2 = res[key][result][i][data2]
            # 形成 key-value 结构的数据
            res_req = {res_req2:res_req1}
            print(res_req)
            res_req = json.dumps(res_req,encoding='utf8',ensure_ascii=False)
            # print(res_req2)
            # 写入文件
            self.write_req(res_req, req_file_name)

    # 获取的数据写入文件中
    def write_req(self, str_req, req_file_name):
        file = codecs.open(req_file_name,"a","utf-8")
        file.write(str_req + "\n")
        file.close()
        print("数据%s写入成功"%str_req.encode('utf8'))

# 根据上面生成的数据的key值获取新的地址并返回需要的数据集合，然后写入指定的文件中
class jsondatasend():
    """
        通过一行一行读取指定文件中的数据作为新的data传递给urllib模块
        下载指定的对象数据
    """
    # 输入对象地址和参数,datahe user_agent为可选参数，若无则填写为空
    def __init__(self,url,data,remote_path,data1,data2,req_file_name):
        # self.file = open(req_file_name,"wb")
        self.url = url
        resfile = open(remote_path,"r")
        while True:
            line = resfile.readline()
            res = eval(line)
            content = res.keys()
            content = content[0]
            self.data = data+ content
            self.req = urllib2.Request(self.url, self.data)
            self.res = urllib2.urlopen(self.req)
            self.response = self.res.read()
            self.content = content
            res = json.loads(self.response)
            print(len(res[data1]))
            if len(res[data1])>0:
                # 获取需要的第二个数据作为我们需要的value
                res_req2 = res[data1][0][data2]
                print(res_req2)
                # 形成 key-value 结构的数据
                res_req = {self.content: res_req2}
                res_req = json.dumps(res_req, encoding='utf8', ensure_ascii=False)
                # print(res_req2)
                # 写入文件
                self.write_req(res_req, req_file_name)
            else:
                return
            if not line:
               break

    # 获取的数据写入文件中
    def write_req(self, str_req, req_file_name):
        file = codecs.open(req_file_name,"a","utf-8")
        file.write(str_req + "\n")
        file.close()
        print("数据%s写入成功"%str_req.encode('utf8'))


if __name__ == '__main__':
    # res = JsonOperation("http://10.25.245.116:8080/MIGUM2.0/v1.0/content/search_all.do",
    #                     'isCopyright=1&isCorrect=1&pageNo=1&pageSize=10&searchSwitch={"song":1,"album":0,"singer":0,"tagSong":1,"mvSong":0,"songlist":0,"bestShow":1}&text=爱情 ')
    # res.write_json("json.txt")
    # res.get_key("songResultData", "result", "copyright", "contentId", "res.txt")
    # res = JsonOperation("http://118.24.151.27/WebAppReader/mock/home.json")
    # res.get_key("items","ad_name","ad_type","res.txt")
    # res.get_key("songResultData", "result", "contentId", "content.txt")
    res = jsondatasend("http://10.25.245.116:8080/MIGUM2.0/v1.0/content/resourceinfo.do",'needSimple=01&resourceType=2&resourceId=',"res.txt","resource","copyright","res2.txt")
    # res.get_key("resource","copyright","res2.txt")
