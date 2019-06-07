
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


[root@secure7ftp7server ~]# systemctl start vsftpd
[root@secure7ftp7server ~]# systemctl enable vsftpd
Created symlink from /etc/systemd/system/multi-user.target.wants/vsftpd.service to /usr/lib/systemd/system/vsftpd.service.


---------------------------------------------------------------------------------------------------




[root@anon7ftp7server ~]# grep 'ftp' /etc/passwd
ftp:x:14:50:FTP User:/var/ftp:/sbin/nologin

[root@anon7ftp7server ~]# chown -R ftp:ftp /var/ftp/pub/
[root@anon7ftp7server ~]# chmod 755 /var/ftp/pub/

[root@anon7ftp7server ~]# vim /etc/vsftpd/vsftpd.conf    # 如下配置是针对 匿名访问 的设置
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
[root@anon7ftp7server ~]# systemctl start vsftpd
[root@anon7ftp7server ~]# systemctl enable vsftpd
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
Name (192.168.175.10:root): ftp    <--- 匿名登录, 输入 用户名 'ftp'
331 Please specify the password.
Password:      <---  直接 回车
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> help   <--- 查看帮助, 显示可用命令
Commands may be abbreviated.  Commands are:

!               debug           mdir            sendport        site
$               dir             mget            put             size
account         disconnect      mkdir           pwd             status
append          exit            mls             quit            struct
ascii           form            mode            quote           system
bell            get             modtime         recv            sunique
binary          glob            mput            reget           tenex
bye             hash            newer           rstatus         tick
case            help            nmap            rhelp           trace
cd              idle            nlist           rename          type
cdup            image           ntrans          reset           user
chmod           lcd             open            restart         umask
close           ls              prompt          rmdir           verbose
cr              macdef          passive         runique         ?
delete          mdelete         proxy           send
ftp> help ls  <--- 查看指定 命令的帮助信息
ls              list contents of remote directory
ftp> ls   <--- 执行 ls 命令
227 Entering Passive Mode (192,168,175,10,171,58).
150 Here comes the directory listing.
drwxr-xr-x    3 14       50             30 Jun 07 11:02 pub
226 Directory send OK.
ftp> cd pub   <--- 切换目录
250 Directory successfully changed.
ftp> quit   <--- 退出
221 Goodbye.

ftp 内部 的 常用的命令有:

         lcd
         get
         mget
----------------------------------------------------
[root@client ~]# yum -y install lftp     # 安装 ftp 客户端工具 lftp

[root@client ~]# lftp 192.168.175.10     # 更多信息见 man lftp
lftp 192.168.175.10:~> ls   <-- 执行 ls 命令
drwxr-xr-x    3 14       50             30 Jun 07 11:02 pub
lftp 192.168.175.10:/> help help  <--- 查看 help 命令的帮助信息
Usage: help [<cmd>]
Print help for command <cmd>, or list of available commands
lftp 192.168.175.10:/> help  <--- 查看帮助信息

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

   https://serverfault.com/questions/247096/allow-anonymous-upload-for-vsftpd
