

服务器端：
[root@ntp7server ~]# yum -y install ntp

修改/etc/ntp.conf
      restrict 192.168.175.0 mask 255.255.255.0 nomodify notrap

      server 0.cn.pool.ntp.org iburst
      server 1.cn.pool.ntp.org iburst
      server 2.cn.pool.ntp.org iburst
      server 3.cn.pool.ntp.org iburst

      server 127.127.1.0 iburst
      fudge 127.127.1.0  stratum 10

[root@ntp7server ~]# systemctl start ntpd
[root@ntp7server ~]# systemctl enable ntpd


客户端：
[root@ntp7client ~]# yum -y install ntpdate
[root@ntp7client ~]# ntpdate 192.168.175.123  #与本地ntp服务器同步





