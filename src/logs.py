# -*- coding: UTF-8 -*-
#author:ycj
#email:yochji520@163.com
#filename:
#description:封装日志logging

import logging
import time

logtime = time.strftime('%Y%m%d', time.localtime(time.time()))

class Log(object):
    def __init__(self, name):
        self.path = "../../log"
        self.filename = self.path + 'running' +logtime + '.log'
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        #定义日志文件中格式
        self.formatter = logging.Formatter('%(asctime)s - %(levelname)s -   %(name)s[line:%(lineno)d] - %(message)s')
        self.fh.setFormatter(self.formatter)
        self.logger.addHandler(self.fh)

class customError(Exception):
     def __init__(self, msg=None):
          self.msg = msg
     def __str__(self):
           if self.msg:
                  return self.msg
           else:
                  return u"某个不符合条件的语法出了问题"

