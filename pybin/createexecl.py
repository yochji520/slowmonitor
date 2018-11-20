#!/usr/bin/python3
#-*- coding: UTF-8 -*- 
#@Author:
#@Time:
#@File:

import xlwt

basename = "slowlog-"

'''
dateFormat = xlwt.XFStyle()
dateFormat.num_format_str = 'yyyy/mm/dd'
worksheet.write(0, 0, dt.date.today(),dateFormat)
'''

#生成slowlog的exlec文件
def contentexecl(rows, yesterday):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    for i in range(len(rows)):
        for j in range(len(rows[i])):
            sheet.write(i, j, str(rows[i][j]))
    execlfile = basename + str(yesterday) + '.xls'
    wbk.save(execlfile)
    return execlfile