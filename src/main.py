#!/bin/env python3
# -*- coding: UTF-8 -*-
#author:ycj
#email:yochji520@163.com
#filename:
#description:

import datetime
from src.aliauth import *
from src.getslowlog import *

#定义AcsClient信息
accessKeyId = 'LTAI7CW0wse6REbg'
accessKeySecret = 'tEGeXXpYMPx5Rqmv9W4y1OBlXsJPcJ'
regionid = 'cn-hangzhou'

#计算起始-->UTC时间
utcbegintime = (datetime.datetime.now()-datetime.timedelta(hours=28)).strftime("%Y-%m-%dT%H:%MZ")
utcendtime = (datetime.datetime.now() - datetime.timedelta(hours=24)).strftime("%Y-%m-%dT%H:%MZ")

#获取实例信息
def getinstance():
    db_dict = read_cof()
    dbdml = dbDml(db_dict)
    getinstanceid = 'select instancename from monitor.dbinstance'
    rows = dbdml.select(getinstanceid)
    return rows

if __name__  ==  "__main__":
    alisdkauth = alisdkauth(accessKeyId, accessKeySecret, regionid)
    clt = alisdkauth.aliauth()
    rows = getinstance()
    for instance in rows:
        instanceid = instance[0]
        getslow = slowLog(instanceid, utcbegintime, utcendtime, clt)
        getslow.getSlowLogs()



