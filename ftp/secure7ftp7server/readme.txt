
主动模式:
  端口号：
    命令连接： 21/tcp
    数据连接： 20/tcp


被动模式
  端口号：
    命令连接： 21/tcp
    数据连接:  >1024  随机

---------------------------------------------------------------------------------------------------
server 端

secure7ftp7server 的 ip: 192.168.175.10

[root@secure7ftp7server ~]# yum -y install vsftpd

[root@secure7ftp7server ~]# rpm -q vsftpd
      vsftpd-3.0.2-25.el7.x86_64

[root@secure7ftp7server ~]# grep 'ftp' /etc/passwd
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin

// 创建 秘钥 证书 存放目录
[root@secure7ftp7server ~]# mkdir /etc/vsftpd/ssl
[root@secure7ftp7server ~]# chmod 700 /etc/vsftpd/ssl


[root@anon7ftp7server ~]# vim /etc/vsftpd/vsftpd.conf    # 最终的 /etc/vsftpd/vsftpd.conf 配置 如下
          anonymous_enable=NO
          local_enable=YES
          write_enable=YES
          local_umask=022
          dirmessage_enable=YES
          xferlog_enable=YES
          connect_from_port_20=YES
          xferlog_std_format=YES
          chroot_local_user=YES
          listen=NO
          listen_ipv6=YES
          pam_service_name=vsftpd
          userlist_enable=YES
          userlist_file=/etc/vsftpd/user_list
          userlist_deny=NO
          tcp_wrappers=YES
          user_sub_token=$USER
          local_root=/home/$USER/ftp
          pasv_min_port=30000
          pasv_max_port=31000
          rsa_cert_file=/etc/vsftpd/ssl/vsftpd.pem
          rsa_private_key_file=/etc/vsftpd/ssl/vsftpd.pem
          ssl_enable=YES


