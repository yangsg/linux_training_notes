
主动模式:
  端口号：
    命令连接： 21/tcp
    数据连接： 20/tcp


被动模式
  端口号：
    命令连接： 21/tcp
    数据连接:  >1024  随机


[root@ftpserver ~]# yum -y install vsftpd

[root@ftpserver ~]# rpm -q vsftpd
    vsftpd-3.0.2-25.el7.x86_64


[root@ftpserver ~]# grep 'ftp' /etc/passwd
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin



[root@ftpserver ~]# vim /etc/vsftpd/vsftpd.conf










---------------------------------------------------------------------------------------------------

man vsftpd
man 5 vsftpd.conf


网上资料:

   ftp的主动模式和被动模式: http://slacksite.com/other/ftp.html

