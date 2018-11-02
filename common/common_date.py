# -*-encoding:utf-8 -*-

import datetime
import time

DEFAULE_DATE_FORMAT='%Y%m%d'


def get_someday_before(n,fmt=DEFAULE_DATE_FORMAT):
    '''获取n天前日期，返回的fmt日期格式'''
    yes = datetime.date.today()-datetime.timedelta(days=n)
    return yes.strftime(fmt)

def get_today(fmt=DEFAULE_DATE_FORMAT):
    '''获取今天前日期，返回的fmt日期格式'''
    return get_someday_before(0,fmt)

def get_yesterday(fmt=DEFAULE_DATE_FORMAT):
    '''获取昨天前日期，返回的fmt日期格式'''
    return get_someday_before(1,fmt)

def get_someday_before_tmp(n,ms=False):
    '''获取n天前的时间戳'''
    yes = datetime.date.today()-datetime.timedelta(days=n)
    if ms:
        return long(time.mktime(yes.timetuple())*1000)
    else:
        return long(time.mktime(yes.timetuple()))

def get_today_tmp(ms=False):
    '''获取今天前的时间戳'''
    return get_someday_before_tmp(0,ms)

def get_yesterday_tmp(n,ms=False):
    '''获取昨天前的时间戳'''
    return get_someday_before_tmp(1,ms)