// 生成私钥 和 自签名的 证书 (1024 已不太安全, 最好使用 2048 位的)
[root@secure7ftp7server ~]# openssl req -x509 -nodes -days 3650 -newkey rsa:2048 -keyout /etc/vsftpd/ssl/vsftpd.pem -out /etc/vsftpd/ssl/vsftpd.pem
    Generating a 2048 bit RSA private key
    .....+++
    ................+++
    writing new private key to '/etc/vsftpd/ssl/vsftpd.pem'
    -----
    You are about to be asked to enter information that will be incorporated
    into your certificate request.
    What you are about to enter is what is called a Distinguished Name or a DN.
    There are quite a few fields but you can leave some blank
    For some fields there will be a default value,
    If you enter '.', the field will be left blank.
    -----
    Country Name (2 letter code) [XX]:CN
    State or Province Name (full name) []:Beijing
    Locality Name (eg, city) [Default City]:Beijing
    Organization Name (eg, company) [Default Company Ltd]:mytraining
    Organizational Unit Name (eg, section) []:mytraining
    Common Name (eg, your name or your server's hostname) []:mytraining.com   <-- 输入公司域名
    Email Address []:123@qq.com

[root@secure7ftp7server ~]# chmod 400 /etc/vsftpd/ssl/vsftpd.pem

[root@secure7ftp7server ~]# systemctl restart vsftpd


[root@secure7ftp7server ~]# systemctl start vsftpd
[root@secure7ftp7server ~]# systemctl enable vsftpd
Created symlink from /etc/systemd/system/multi-user.target.wants/vsftpd.service to /usr/lib/systemd/system/vsftpd.service.

[root@secure7ftp7server ~]# useradd newftpuser
[root@secure7ftp7server ~]# passwd newftpuser
Changing password for user newftpuser.
New password:
Retype new password:
passwd: all authentication tokens updated successfully.

// 将用户添加到 /etc/vsftpd/user_list
[root@secure7ftp7server ~]# echo "newftpuser" | sudo tee -a /etc/vsftpd/user_list
newftpuser


[root@secure7ftp7server ~]# vim /etc/vsftpd/user_list
# vsftpd userlist
# If userlist_deny=NO, only allow users in this file
# If userlist_deny=YES (default), never allow users in this file, and
# do not even prompt for a password.
# Note that the default vsftpd pam config also checks /etc/vsftpd/ftpusers
# for users that are denied.
#  因为我们在 /etc/vsftpd/vsftpd.conf 中将 /etc/vsftpd/user_list 配置为了 允许 login access(即 ftp访问) 的 "白名单", 所以 需要根据需要对其进行修改
#root
#bin
#daemon
#adm
#lp
#sync
#shutdown
#halt
#mail
#news
#uucp
#operator
#games
#nobody
newftpuser


[root@secure7ftp7server ~]# mkdir -p /home/newftpuser/ftp/upload
[root@secure7ftp7server ~]# chmod 550 /home/newftpuser/ftp
[root@secure7ftp7server ~]# chmod 750 /home/newftpuser/ftp/upload
[root@secure7ftp7server ~]# chown -R newftpuser: /home/newftpuser/ftp
[root@secure7ftp7server ~]# ls -ld /home/newftpuser/ftp
dr-xr-x--- 3 newftpuser newftpuser 20 Jun  8 17:11 /home/newftpuser/ftp

// 禁止 shell access
[root@secure7ftp7server ~]# echo -e '#!/bin/sh\necho "This account is limited to FTP access only."' |  tee -a  /bin/ftponly
#!/bin/sh
echo "This account is limited to FTP access only."
[root@secure7ftp7server ~]# echo "/bin/ftponly" | tee -a /etc/shells
/bin/ftponly
[root@secure7ftp7server ~]# usermod newftpuser -s /bin/ftponly     # 禁止 用于 shell 访问

[root@secure7ftp7server ~]# systemctl restart vsftpd

---------------------------------------------------------------------------------------------------
windows 客户端: (使用专用的 ftp 工具 )

    ftp 客户端工具: 如  filezilla:  https://filezilla-project.org/


linux 客户端:

[root@client ~]# yum -y install lftp     # 安装 ftp 客户端工具 lftp
[root@basic linux_training_notes]# lftp      # 参考: http://www.linuxweblog.com/ftp-tls-ssl
lftp :~> set ssl:verify-certificate no    <--- 取消验证  (因为这里 server 端使用的是自签名的证书)
lftp :~> connect 192.168.175.10           <--- 连接 到 server
lftp 192.168.175.10:~> login newftpuser   <--- 登录
Password:        <--- 输入密码
lftp newftpuser@192.168.175.10:~> ls     <--- 执行 ls 命令
drwxr-x---    2 1001     1001            6 Jun 08 09:11 upload
lftp newftpuser@192.168.175.10:/>


lftp 内部 的常用命令有:

        lcd
        get
        mget
        mirror

---------------------------------------------------------------------------------------------------

man vsftpd
man 5 vsftpd.conf


网上资料:
   vsftpd 安装:
       https://linuxize.com/post/how-to-setup-ftp-server-with-vsftpd-on-centos-7/#6-securing-transmissions-with-ssl-tls
       https://www.tecmint.com/install-ftp-server-in-centos-7/
       https://www.krizna.com/centos/setup-ftp-server-centos-7-vsftp/
       https://www.tecmint.com/secure-vsftpd-using-ssl-tls-on-centos/
       https://blog.csdn.net/qq_14940627/article/details/83189999

   ftp的主动模式和被动模式: http://slacksite.com/other/ftp.html

   证书:
       https://www.cnblogs.com/hnxxcxg/p/7610582.html
       https://blog.csdn.net/gengxiaoming7/article/details/78505107

   https://serverfault.com/questions/247096/allow-anonymous-upload-for-vsftpd

  lftp with ssl
    https://stackoverflow.com/questions/23900071/how-do-i-get-lftp-to-use-ssl-tls-security-mechanism-from-the-command-line
    http://www.linuxweblog.com/ftp-tls-ssl
