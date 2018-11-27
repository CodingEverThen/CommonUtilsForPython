#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    @Time    : 2018/5/31
    @Author  : LiuXueWen
    @Site    : 
    @File    : common_emailsend.py
    @Software: PyCharm
    @Description: 使用SMTP协议发送邮件，支持同时发送给多个地址，支持同时发送文本信息、超文本信息和多附件
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.header import Header
import os

# 配置信息，可单独写成一个文件引入
class properties():
    # 设置服务器, "smtp.xx.com"
    mail_host = "smtp.qq.com"
    # 用户名
    mail_user = "947752894@qq.com"
    # 口令
    mail_pass = "rmqemzsvlhhqbfbb"
    # smtp服务器端口，每个服务商提供的邮件服务端口可能不一致，465是腾讯的端口
    mail_port = 465
    # 发送邮件的地址
    sender = "lxw112@vip.qq.com"
    # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，list类型，可同时填写多个地址并以,分割
    receivers = "947752894@qq.com"
    # 邮件发送的内容
    messageText = "测试使用\n"
    # 邮件发送的超文本内容
    messageHTML = """
                    <!DOCTYPE html>
                    <html lang="en">
                    <head>
                        <meta charset="UTF-8">
                        <title>test</title>
                    </head>
                    <body>
                        <img src="http://a.hiphotos.baidu.com/image/pic/item/730e0cf3d7ca7bcb6a172486b2096b63f624a82f.jpg" alt="test" width="200px" height="200px">
                    </body>
                    </html>
                """
    # 发送邮件方的别名展示（类似昵称）,为空则显示发件方地址
    messageFromHeader = ""
    # 接收邮件方的展示信息
    messageToHeader = "test python"
    # 邮件主题
    messageSubject = "ceshiceshi123"
    # 需要发送的附件的详细地址，支持多附件发送，附件之间以，分割(需要保留中括号形成数组，否则当附件只有一个的时候会报错)
    filePaths = ["1.csv","2.mp3"]

