#!/usr/bin/env python
# -*- coding: utf-8 -*-
# LCH @ 2017-04-28 09:24:52

import string
import smtplib

HOST = "smtp-mail.outlook.com"  # 定义smtp主机
SUBJECT = "Test email from Python"  # 定义邮件主题
TO = "lch_mail@hotmail.com"  # 定义邮件收件人
FROM = "lch_mail@hotmail.com"  # 定义邮件发件人
TEXT = "Hello!"  # 邮件内容
BODY = string.join((  # 组装sendmail方法的邮件主体内容,各段以"\r\n"进行分割
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        TEXT
        ), "\r\n")

def getconfig(keyword):
    try:
        with open("config.cfg", "r") as config:
            for line in config:
                if line.startswith(keyword):
                    return line[len(keyword)+2:].strip()
            else:
                return None
    except Exception, e:
        print e
        print 'can not find ***%s*** config info' % keyword
        return None

PASSWORD = getconfig('password')

if __name__ == "__main__":
    server = smtplib.SMTP()  # 创建一个SMTP()对象
    server.connect(HOST, "587")  # 通过connect方法链接smtp主机
    server.starttls()  # 启动安全传输模式
    server.login("lch_mail@hotmail.com", PASSWORD)  # 邮箱账号登录校验
    server.sendmail(FROM, [TO], BODY)  # 邮件发送
    server.quit()  # 断开smtp链接
