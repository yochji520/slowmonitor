#!/bin/env python3
# -*- coding: UTF-8 -*-
#author:ycj
#email:yochji520@163.com
#filename:
#description:

import configparser
from src.logs import *

CONFNAME = r"/app/slowmonitor/conf/db.conf"

#读取配置文件，并以字典形式返回

def read_cof():
    log = LogtoLog().getlog()
    conf = configparser.ConfigParser()
    try:
        conf = configparser.ConfigParser()
        conf.read(CONFNAME)
    except IOError as err:
        log.error("文件不存在，或者权限不足!!! " + str(err))
    kvs = conf.items("db1")
    db_host = kvs[2][1]
    db_user = kvs[0][1]
    db_port = kvs[3][1]
    db_passwd = kvs[1][1]
    db_name = kvs[4][1]
    db_dict = dict(host=db_host, port=int(db_port), user=db_user, passwd=db_passwd, db=db_name)
    return db_dict

