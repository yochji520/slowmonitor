#!/bin/env python3
# -*- coding: UTF-8 -*-
#author:ycj
#email:yochji520@163.com
#filename:
#description: rds认证，数据处理

from aliyunsdkcore import client

#SDK认证
class alisdkauth(object):
    def __init__(self, accessKeyId, accessKeySecret, regionid):
        self._accessKeyId = accessKeyId
        self._accessKeySecret = accessKeySecret
        self._regionid = regionid

#连接认证
    def aliauth(self):
        clt = client.AcsClient(self._accessKeyId, self._accessKeySecret, self._regionid)
        return clt













