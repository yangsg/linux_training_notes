
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

local7ftp7server 的 ip: 192.168.175.10

[root@local7ftp7server ~]# yum -y install vsftpd

[root@local7ftp7server ~]# rpm -q vsftpd
      vsftpd-3.0.2-25.el7.x86_64

[root@local7ftp7server ~]# useradd Bob    # 创建 Bob 用户账号
[root@local7ftp7server ~]# passwd Bob     # 为 Bob 用户账号 修改密码
Changing password for user Bob.
New password:
Retype new password:
passwd: all authentication tokens updated successfully.

[root@local7ftp7server ~]# mkdir -p /ftp_srv/Bob

[root@local7ftp7server ~]# chown -R Bob:Bob /ftp_srv/Bob/
[root@local7ftp7server ~]# chmod 750 /ftp_srv/Bob/

[root@local7ftp7server ~]# vim /etc/vsftpd/vsftpd.conf   # 针对本地用户认证 的配置

      ## 启用本地用户认证
      local_enable=YES

      ## 设置 user 替换标记
      user_sub_token=$USER

      ##修改本地用户的数据目录
      local_root=/ftp_srv/$USER


// 启动 vsftpd 并将其 设为 开机自启
[root@local7ftp7server ~]# systemctl start vsftpd
[root@local7ftp7server ~]# systemctl enable vsftpd
Created symlink from /etc/systemd/system/multi-user.target.wants/vsftpd.service to /usr/lib/systemd/system/vsftpd.service.

---------------------------------------------------------------------------------------------------


windows 客户端:

    ftp://192.168.175.10

    ftp 客户端工具: 如  filezilla:  https://filezilla-project.org/


linux 客户端:
     linux 下的 ftp 客户端工具有 ftp, lftp. 其中 lftp 有命令自动补齐功能

[root@client ~]# yum -y install ftp      # 安装 ftp 客户端工具 ftp

[root@client ~]# ftp 192.168.175.10            # 连接 ftp 服务器  # 更多信息见 man ftp
Connected to 192.168.175.10 (192.168.175.10).
220 (vsFTPd 3.0.2)
Name (192.168.175.10:root): Bob   <--- 输入用户名
331 Please specify the password.
Password:         <--- 输入用户密码
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> pwd   <--- 执行命令
257 "/ftp_srv/Bob"
ftp> quit  <--- 退出
221 Goodbye.

----------------------------------------------------
[root@client ~]# yum -y install lftp     # 安装 ftp 客户端工具 lftp

[root@client ~]# lftp 192.168.175.10 -u Bob  # 更多信息见 man lftp
Password:   <--- 输入 用户 Bob 的密码
lftp Bob@192.168.175.10:~> pwd
ftp://Bob@192.168.175.10
lftp Bob@192.168.175.10:~> ls
-rw-r--r--    1 1001     1001          118 Jun 07 14:15 bbb.txt
lftp Bob@192.168.175.10:~> quit

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

   https://serverfault.com/questions/247096/allow-anonymous-upload-for-vsftpd
