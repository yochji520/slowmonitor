#!/bin/env python3
# -*- coding: UTF-8 -*-
#author:ycj
#email:yochji520@163.com
#filename:
#description:封装的db_op

import pymysql
from src.logs import *

log = LogtoLog().getlog()
#数据库操作（op）
class dbDml(object):
    def __init__(self, db_dict):
        self._db_dict = db_dict
        self._conn = self.getconn()
        self._cursor = self._conn.cursor()

#获取连接
    def getconn(self):
        try:
            conn = pymysql.connect(**self._db_dict)
        except Exception as err:
            log.warning("connect database failed, %s:" % err)
        return conn

#数据查询
    def select(self, sql):
        rows = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                rows = self._cursor.fetchall()
            except Exception as err:
                rows = False
                log.warning("query database exception, %s:" % err)
        return rows

#带参数的查询
    def select_params(self, sql, *params):
        rows = ''
        if(self._conn):
            try:
                self._cursor.execute(sql, params)
                rows = self._cursor.fetchall()
            except Exception as err:
                rows = False
                log.warning("query database exception, %s:" % err)
        return rows

#update():用于处理不带参数的所有数据更新;
    def update(self, sql):
        if (self._conn):
            try:
                self._cursor.execute(sql)
                self._conn.commit()
            except Exception as err:
                log.warning("MySQL Exception %s:" % err)

# 改参数的更新
    def update_params(self, sql, *params):
        if (self._conn):
            try:
                self._cursor.execute(sql, params)
                self._conn.commit()
            except Exception as err:
                log.warning("MySQL Exception %s:" % err)

    def close(self):
        if (self._conn):
            try:
                if(type(self._cursor) == 'object'):
                    self._cursor.close()
                if(type(self._conn) == 'object'):
                    self._conn.close()
            except Exception as err:
                log.warning("close database exception, %s,%s,%s" % (err, type(self._cursor), type(self._conn)))