class emailsend():
    def __init__(self):
        # 下面所有参数均可通过配置文件配置获取
        """
            :param mail_host: 设置服务器,"smtp.xx.com"
            :param mail_user: 用户名
            :param mail_pass: 口令
            :param sender: 发送邮件的地址
            :param receivers: 接收邮件，可设置为你的QQ邮箱或者其他邮箱
            :param messageText: 邮件发送的文本内容
            :param messageHTML: 邮件发送的超文本内容
            :param messageFromHeader: 发送邮件方的别名展示（类似昵称）
            :param messageToHeader: 接收邮件方的展示信息
            :param messageSubject: 邮件主题
            :param filePath: 附件详细地址
            :param sendtype: 邮件发送类型
            :return:
        """
        # 需要获取的参数列
        # 地址
        self.mail_host = properties.mail_host
        # 用户名（邮箱）
        self.mail_user = properties.mail_user
        # 密码（smtp的密码）
        self.mail_pass = properties.mail_pass
        # 端口，链接smtp的端口，每个服务商可能不一样
        self.mail_port = properties.mail_port
        # 接收方
        self.receivers = properties.receivers
        # 发送的文本内容
        self.messageText = properties.messageText
        # 发送的超文本内容
        self.messageHTML = properties.messageHTML
        # 发送的附件地址
        self.filePaths = properties.filePaths
        # 接收方头部展示信息
        self.messageToHeader = properties.messageToHeader
        # 接收方展示主题
        self.messageSubject = properties.messageSubject
        # 发送方昵称
        messageFromHeader = properties.messageFromHeader
        # 接收方展示的发送方地址
        self.sender = properties.sender
        # 如果发件人昵称未填写则直接使用发件人地址作为名称
        if messageFromHeader == "":
            self.messageFromHeader = self.sender
        else:
            self.messageFromHeader = messageFromHeader

    # 公共头部分
    def common_header(self,sendtype):
        # 邮件类型为"multipart/alternative"的邮件包括纯文本正文（text / plain）和超文本正文（text / html）
        # 一共三个参数，第一个为发送文本信息，第二个发送类型，第三个发送信息的编码。如果想要发送html类型的信息，仅需要修改第二个参数'plain'为'html'即可
        # 文本信息,使用‘plain’属性不能正常显示
        # message = MIMEText(self.messageHTML, 'plain', 'utf-8')
        if sendtype == "plain":
            message = MIMEText(self.messageText, sendtype, 'utf-8')
        elif sendtype == "html":
            message = MIMEText(self.messageHTML, sendtype, 'utf-8')
        # 邮件显示信息内容
        # 发送邮件方的头部展示信息
        message['From'] = Header(self.messageFromHeader, 'utf-8')
        # 接收邮件方的展示信息
        message['To'] = Header(self.messageToHeader, 'utf-8')
        # 邮件主题
        message['Subject'] = Header(self.messageSubject, 'utf-8')
        return message

    # 发送文本内容
    def sendemailbytext(self):
        message = self.common_header("plain")
        self.sendmain(message)

    # 发送超文本内容
    def sendemailbyhtml(self):
        message = self.common_header("html")
        self.sendmain(message)

    # 发送混合内容，带附件
    def sendemailbymixed(self):
        # 邮件类型为"multipart/mixed"的邮件包含附件。向上兼容，如果一个邮件有纯文本正文，超文本正文，内嵌资源，附件，则选择mixed类型。
        message = MIMEMultipart('mixed')
        # 邮件显示信息内容
        # 发送邮件方的头部展示信息
        message['From'] = Header(self.messageFromHeader, 'utf-8')
        # 接收邮件方的展示信息
        message['To'] = Header(self.messageToHeader, 'utf-8')
        # 邮件主题
        message['Subject'] = Header(self.messageSubject, 'utf-8')
        emailtext = MIMEText(self.messageText,"plain",'utf-8')
        message.attach(emailtext)
        emailhtml = MIMEText(self.messageHTML,"html",'utf-8')
        message.attach(emailhtml)
        """发送邮件附件，支持多附件发送"""
        try:
            # 如果没有需要发送的附件，跳过
            if len(self.filePaths) == 0:
                pass
            # 如果只发送一个附件内容
            elif len(self.filePaths) == 1:
                part = MIMEApplication(open(self.filePaths[0],"rb").read())
                part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.filePaths[0]))
                # 附件内容
                message.attach(part)
            # 发送多个邮件附件
            else:
                for i in range(0,len(self.filePaths)):
                    part = MIMEApplication(open(self.filePaths[i], "rb").read())
                    part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(self.filePaths[i]))
                    # 附件内容
                    message.attach(part)
            self.sendmain(message)
        except Exception as e:
            print("附件发送失败，错误信息：" + str(e))

    # 发送主程序
    def sendmain(self,message):
        try:
            # 因为现在很多服务商做了安全验证，所有在发送邮件的时候需要把原来的smtplib.SMTP()改成现在的smtplib.SMTP_SSL()方式
            smtpObj = smtplib.SMTP_SSL()
            # smtpObj = smtplib.SMTP()
            # 链接邮件服务器
            smtpObj.connect(self.mail_host, self.mail_port)
            # 登录邮件系统
            smtpObj.login(self.mail_user, self.mail_pass)
            # 发送邮件信息
            smtpObj.sendmail(self.sender,self.receivers,message.as_string())
            # 关闭会话
            smtpObj.quit()
            # 关闭连接
            smtpObj.close()
            print("邮件发送成功")
        except Exception as e:
            print("邮件发送失败，错误信息：" + str(e).encode("utf8"))


if __name__ == '__main__':
    # emailsend().sendemailbytext()
    # emailsend().sendemailbyhtml()
    emailsend().sendemailbymixed()