#!/bin/env python3
# -*- coding: UTF-8 -*-
# author:ycj
# email:yochji520@163.com
# filename:
# description:

import json
from aliyunsdkrds.request.v20140815 import DescribeRegionsRequest
from src.parseslowlog import *
from src.basetool import utc_to_local

# 处理json数据
class slowLog(object):
    def __init__(self, instanceid, begintime, endtime, clt):
        self.instanceid = instanceid
        self.begintime = begintime
        self.endtime = endtime
        self.client = clt

    def getSlowLogs(self):
        request = DescribeRegionsRequest.DescribeRegionsRequest()
        request.set_accept_format('json')
        request.set_action_name('DescribeSlowLogRecords')
        request.set_query_params(dict(DBInstanceId=self.instanceid, StartTime=self.begintime, EndTime=self.endtime))
        response = self.client.do_action_with_exception(request).decode()
        data = json.loads(response)
        '''解析json数据,判断是否存在备份语句，备份SQL直接跳过处理'''
        for slowdata in data['Items']['SQLSlowRecord']:
            ReturnRowCounts = slowdata['ReturnRowCounts']
            HostAddress = slowdata['HostAddress']
            LockTimes = slowdata['LockTimes']
            ExecutionStartTime = slowdata['ExecutionStartTime']
            # UTC_TIME --> BJ_TIME
            CtsStartTime = utc_to_local(ExecutionStartTime)
            ParseRowCounts = slowdata['ParseRowCounts']
            QueryTimes = slowdata['QueryTimes']
            DBName = slowdata['DBName']
            SQLText = slowdata['SQLText']
            #判断是否跳过循环,包含SQL_NO_CACHE,dumper.data_stat的不记录
            skipcondition1 = "SQL_NO_CACHE"
            skipcondition2 = "dumper"
            skipcondition3 = "data_stat"
            if skipcondition1 in SQLText:
                continue
            elif skipcondition2 in HostAddress:
                continue
            elif skipcondition3 in DBName:
                continue
            else:
                hashvalue = parseSlow(SQLText, DBName, CtsStartTime)#返回hashvalue带入slowinfotodb函数，将数据写入slowlog
                slowinfotodb(HostAddress, QueryTimes, LockTimes, ParseRowCounts, ReturnRowCounts, CtsStartTime\
                             , DBName, SQLText, hashvalue)


