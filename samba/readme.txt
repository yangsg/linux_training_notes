

协议: SMB/CIFS

端口:
    smb   tcp/139   tcp/445
    nmb   udp/137   udp/138

---------------------------------------------------------------------------------------------------

sambaserver ip: 192.168.175.10/24

// 安装软件
[root@sambaserver ~]# yum -y install samba samba-client

// 验证安装
[root@sambaserver ~]# rpm -q samba samba-client
    samba-4.8.3-4.el7.x86_64
    samba-client-4.8.3-4.el7.x86_64

// 创建 samba user account 注:the default passdb backends 要求 the user to already exist in the system password file (usually /etc/passwd)
[root@sambaserver ~]# useradd Bob
[root@sambaserver ~]# groupadd smbgrp
[root@sambaserver ~]# usermod -a -G smbgrp Bob
[root@sambaserver ~]# smbpasswd -a Bob         # 添加 samba user account (注: 该 user 必须在 /etc/passwd 中 已经存在, 即其应该已经是一个存在了的系统用户)
New SMB password:
Retype new SMB password:
Added user Bob.


[root@sambaserver ~]# pdbedit -L     # 查看 samba user account  (pdbedit -L 列出 samba 的 user databases 中的所有的 user account)
Bob:1001:

[root@sambaserver ~]# mkdir -p /samba_srv/secure
[root@sambaserver ~]# chown -R Bob:smbgrp /samba_srv/secure/
[root@sambaserver ~]# chmod -R 0770 /samba_srv/secure/


// 修改配置
[root@sambaserver ~]# vim /etc/samba/smb.conf

## 其实还可以禁用一些不需要的其他share, 参考: https://github.com/yangsg/linux_training_notes/blob/master/samba/sambaserver/etc/samba/smb.conf

##  注释掉 [homes] section, 即不 提供对用户家目录的共享
#[homes]
#       comment = Home Directories
#       valid users = %S, %D%w%S
#       browseable = No
#       read only = No
#       inherit acls = Yes


## 定义 名为 Secure 的 file space share
[Secure]
path = /samba_srv/secure
valid users = @smbgrp
writable = yes
browsable = yes


[root@sambaserver ~]# testparm --suppress-prompt   # 修改完 /etc/samba/smb.conf 之后 检查其 是否 正确.


[root@sambaserver ~]# systemctl start smb nmb      # 启动 smb 和 nmb 服务
[root@sambaserver ~]# systemctl enable smb nmb     # 将 smb
Created symlink from /etc/systemd/system/multi-user.target.wants/smb.service to /usr/lib/systemd/system/smb.service.
Created symlink from /etc/systemd/system/multi-user.target.wants/nmb.service to /usr/lib/systemd/system/nmb.service.


[root@sambaserver ~]# netstat -anptu
Active Internet connections (servers and established)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 0.0.0.0:139             0.0.0.0:*               LISTEN      1811/smbd
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      892/sshd
tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      973/master
tcp        0      0 0.0.0.0:445             0.0.0.0:*               LISTEN      1811/smbd
tcp        0      0 192.168.175.10:22       192.168.175.1:11552     ESTABLISHED 1023/sshd: root@pts
tcp6       0      0 :::139                  :::*                    LISTEN      1811/smbd
tcp6       0      0 :::22                   :::*                    LISTEN      892/sshd
tcp6       0      0 ::1:25                  :::*                    LISTEN      973/master
tcp6       0      0 :::445                  :::*                    LISTEN      1811/smbd
udp        0      0 192.168.175.255:137     0.0.0.0:*                           1823/nmbd
udp        0      0 192.168.175.10:137      0.0.0.0:*                           1823/nmbd
udp        0      0 0.0.0.0:137             0.0.0.0:*                           1823/nmbd
udp        0      0 192.168.175.255:138     0.0.0.0:*                           1823/nmbd
udp        0      0 192.168.175.10:138      0.0.0.0:*                           1823/nmbd
udp        0      0 0.0.0.0:138             0.0.0.0:*                           1823/nmbd



