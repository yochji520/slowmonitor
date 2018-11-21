#!/usr/bin/python3
#-*- coding: UTF-8 -*- 
#@Author:
#@Time:
#@File:

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from src.getconf import read_cof
from src.dbop import dbDml
import pandas as pd
from pybin.createexecl import contentexecl
import datetime

#mail账号
mail_host = "smtp.ym.163.com"
sender_user = "youchuanjiang@wanbei.tv"
user_pass = "wuhuan42@123.A"

yesterday = (datetime.datetime.now()-datetime.timedelta(hours=11)).strftime("%Y-%m-%d")

#发送邮件
def sendmail():
    # 获取邮件接收人
    db_dict = read_cof()
    dbdml = dbDml(db_dict)
    emails = dbdml.select("select email from monitor.user")
    receivers = []
    for email in emails:
        receivers.append(email[0])

    #统计SQL出现的次数，以出现次数排序（降序）显示前10条
    rows = dbdml.select("select dbname,sqltext,max(lasttime),count(hashvalue) as sqlcount from \
        (select a.dbname,b.sqltext,b.lasttime,c.hashvalue from dbinfo a left join slowagginfo b on\
        a.dbid=b.dbnameid left join slowlogdetail c on b.hashvalue = c.hashvalue where b.sqlstatus=0) a group by hashvalue order by count(hashvalue) desc ;")
    DBNAME = []
    SQL = []
    LASTTIME = []
    NUM = []
    for row in rows:
        DBNAME.append(row[0])
        SQL.append(row[1])
        LASTTIME.append(row[2])
        NUM.append(row[3])

    #生成附件
    execlfile = contentexecl(rows, yesterday)

    #生成邮件内容
    rlist = pd.DataFrame({'DBNAME': DBNAME, 'SQL': SQL, 'LASTTIME': LASTTIME, 'SQLCOUNT': NUM})
    tr = ''
    for r in range(len(rlist)):
        tr = tr + """
        <tr>
          <td width="40">""" + str(rlist.iloc[r][0]) + """</td>
          <td width="110">""" + str(rlist.iloc[r][1]) + """</td>
          <td width="700">""" + str(rlist.iloc[r][2]) + """</td>
          <td width="50" align="center">""" + str(rlist.iloc[r][3]) + """</td>
        </tr>"""

    Text = """
            <span style="font-size: 20px">""" + yesterday + "慢SQL统计情况" + """</span>
            <table style="font-size: 12px"  width="1000" border="1" cellspacing="0" cellpadding="1" text-align="center">
                <tr>
                    <td width="40" style="background:yellow" align="center">数据库</td>
                    <td width="110" style="background:yellow" align="center">最近更新时间</td>
                    <td width="700" style="background:yellow" align="center">SQL语句</td>
                    <td width="50" style="background:yellow" align="center">SQL统计</td>
                </tr> """ + tr + """  
            </table>
            <p style="color: red; font-size: 12px">""" + "说明：列表按统计NUM降序排序，返回执行时间最慢SQL前十，全部信息内容请查看附件" + """</p>    
        """
    #创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("youchuanjiang@wanbei.tv", 'utf-8')
    for recename in receivers:
        message['To'] = Header(recename, 'utf-8')
        subject = 'SLOWLOG'
        message['Subject'] = Header(subject, 'utf-8')
        #构建文件正文
        message.attach(MIMEText(Text, 'html', 'utf-8'))
        # 构造附件1，传送当前目录下的execlfile文件
        att1 = MIMEText(open(execlfile, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename=' + execlfile
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(mail_host, 25)
            smtpObj.login(sender_user, user_pass)
            smtpObj.sendmail(sender_user, recename, message.as_string())
            print("邮件发送成功")
        except Exception:
            print("邮件发送失败")

if __name__=="__main__":
    sendmail()