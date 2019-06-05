
// 修改主机名
[root@localhost ~]# hostnamectl set-hostname ns01.mytraining.com

// 配置 ip 地址
[root@ns01 ~]# vim /etc/sysconfig/network-scripts/ifcfg-ens33
      TYPE=Ethernet
      BOOTPROTO=none
      NAME=ens33
      DEVICE=ens33
      ONBOOT=yes


      IPADDR=192.168.175.170
      PREFIX=24
      GATEWAY=192.168.175.2
      DNS1=192.168.175.2




// 安装 bind (name server) 软件程序
[root@ns01 ~]# yum install -y bind bind-chroot


// 修改 和 创建相应配置文件 (略)


// 启动 服务 并 设置为 开机自启
[root@ns01 ~]# systemctl start named named-chroot
[root@ns01 ~]# systemctl enable named named-chroot


// 查看相应端口
[root@ns01 ~]# netstat -anptu | grep named
tcp        0      0 192.168.175.170:53      0.0.0.0:*               LISTEN      1851/named
tcp        0      0 127.0.0.1:53            0.0.0.0:*               LISTEN      1813/named
tcp        0      0 127.0.0.1:953           0.0.0.0:*               LISTEN      1813/named
tcp6       0      0 ::1:53                  :::*                    LISTEN      1813/named
tcp6       0      0 ::1:953                 :::*                    LISTEN      1813/named
udp        0      0 192.168.175.170:53      0.0.0.0:*                           1851/named
udp        0      0 127.0.0.1:53            0.0.0.0:*                           1851/named
udp        0      0 127.0.0.1:53            0.0.0.0:*                           1813/named
udp6       0      0 ::1:53                  :::*                                1813/named

[root@ns01 ~]# netstat -aptu | grep named
tcp        0      0 ns01.mytraining.:domain 0.0.0.0:*               LISTEN      1851/named
tcp        0      0 localhost:domain        0.0.0.0:*               LISTEN      1813/named
tcp        0      0 localhost:rndc          0.0.0.0:*               LISTEN      1813/named
tcp6       0      0 localhost:domain        [::]:*                  LISTEN      1813/named
tcp6       0      0 localhost:rndc          [::]:*                  LISTEN      1813/named
udp        0      0 ns01.mytraining.:domain 0.0.0.0:*                           1851/named
udp        0      0 localhost:domain        0.0.0.0:*                           1851/named
udp        0      0 localhost:domain        0.0.0.0:*                           1813/named
udp6       0      0 localhost:domain        [::]:*                              1813/named


// 测试 (利用类似 dig 或 nslookup 工具)
[root@ns01 ~]# dig @192.168.175.170  www.mytraining.com
[root@ns01 ~]# dig @192.168.175.170 -x 192.168.175.171



网上资料:
  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/ch-dns_servers#s2-dns-introduction-bind
  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/deployment_guide/s1-bind

  https://blog.51cto.com/wubinary/1375333
  http://linuxpitstop.com/dns-server-setup-using-bind-9-on-centos-7-linux/

