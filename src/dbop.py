#!/bin/env python3
# -*- coding: UTF-8 -*-
#author:ycj
#email:yochji520@163.com
#filename:
#description:封装的db_op

import logging
import pymysql

class dbDml(object):
    def __init__(self, db_dict):
        self._db_dict = db_dict
        self._conn = self.getconn()
        self._cursor = self._conn.cursor()

#获取连接
    def getconn(self):
        try:
            conn = pymysql.connect(**self._db_dict)
        except Exception as e:
            print("connect database failed, %s:" % e)
        return conn

#数据查询
    def select(self, sql):
        rows = ''
        if(self._conn):
            try:
                self._cursor.execute(sql)
                rows = self._cursor.fetchall()
            except Exception as e:
                rows = False
                print("query database exception, %s:" % e)
                logging.info("query database exception, %s:" % e)
        return rows

#update():用于处理不带参数的所有数据更新;
    def update(self, sql):
        if (self._conn):
            try:
                flag = self._cursor.execute(sql)
                self._conn.commit()
            except Exception as e:
                print("update database exception, %s:" % e)
                logging.info("MySQL Exception %s:" % e)
        return flag

    def close(self):
        if (self._conn):
            try:
                if(type(self._cursor) == 'object'):
                    self._cursor.close()
                if(type(self._conn) == 'object'):
                    self._conn.close()
            except Exception as e:
                print("close database exception, %s,%s,%s" % (e, type(self._cursor), type(self._conn)))

    def update_params(self, sql, params):
        if (self._conn):
            try:
                flag = self._cursor.execute(sql, params)
                self._conn.commit()
            except Exception as e:
                print("MySQL Exception %s:" % e)
        return flag

