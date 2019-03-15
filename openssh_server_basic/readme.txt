
ssh: tcp/22

服务器端：
// 查看openssh-server是否安装,如果没有安装，执行命令`yum -y install openssh-server`安装
[root@server ~]# rpm -q openssh-server
    openssh-server-7.4p1-11.el7.x86_64

[root@server ~]# netstat -anptu | grep :22


Centos客户端： //注：生产环境中应该禁用root账户远程登录
[root@client ~]# rpm -q openssh-clients   #必要时执行 yum -y install openssh-clients
    openssh-clients-7.4p1-11.el7.x86_64

// 远程登录
[root@client ~]# ssh root@192.168.175.10 -p 22
[root@client ~]# ssh root@192.168.175.10

// 远程执行命令
[root@client ~]# ssh root@192.168.175.10 'hostname; date'

// 远程copy
[root@client ~]# scp    /etc/fstab     root@192.168.175.10:/tmp
[root@client ~]# scp -r /root/dir01/   root@192.168.175.10:/tmp   #-r: 递归copy目录

// rsync 增量copy
[root@client ~]# rsync -av /root/dir01/  root@192.168.175.10:/tmp   #对于rsync, 此处 /root/dir01/ 表示copy目录下的内容,不包含目录本身
[root@client ~]# rsync -av /root/dir01   root@192.168.175.10:/tmp   #对于rsync, 此处 /root/dir01  表示copy目录即其内容



[root@client ~]# cat .ssh/known_hosts   #该文件包含了已连接过的主机的公钥信息,详见 `man sshd`
192.168.175.10 ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBGNWCzoVv1dJ6G1bALkioy93tc5Al/MFC7Ng/jXoIoWGzwbbB5eN4JOAsfCBMp/RJUMmIbqvEXrqZNxbu9CT7LE=


Windows上XShell客户端:
[c:\~]$ ssh root@192.168.175.10  22
[c:\~]$ ssh root@192.168.175.10


-----------
// 实现客户端免密登录
// 针对linux系统
[root@client ~]# ssh-keygen
[root@client ~]# ls -l .ssh/id_rsa .ssh/id_rsa.pub
[root@client ~]# ssh-copy-id root@192.168.175.10    #将公钥copy给远程服务器

[root@server ~]# ls .ssh
    authorized_keys


// 针对windows上的xshell客户端软件
  step01:  菜单：[工具] -> [新建用户秘钥生成向导W...] -> [秘钥类型 rsa] ....
  step02:  将step01中生成的公钥copy给服务器

-----------

// ssh 服务端的安全及连接速度设置(注意：和设置防火墙类似，不要将自己"锁在门外")
[root@server ~]# vim /etc/ssh/sshd_config
        Port 44444
        PermitRootLogin no
        MaxAuthTries 1
        PasswordAuthentication no
        GSSAPIAuthentication no
        UseDNS no















