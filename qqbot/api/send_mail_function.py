#!/usr/bin/env python
from smtplib import SMTP_SSL
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
from config import SECRETS


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))


def send_email(email_num, words):
    if SECRETS['qq_mail']['msg_from'] and SECRETS['qq_mail']['passwd']:
        msg_from = SECRETS['qq_mail']['msg_from'] 
        passwd = SECRETS['qq_mail']['passwd'] 
        msg_to = email_num
        subject = 'SS服务器'
        mail_info = words

        # msg = MIMEText(mail_content, "plain", 'utf-8')
        msg = MIMEText(mail_info, "html", 'utf-8')
        msg["Subject"] = Header(subject, 'utf-8')
        msg["From"] = _format_addr(u'Parrot-CN <%s>' % msg_from)
        msg["To"] = _format_addr(u'管理员 <%s>' % msg_to)

        try:
            # ssl登录
            smtp = SMTP_SSL('smtp.qq.com')
            # set_debuglevel()用来调试,1开启调试，0关闭调试
            smtp.set_debuglevel(0)
            smtp.ehlo('smtp.qq.com')
            smtp.login(msg_from, passwd)
            # Send_email
            smtp.sendmail(msg_from, msg_to, msg.as_string())
            smtp.quit()
            return "Mail sent successfully!"
        except Exception as e:
            return "Mail delivery failed!"

