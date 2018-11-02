# common_utils
公共脚本工具使用

[TOC]

## 仓库说明

### common
一些常用的公共脚本类

|编号|文件名|说明|
|:---:|:---|:---|
|1|common_date.py|对时间相关操作的工具类|

### data
主要用于操作数据相关的公共脚本

|编号|文件名|说明|
|:---:|:---|:---|
|1|common_elasticsearch.py|有关ES的一些基本操作，增删改查等|
|2|common_ftpupload.py|用于对ftp服务器的一些操作，上传、删除、查询等|
|3|common_jsondata.py|对服务器上获取的json数据的一些操作，需要根据情况修改|
|4|common_kafka.py|对kafka的一些操作，包括生产者和消费者，可通过配置文件配置相关信息|
|5|common_pymysql.py|使用pymysql对mysql数据库的增删改查操作|
|6|common_redis.py|对redis的一些常用操作|
|7|common_mongodb.py|常用的mongodb数据库的操作|

### file
主要对文件进行相关操作的工具类

|编号|文件名|说明|
|:---:|:---|:---|
|1|common_allrows.py|统计指定路径下所有文件的总行数|
|2|common_csvconfig.py|查询csv类型文件并获取指定信息|
|3|common_filefunction.py|对文件的增删改查等操作|
|4|common_filemerge.py|合并指定规则下的所有文件|
|5|common_filename_change.py|批量修改指定路径下所有文件的文件名指定位置上的信息|
|6|common_filesplite.py|拆分指定文件为多个文件|
|7|common_iniconfig.py|对ini类型的文件进行增删改查操作|

### telecommunication
主要对网络信息等相关操作的工具类

|编号|文件名|说明|
|:---:|:---|:---|
|1|common_emailsend.py|基于python和smtp协议的邮件发送客户端，支持文本、超文本、多媒体附件等|
|2|common_nntp.py|基于python和nntp协议的新闻组客户端|

### shell
一些常见的基本的shell脚本

|编号|文件名|说明|
|:---:|:---|:---|
|1|nohup.sh|nohup后台守护进程运行命令脚本|
