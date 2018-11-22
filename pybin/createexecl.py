#!/usr/bin/python3
#-*- coding: UTF-8 -*- 
#@Author:
#@Time:
#@File:

import xlwt

basename = "slowlog-"

#生成slowlog的exlec文件
def contentexecl(rows, yesterday):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    #row0 = [u'数据库', u'最近更新时间', u'SQL语句', u'SQL统计']
    #sheet1 = a(sheet, row0)
    #写数据
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            sheet.write(i, j, str(rows[i][j]))
            #设置行宽
            sheet.col(1).width = 5000
            sheet.col(2).width = 24000
    execlfile = basename + str(yesterday) + '.xls'
    wbk.save(r"../tmp/" + execlfile)
    return execlfile

