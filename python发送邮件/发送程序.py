from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))
# 输入Email地址和口令:
from_addr = input('请输入发件人的邮箱号码From: ')
password = input('请输入发件人的邮箱授权码Password: ')
# 输入SMTP服务器地址:
smtp_server = input('请输入邮箱服务器地址SMTP server: ')
# 输入收件人地址:
to_addr = []
try:
    while True:
        a = input('请输入收件人邮箱：')
        to_addr.append(a)
        print(to_addr)
        b = input('是否继续输入，n退出，任意键继续：')
        if b == 'n':
            break
    content =input('请输入邮件正文：')
    subject = input('请输入你的邮件主题：')
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['From'] = _format_addr('发送者<%s>' %(from_addr) )
    msg['To'] = _format_addr('管理员<%s>' % (to_addr))
    msg['Subject'] = Header(subject, 'utf-8')#.encode()

    server = smtplib.SMTP_SSL(smtp_server, 465)
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()
    print('邮件发送成功')
except:
    print('发送失败')