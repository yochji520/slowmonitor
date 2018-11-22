#!/usr/bin/python3

import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from src.getconf import read_cof
from src.dbop import dbDml
import pandas as pd
from src.createexecl import contentexecl
from src.logs import *


#mail账号
mail_host = "smtp.ym.163.com"
sender_user = "youchuanjiang@wanbei.tv"
user_pass = "wuhuan42@123.A"
#计算时间
yesterday = (datetime.datetime.now()-datetime.timedelta(hours=2)).strftime("%Y-%m-%d")
starttime=(datetime.datetime.now()-datetime.timedelta(days=1)).strftime("%Y-%m-%d")
endtime=datetime.datetime.now().strftime("%Y-%m-%d")


#发送邮件
def sendmail():
    # 获取邮件接收人
    db_dict = read_cof()
    dbdml = dbDml(db_dict)
    emails = dbdml.select("select email from monitor_bak.user")
    receivers = []
    for email in emails:
        receivers.append(email[0])

    #统计SQL出现的次数，以出现次数排序（降序）显示前10条
    selectsql = "select dbname,max(lasttime),sqltext,count(hashvalue) as sqlcount from \
        (select a.dbname,b.sqltext,b.lasttime,c.hashvalue from  dbinfo a left join slowagginfo b on\
        a.dbid=b.dbnameid left join slowlogdetail c on b.hashvalue = c.hashvalue where c.execstarttime >= '%s' \
        and c.execstarttime < '%s' and b.sqlstatus=0 ) a group by hashvalue order by count(hashvalue) desc limit 10 ;" % (starttime, endtime)
    rows = dbdml.select(selectsql)
    dbname = []
    lasttime = []
    sqltext = []
    num = []
    for row in rows:
        dbname.append(row[0])
        lasttime.append(row[1])
        sqltext.append(row[2])
        num.append(row[3])
    #生成附件
    execlfile = contentexecl(rows, yesterday)
    #生成邮件内容
    rlist = pd.DataFrame({'DBNAME': dbname, 'LASTTIME': lasttime, 'SQL': sqltext, 'SQLCOUNT': num})
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
    for recename in receivers:
        # 创建一个带附件的实例
        message = MIMEMultipart()
        message['From'] = Header("youchuanjiang@wanbei.tv", 'utf-8')
        message['To'] = Header(recename, 'utf-8')
        subject = 'SLOWLOG'
        message['Subject'] = Header(subject, 'utf-8')
        #构建文件正文
        message.attach(MIMEText(Text, 'html', 'utf-8'))
        # 构建附件1，传送当前目录下的execlfile文件
        att1 = MIMEText(open(r'../tmp/' + execlfile, 'rb').read(), 'base64', 'utf-8')
        att1["Content-Type"] = 'application/octet-stream'
        # 这里的filename可以任意写，写什么名字，邮件中显示什么名字
        att1["Content-Disposition"] = 'attachment; filename=' + execlfile
        message.attach(att1)
        try:
            smtpObj = smtplib.SMTP_SSL(mail_host)
            smtpObj.login(sender_user, user_pass)
            smtpObj.sendmail(sender_user, recename, message.as_string())
            print("邮件发送成功")
        except Exception as err:
            log = LogtoLog().getlog()
            log.warning("邮件发送失败" + str(err))

if __name__=="__main__":
    sendmail()