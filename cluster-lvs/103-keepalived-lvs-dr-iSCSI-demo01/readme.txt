
----------------------------------------------------------------------------------------------------

                                                                            |web01_server-------------------------------------------
                                                                            |    ens33: rip:     192.168.175.121                    |
                                                                            |           gateway: 192.168.175.2                      |
                                                                            |                                                       |
                                                                            |    lo: vip: 192.168.175.100/32->                      |
                      |--------------------------------------------------|  |     (hidden: arp_ignore=1, arp_announce=2)            |
                      |                                                  |  |      注意:一定要先设置好hidden效果, 然后再去配置vip   |
vip: 192.168.175.100  |                                                  |  |                                                       |
                      |   lvs_director01                                 |  |                                                       |
                      |->vip: 192.168.175.100/32(visible, by keepalived) |  |                                                       |
                      |     dip: 192.168.175.101->                       |  |                                                       |
                      |     gateway:192.168.175.2                        |  |                                                       |
                      |                                                  |  |                                                       |
                      |                                                  |->|                                                       |
                      |                                                  |  |                                                       |
                      |                                                  |  |                                         iscsi_share_storage
                      |                                                  |  |                                              ip: 192.168.175.130
                      |                                                  |  |                                                       |
                      |   lvs_director02                                 |  |                                                       |
                      |-> vip: 192.168.175.100/32(visible, by keepalived)|  |                                                       |
                      |     dip: 192.168.175.102->                       |  |                                                       |
                      |     gateway:192.168.175.2                        |  |                                                       |
                      |                                                  |  |                                                       |
                      |--------------------------------------------------|  |                                                       |
                                                                            |----web02_server ---------------------------------------
                                                                                   ens33: rip:     192.168.175.122
                                                                                          gateway: 192.168.175.2

                                                                                     lo: vip: 192.168.175.100/32->
                                                                                         (hidden: arp_ignore=1, arp_announce=2)
                                                                                          注意:一定要先设置好hidden效果, 然后再去配置vip



----------------------------------------------------------------------------------------------------
已经设置好时间同步

----------------------------------------------------------------------------------------------------
配置 web01_server:

    注: 一定要先设置好 arp_ignore 和 arp_announce 内核参数, 然后再去配置 vip

// 设置 内核参数 arp_ignore 为 1 和 arp_announce 为 2

[root@web01_server ~]# vim /etc/sysctl.conf

        net.ipv4.conf.all.arp_ignore = 1
        net.ipv4.conf.all.arp_announce = 2

[root@web01_server ~]# sysctl -p       #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
    net.ipv4.conf.all.arp_ignore = 1
    net.ipv4.conf.all.arp_announce = 2

[root@web01_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_ignore
    1
[root@web01_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_announce
    2

// 在 文件 ifcfg-lo 中配置 vip, 即追加 如下 两行
[root@web01_server ~]# vim /etc/sysconfig/network-scripts/ifcfg-lo

    IPADDR1=192.168.175.100
    PREFIX1=32


// 使如上 vip 配置生效
[root@web01_server ~]# ifup lo


[root@web01_server ~]# ip addr show lo
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet 192.168.175.100/32 brd 192.168.175.100 scope host lo  <----- 观察
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever


[root@web01_server ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
    192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33


[root@web01_server ~]# yum -y install httpd
[root@web01_server ~]# systemctl start httpd
[root@web01_server ~]# systemctl enable httpd

[root@web01_server ~]# echo 'web01_server' > /var/www/html/index.html

[root@web01_server ~]# curl http://192.168.175.121:80
    web01_server

----------------------------------------------------------------------------------------------------
配置 web02_server:

    注: 一定要先设置好 arp_ignore 和 arp_announce 内核参数, 然后再去配置 vip

// 设置 内核参数 arp_ignore 为 1 和 arp_announce 为 2

[root@web02_server ~]# vim /etc/sysctl.conf

        net.ipv4.conf.all.arp_ignore = 1
        net.ipv4.conf.all.arp_announce = 2

[root@web02_server ~]# sysctl -p       #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
    net.ipv4.conf.all.arp_ignore = 1
    net.ipv4.conf.all.arp_announce = 2

[root@web02_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_ignore
    1
[root@web02_server ~]# cat /proc/sys/net/ipv4/conf/all/arp_announce
    2

// 在 文件 ifcfg-lo 中配置 vip, 即追加 如下 两行
[root@web02_server ~]# vim /etc/sysconfig/network-scripts/ifcfg-lo

    IPADDR1=192.168.175.100
    PREFIX1=32


// 使如上 vip 配置生效
[root@web02_server ~]# ifup lo


[root@web02_server ~]# ip addr show lo
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet 192.168.175.100/32 brd 192.168.175.100 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever



[root@web02_server ~]# route -n
    Kernel IP routing table
    Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
    192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33



[root@web02_server ~]# yum -y install httpd
[root@web02_server ~]# systemctl start httpd
[root@web02_server ~]# systemctl enable httpd

[root@web02_server ~]# echo 'web02_server' > /var/www/html/index.html

[root@web02_server ~]# curl http://192.168.175.122:80
    web02_server


----------------------------------------------------------------------------------------------------





















