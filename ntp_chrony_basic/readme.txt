
ntp: udp/123

注: ntp 作为 server 是需要防火墙开放双向的 upd/123端口

注: chronyd 还开放了 udp/323端口用于 chronyc 命令远程监视和控制.
    如果要关闭 udp/323端口, 则在 /etc/chrony.conf 中设置 cmdport 0 即可,
    这并不会关闭 Unix domain command socket, 所以本地运行 chronyc 仍然可行.
	https://forums.docker.com/t/chronyd-listening-on-udp-323/14987

服务器端：
基本信息：
[root@ntp7server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@ntp7server ~]# uname -r
    3.10.0-693.el7.x86_64

[root@ntp7server ~]# timedatectl status | grep 'Time zone'
       Time zone: Asia/Shanghai (CST, +0800)

ip地址：192.168.175.123/24


[root@ntp7server ~]# yum -y install chrony
[root@ntp7server ~]# rpm -q chrony
    chrony-3.2-2.el7.x86_64


[root@ntp7server ~]# vim /etc/chrony.conf
    #server 0.centos.pool.ntp.org iburst
    #server 1.centos.pool.ntp.org iburst
    #server 2.centos.pool.ntp.org iburst
    #server 3.centos.pool.ntp.org iburst

    # http://www.ntp.org.cn/pool.php
    # https://help.aliyun.com/document_detail/92704.html
    server ntp1.aliyun.com iburst
    server ntp2.aliyun.com iburst
    server 0.cn.pool.ntp.org iburst
    server 1.cn.pool.ntp.org iburst


    allow 192.168.175.0/24

    local stratum 10


[root@ntp7server ~]# systemctl start chronyd
[root@ntp7server ~]# systemctl enable chronyd

[root@ntp7server ~]# chronyc sources -v
[root@ntp7server ~]# chronyc sourcestats -v
[root@ntp7server ~]# chronyc tracking
[root@ntp7server ~]# timedatectl  | grep 'NTP enabled'  # timedatectl set-ntp true

[root@ntp7server ~]# netstat -anptu | grep chronyd

客户端:
[root@ntp7client ~]# yum -y install chrony

[root@ntp7client ~]# vim /etc/chrony.conf

    #server 0.centos.pool.ntp.org iburst
    #server 1.centos.pool.ntp.org iburst
    #server 2.centos.pool.ntp.org iburst
    #server 3.centos.pool.ntp.org iburst

    server 192.168.175.123 iburst


[root@ntp7client ~]# systemctl start chronyd
[root@ntp7client ~]# systemctl enable chronyd

[root@ntp7client ~]# chronyc sources -v
[root@ntp7client ~]# timedatectl | grep 'NTP enabled'   # timedatectl set-ntp true

-----------------------
//其他：
//注：客户端也可以使用以前ntpdate的方式来保持与ntp server的同步
[root@ntp7client ~]# yum -y install ntpdate
[root@ntp7client ~]# ntpdate 192.168.175.123









