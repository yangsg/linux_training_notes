import smtplib

#// https://docs.python.org/3.6/tutorial/stdlib.html#internet-access

#// 发送邮件 email

server = smtplib.SMTP('localhost')
server.sendmail('soothsayer@example.org', 'jcaesar@example.org',
"""To: jcaesar@example.org
From: soothsayer@example.org

Beware the Ides of March.
""")
server.quit()