在windows测试访问:

  访问方法1)
        \\192.168.175.10

  访问方法2)
        映射网络驱动器:
            step01: 右键点击 [我的电脑] -> 选择 [映射网络驱动器]
            step02: 在弹出的对象框中 选择驱动器号(即盘符) 和 共享目录的访问路径,访问路径格式如下：
                            \\服务IP\共享名称   如:  \\192.168.175.10\Secure

        取消网路驱动器的方法:
             右键点击 网络驱动器对应的盘符 -> 在弹出菜单中选择 [断开连接] 即可

在 linux 客户端访问:
[root@basic ~]# smbclient //192.168.175.10/Secure -U Bob
Enter SAMBA\Bob's password:
Try "help" to get a list of possible commands.
smb: \> help
?              allinfo        altname        archive        backup
blocksize      cancel         case_sensitive cd             chmod
chown          close          del            deltree        dir
du             echo           exit           get (常用)     getfacl
geteas         hardlink       help           history        iosize
lcd  (常用)    link           lock           lowercase      ls
l              mask           md             mget           mkdir
more           mput           newer          notify         open
posix          posix_encrypt  posix_open     posix_mkdir    posix_rmdir
posix_unlink   posix_whoami   print          prompt         put (常用)
pwd            q              queue          quit           readlink
rd             recurse        reget          rename         reput
rm             rmdir          showacls       setea          setmode
scopy          stat           symlink        tar            tarmode
timeout        translate      unlock         volume         vuid
wdel           logon          listconnect    showconnect    tcon
tdis           tid            utimes         logoff         ..
!
smb: \> help lcd
HELP lcd:
        [directory] change/report the local current working directory

smb: \>


[root@basic ~]# smbclient -L //192.168.175.10/Secure -U Bob   # 列出 samba server 提供的 可用的 services
      Enter SAMBA\Bob's password:

              Sharename       Type      Comment
              ---------       ----      -------
              Secure          Disk      secure share folder
              IPC$            IPC       IPC Service (Samba 4.8.3)   <--关于IPC$ 的信息见 https://www.cyberciti.biz/faq/samba-restrict-access-to-ipc-share/
      Reconnecting with SMB1 for workgroup listing.

              Server               Comment
              ---------            -------

              Workgroup            Master
              ---------            -------
              SAMBA                SAMBASERVER


---------------------------------------------------------------------------------------------------


网上资料:
    https://linuxhint.com/install_samba_centos7/
    https://www.tecmint.com/install-samba4-on-centos-7-for-file-sharing-on-windows/
    https://lintut.com/easy-samba-installation-on-rhel-centos-7/
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/chap-managing_confined_services-samba#sect-Managing_Confined_Services-Samba-Samba_and_SELinux
    https://support.microsoft.com/en-in/help/4046019/guest-access-in-smb2-disabled-by-default-in-windows-10-and-windows-ser
    https://www.cnblogs.com/muscleape/p/6385583.html
    https://www.cnblogs.com/zoulongbin/p/7216246.html

    https://wiki.samba.org/index.php/User_Documentation
    https://devel.samba.org/

    http://www.ubiqx.org/cifs/

    https://www.cyberciti.biz/faq/samba-restrict-access-to-ipc-share/
    https://support.microsoft.com/en-us/help/3034016/ipc-share-and-null-session-behavior-in-windows

man samba
man 5 smb.conf
man smbpasswd
man pdbedit
man testparm


vim /etc/samba/smb.conf.example  #查看示例 配置文件


[root@sambaserver ~]# ls /var/lib/samba/private/{passdb.tdb,secrets.tdb}   #<--- 存放 samba 用户 账号 和 密码 的数据库文件
/var/lib/samba/private/passdb.tdb  /var/lib/samba/private/secrets.tdb

