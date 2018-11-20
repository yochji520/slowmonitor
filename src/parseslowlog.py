#!/bin/env python3
# -*- coding: UTF-8 -*-
# author:ycj
# email:yochji520@163.com
# filename:
# description:解析处理slowlog


from src.getconf import *
from src.dbop import *
from src.hashforstr import hashForString
import re


# 解析替换SQL，并计算出一致性hash值，解析顺序：like-->in-->字符串-->时间-->日期-->数字
def parseSlow(SQLTEXT, DBName, CtsStartTime):
    # 包含like
    pattern1 = re.compile(r'\'%[\u4e00-\u9fa5A-Za-z0-9_]{0,}%\'')
    outstream1 = re.sub(pattern1, '\'?\'', SQLTEXT)
    # 包含in
    pattern2 = re.compile(r'(\'[\u4E00-\u9FA5A-Za-z0-9_]{0,}\')')
    outstream2 = re.sub(pattern2, '=\'?\'', outstream1)
    # 替换字符串
    pattern3 = re.compile(r'=\'[\u4e00-\u9fa5A-Za-z0-9_]{0,}\'')
    outstream3 = re.sub(pattern3, '=\'?\'', outstream2)
    # 替换时间
    pattern4 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}')
    outstream4 = re.sub(pattern4, '?', outstream3)
    # 替换日期
    pattern5 = re.compile(r'[0-9]{4}-[0-9]{2}-[0-9]{2}')
    outstream5 = re.sub(pattern5, '?', outstream4)
    # 替换数字
    pattern6 = re.compile(r'[0-9]{1,100}')
    sqltext = re.sub(pattern6, '?', outstream5)
    # outstream作为最终输出，将以outstream作为计算hashvalues的变量
    hashvalues = hashForString("md5", sqltext)
    # 查询数据库id,将计算的结果写入数据库，同时判断SQL类型是否存在，并最终更新时间
    db_dict = read_cof()
    dbdml = dbDml(db_dict)
    dbids = dbdml.select_params("select dbid from dbinfo where dbname= %s", DBName)
    hashifexists = dbdml.select_params("select count(*) from slowagginfo where hashvalue=%s", hashvalues)
    ifhash = hashifexists[0][0]
    lasttime = CtsStartTime
    dbnameid = dbids[0][0]
    sqlstatus = 0
    dbname = DBName
    if ifhash == 1:
        # 数据存在直接修改lasttime
        updatesql="update slowagginfo set lasttime = '%s' where hashvalue='%s'" % (lasttime, hashvalues)
        dbdml.update(updatesql)
    else:
        # 不存在直接写库
        insertsql = "insert into slowagginfo(dbnameid, dbname, sqltext, sqlstatus, hashvalue, lasttime) values(%s,'%s',\"%s\",%d,'%s','%s')" % \
                    (dbnameid, dbname, sqltext, sqlstatus, hashvalues, lasttime)
        dbdml.update(insertsql)
    return hashvalues


# slowlog详细信息入库
def slowinfotodb(HostAddress, QueryTimes, LockTimes, ParseRowCounts, ReturnRowCounts, CtsStartTime, DBName, SQLText,
                 hashvalue):
    insertsql = "insert into monitor.slowlogdetail(ipaddr,querytime,locktime,parserowcount,returnrowcount,execstarttime,dbname,sqltext,hashvalue) \
    values('%s','%s','%s',%d,%d,'%s','%s',\"%s\",'%s')" % (
    HostAddress, QueryTimes, LockTimes, ParseRowCounts, ReturnRowCounts, CtsStartTime, DBName, SQLText, hashvalue)
    db_dict = read_cof()
    dbdml = dbDml(db_dict)
    dbdml.update(insertsql)
