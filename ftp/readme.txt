
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


[root@ftpserver ~]# chown -R ftp:ftp /var/ftp/pub/
[root@ftpserver ~]# chmod 755 /var/ftp/pub/


[root@ftpserver ~]# vim /etc/vsftpd/vsftpd.conf   # 如下配置是针对 匿名访问 的设置
        ## 开启匿名访问
        anonymous_enable=YES

        ## 针对所有用户的上传权限
        write_enable=YES

        ##    注意：
        ##      a. 确保匿名用户对本地目录拥有写权限
        ##      b. 匿名用户上传时，不允许在数据根目录直接上传文件
        ##      c. 不允许在匿名用户的数据根目录添加任何写权限，否则ftp会禁止匿名访问
        ## 启用匿名用户上传文件的权限
        anon_upload_enable=YES

        ## 启用匿名用户上传目录的权限
        anon_mkdir_write_enable=YES

        ## 启用匿名用户其他写入操作(删除、重命名)
        anon_other_write_enable=YES

        ## 保证其他匿名用户可正常下载文件
        anon_umask=022

        ## 修改匿名用户默认的数据目录 (如果有需要的话, 注意, 如果启用了这该项, 还应该注意系统的文件系统本身的权限是否满足要求)
        ## anon_root=/data/caiwu


// 启动 vsftpd 并将其 设为 开机自启
[root@ftpserver ~]# systemctl start vsftpd
[root@ftpserver ~]# systemctl enable vsftpd
Created symlink from /etc/systemd/system/multi-user.target.wants/vsftpd.service to /usr/lib/systemd/system/vsftpd.service.



ftp://192.168.175.10/






---------------------------------------------------------------------------------------------------

man vsftpd
man 5 vsftpd.conf


网上资料:
   vsftpd 安装:
       https://linuxize.com/post/how-to-setup-ftp-server-with-vsftpd-on-centos-7/#6-securing-transmissions-with-ssl-tls
       https://www.tecmint.com/install-ftp-server-in-centos-7/
       https://www.krizna.com/centos/setup-ftp-server-centos-7-vsftp/
       https://blog.csdn.net/qq_14940627/article/details/83189999

   ftp的主动模式和被动模式: http://slacksite.com/other/ftp.html

   https://serverfault.com/questions/247096/allow-anonymous-upload-for-vsftpd
