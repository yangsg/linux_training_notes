
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






---------------------------------------------------------------------------------------------------
网上资料:

Where is the SSH Server Fingerprint generated/stored?
    https://askubuntu.com/questions/76337/where-is-the-ssh-server-fingerprint-generated-stored

Calculate RSA key fingerprint
    https://stackoverflow.com/questions/9607295/calculate-rsa-key-fingerprint

SSH key-type, rsa, dsa, ecdsa, are there easy answers for which to choose when?
    https://security.stackexchange.com/questions/23383/ssh-key-type-rsa-dsa-ecdsa-are-there-easy-answers-for-which-to-choose-when

rsa dsa ecdsa 哪个好
    https://developer.aliyun.com/ask/126574?spm=a2c6h.13159736


[root@python3lang ~]# grep -Ei 'HostKey' /etc/ssh/sshd_config
      HostKey /etc/ssh/ssh_host_rsa_key  <----- 这些 key files 都是在安装 openssh-server package 时自动生成的
      #HostKey /etc/ssh/ssh_host_dsa_key
      HostKey /etc/ssh/ssh_host_ecdsa_key
      HostKey /etc/ssh/ssh_host_ed25519_key

// 利用 public key 查看 指纹(fingerprint), # 注: master 的 ip: 192.168.175.100
// -l      Show fingerprint of specified public key file.
[root@master ~]# ssh-keygen -l -f /etc/ssh/ssh_host_ecdsa_key.pub
    256 SHA256:0wZaw1B2PpNE444Oszvpuk8H23eSIi/S4dotH1Ns5yw no comment (ECDSA)   <---------

// -E fingerprint_hash #指定显示 key fingerprints时的hash算法. 合法的选项值为 “md5” 和 “sha256”.  默认为 “sha256”.
[root@master ~]# ssh-keygen -E md5 -lf /etc/ssh/ssh_host_ecdsa_key.pub
      256 MD5:04:0d:cf:28:f8:41:17:2e:b3:03:cc:68:4c:26:2c:3f no comment (ECDSA)  <---


// 在主机 python3lang 通过 ssh 连接 master, 观察 master 提供的主机指纹信息
[root@python3lang ~]# ssh root@192.168.175.100
    The authenticity of host '192.168.175.100 (192.168.175.100)' can't be established.
    ECDSA key fingerprint is SHA256:0wZaw1B2PpNE444Oszvpuk8H23eSIi/S4dotH1Ns5yw.   <--------
    ECDSA key fingerprint is MD5:04:0d:cf:28:f8:41:17:2e:b3:03:cc:68:4c:26:2c:3f.  <---
    Are you sure you want to continue connecting (yes/no)?







