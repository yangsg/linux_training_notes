

服务器端：
基本信息：
[root@ntp7server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@ntp7server ~]# uname -r
    3.10.0-693.el7.x86_64

ip地址：192.168.175.123

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
    server ntp3.aliyun.com iburst
    server ntp4.aliyun.com iburst
    server ntp5.aliyun.com iburst
    server ntp6.aliyun.com iburst
    server ntp7.aliyun.com iburst

    allow 192.168.175.0/24

    local stratum 10


[root@ntp7server ~]# systemctl start chronyd
[root@ntp7server ~]# systemctl enable chronyd

[root@ntp7server ~]# chronyc sources -v
[root@ntp7server ~]# chronyc sourcestats -v
[root@ntp7server ~]# chronyc tracking
[root@ntp7server ~]# timedatectl  | grep 'NTP enabled'  #timedatectl set-ntp yes







