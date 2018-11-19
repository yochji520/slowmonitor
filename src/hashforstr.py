#!/usr/bin/python3
# -*- coding: UTF-8 -*-
'''
#author:ycj
#email:yochji520@163.com
#filename:parseslow.py
#description:计算hash的方法
'''


from hashlib import md5
from hashlib import sha1
from hashlib import sha224
from hashlib import sha384
from hashlib import sha512

#计算hash值
def hashForString(method, srcbyte):
    srcbyte = srcbyte.encode("utf8")

    if method == 'md5':
        m = md5()
        m.update(srcbyte)
        srcbyte = m.hexdigest()
    elif method == 'sha1':
        s = sha1()
        s.update(srcbyte)
        srcbyte = s.hexdigest()
    elif method == 'sha224':
        s = sha224()
        s.update(srcbyte)
        srcbyte = s.hexdigest()
    elif method == 'sha384':
        s = sha384()
        s.update(srcbyte)
        srcbyte = s.hexdigest()
    elif method == 'sha512':
        s = sha512()
        s.update(srcbyte)
        srcbyte = s.hexdigest()
    return srcbyte

