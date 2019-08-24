
https://github.com/yangsg/linux_training_notes/tree/master/cluster/lvs

---------------------------------------------------------------------------------------------------
拓扑结构如下图所示, 同时配置好时间同步, 在 real server 上安装好 演示用的 httpd 软件




                                                                   |--- lvs_real_server01
                                                                   |      ens33: rip:    192.168.175.102
                                                                   |             gateway:192.168.175.2
                                                                   |
                                                                   |         lo: vip:192.168.175.100/32 ->
                                                                   |             (hidden: arp_ignore=1, arp_announce=2)
    client  <--- router------->  lvs_director <------------------->|                注意:一定要先设置好hidden效果, 然后再去配置vip
                      ens33:                                       |
                        ->vip: 192.168.175.100/32(visible)         |
                          dip: 192.168.175.101->                   |
                          gateway:192.168.175.2                    |
                                                                   |--- lvs_real_server02
                                                                   |       ens33: rip:    192.168.175.103
                                                                   |              gateway:192.168.175.2
                                                                   |
                                                                   |        lo: vip:192.168.175.100/32 ->
                                                                   |            (hidden: arp_ignore=1, arp_announce=2)
                                                                   |                注意:一定要先设置好hidden效果, 然后再去配置vip





----------------------------------------------------------------------------------------------------
配置 lvs_real_server01

    注: 一定要先设置好 arp_ignore 和 arp_announce 内核参数, 然后再去配置 vip

// 设置 内核参数 arp_ignore 为 1 和 arp_announce 为 2
[root@lvs_real_server01 ~]# vim /etc/sysctl.conf

        net.ipv4.conf.all.arp_ignore = 1
        net.ipv4.conf.all.arp_announce = 2

[root@lvs_real_server01 ~]# sysctl -p    #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
    net.ipv4.conf.all.arp_ignore = 1
    net.ipv4.conf.all.arp_announce = 2

[root@lvs_real_server01 ~]# cat /proc/sys/net/ipv4/conf/all/arp_ignore
    1
[root@lvs_real_server01 ~]# cat /proc/sys/net/ipv4/conf/all/arp_announce
    2


// 在 文件 ifcfg-lo 中配置 vip, 即追加 如下 两行
[root@lvs_real_server01 ~]# vim /etc/sysconfig/network-scripts/ifcfg-lo

      IPADDR1=192.168.175.100
      PREFIX1=32

// 使如上 vip 配置生效
[root@lvs_real_server01 ~]# ifup lo

[root@lvs_real_server01 ~]# ip addr show lo
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
          link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
          inet 127.0.0.1/8 scope host lo
             valid_lft forever preferred_lft forever
          inet 192.168.175.100/32 brd 192.168.175.100 scope host lo  <----- 观察
             valid_lft forever preferred_lft forever
          inet6 ::1/128 scope host
             valid_lft forever preferred_lft forever

[root@lvs_real_server01 ~]# route -n
      Kernel IP routing table
      Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
      0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
      192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33


[root@lvs_real_server01 ~]# echo 'vs_real_server01' > /var/www/html/index.html
[root@lvs_real_server01 ~]# systemctl start httpd
[root@lvs_real_server01 ~]# systemctl enable httpd

[root@lvs_real_server01 ~]# curl http://192.168.175.102:80
    vs_real_server01



----------------------------------------------------------------------------------------------------
配置 lvs_real_server02

    注: 一定要先设置好 arp_ignore 和 arp_announce 内核参数, 然后再去配置 vip

// 设置 内核参数 arp_ignore 为 1 和 arp_announce 为 2
[root@lvs_real_server02 ~]# vim /etc/sysctl.conf

        net.ipv4.conf.all.arp_ignore = 1
        net.ipv4.conf.all.arp_announce = 2

[root@lvs_real_server02 ~]# sysctl -p    #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
    net.ipv4.conf.all.arp_ignore = 1
    net.ipv4.conf.all.arp_announce = 2

[root@lvs_real_server02 ~]# cat /proc/sys/net/ipv4/conf/all/arp_ignore
    1
[root@lvs_real_server02 ~]# cat /proc/sys/net/ipv4/conf/all/arp_announce
    2


// 在 文件 ifcfg-lo 中配置 vip, 即追加 如下 两行
[root@lvs_real_server02 ~]# vim /etc/sysconfig/network-scripts/ifcfg-lo

      IPADDR1=192.168.175.100
      PREFIX1=32

// 使如上 vip 配置生效
[root@lvs_real_server02 ~]# ifup lo

[root@lvs_real_server02 ~]# ip addr show lo
      1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
          link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
          inet 127.0.0.1/8 scope host lo
             valid_lft forever preferred_lft forever
          inet 192.168.175.100/32 brd 192.168.175.100 scope host lo  <----- 观察
             valid_lft forever preferred_lft forever
          inet6 ::1/128 scope host
             valid_lft forever preferred_lft forever

[root@lvs_real_server02 ~]# route -n
      Kernel IP routing table
      Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
      0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
      192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33


[root@lvs_real_server02 ~]# echo 'vs_real_server02' > /var/www/html/index.html
[root@lvs_real_server02 ~]# systemctl start httpd
[root@lvs_real_server02 ~]# systemctl enable httpd

[root@lvs_real_server02 ~]# curl http://192.168.175.103:80
    vs_real_server02

---------------------------------------------------------------------------------------------------

[root@lvs_director ~]# vim /etc/sysconfig/network-scripts/ifcfg-ens33

        TYPE=Ethernet
        BOOTPROTO=none
        NAME=ens33
        DEVICE=ens33
        ONBOOT=yes

        IPADDR=192.168.175.101
        PREFIX=24
        GATEWAY=192.168.175.2
        DNS1=192.168.175.2

        # 如下两行用户配置 vip
        IPADDR1=192.168.175.100
        PREFIX1=32

[root@lvs_director ~]# nmcli conn reload
[root@lvs_director ~]# nmcli conn up ens33

[root@lvs_director ~]# ip addr show ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 00:0c:29:f6:f0:83 brd ff:ff:ff:ff:ff:ff
    inet 192.168.175.101/24 brd 192.168.175.255 scope global ens33
       valid_lft forever preferred_lft forever
    inet 192.168.175.100/32 brd 192.168.175.100 scope global ens33  <----- 观察
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fef6:f083/64 scope link
       valid_lft forever preferred_lft forever

[root@lvs_director ~]# route -n
      Kernel IP routing table
      Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
      0.0.0.0         192.168.175.2   0.0.0.0         UG    100    0        0 ens33
      192.168.175.0   0.0.0.0         255.255.255.0   U     100    0        0 ens33
      192.168.175.100 0.0.0.0         255.255.255.255 UH    100    0        0 ens33


---------------------------------------------------------------------------------------------------


// 安装 the virtual server table in the Linux kernel 的管理工具
[root@lvs_director ~]# yum -y install ipvsadm
[root@lvs_director ~]# rpm -q ipvsadm
      ipvsadm-1.27-7.el7.x86_64

[root@lvs_director ~]# rpm -ql ipvsadm

          /etc/sysconfig/ipvsadm-config           <----
          /usr/lib/systemd/system/ipvsadm.service <----
          /usr/sbin/ipvsadm                       <----
          /usr/sbin/ipvsadm-restore               <----
          /usr/sbin/ipvsadm-save                  <----
          /usr/share/doc/ipvsadm-1.27
          /usr/share/doc/ipvsadm-1.27/README      <----
          /usr/share/man/man8/ipvsadm-restore.8.gz
          /usr/share/man/man8/ipvsadm-save.8.gz
          /usr/share/man/man8/ipvsadm.8.gz



// 查看一下 service unit file 内容
[root@lvs_director ~]# cat /usr/lib/systemd/system/ipvsadm.service
      [Unit]
      Description=Initialise the Linux Virtual Server
      After=syslog.target network.target

      [Service]
      Type=oneshot
      ExecStart=/bin/bash -c "exec /sbin/ipvsadm-restore < /etc/sysconfig/ipvsadm"
      ExecStop=/bin/bash -c "exec /sbin/ipvsadm-save -n > /etc/sysconfig/ipvsadm"
      ExecStop=/sbin/ipvsadm -C
      RemainAfterExit=yes

      [Install]
      WantedBy=multi-user.target





// 查看帮助
[root@lvs_director ~]# man ipvsadm   # 在线 man page 见:   https://linux.die.net/man/8/ipvsadm
[root@lvs_director ~]# ipvsadm --help | less

        Usage:
          ipvsadm -A|E -t|u|f service-address [-s scheduler] [-p [timeout]] [-M netmask] [--pe persistence_engine] [-b sched-flags]
          ipvsadm -D -t|u|f service-address
          ipvsadm -C
          ipvsadm -R
          ipvsadm -S [-n]
          ipvsadm -a|e -t|u|f service-address -r server-address [options]
          ipvsadm -d -t|u|f service-address -r server-address
          ipvsadm -L|l [options]
          ipvsadm -Z [-t|u|f service-address]
          ipvsadm --set tcp tcpfin udp
          ipvsadm --start-daemon state [--mcast-interface interface] [--syncid sid]
          ipvsadm --stop-daemon state
          ipvsadm -h

        Commands:
        Either long or short options are allowed.
          --add-service     -A        add virtual service with options
          --edit-service    -E        edit virtual service with options
          --delete-service  -D        delete virtual service
          --clear           -C        clear the whole table
          --restore         -R        restore rules from stdin
          --save            -S        save rules to stdout
          --add-server      -a        add real server with options
          --edit-server     -e        edit real server with options
          --delete-server   -d        delete real server
          --list            -L|-l     list the table
          --zero            -Z        zero counters in a service or all services
          --set tcp tcpfin udp        set connection timeout values
          --start-daemon              start connection sync daemon
          --stop-daemon               stop connection sync daemon
          --help            -h        display this help message

        Options:
          --tcp-service  -t service-address   service-address is host[:port]
          --udp-service  -u service-address   service-address is host[:port]
          --fwmark-service  -f fwmark         fwmark is an integer greater than zero
          --ipv6         -6                   fwmark entry uses IPv6
          --scheduler    -s scheduler         one of rr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq,
                                              the default scheduler is wlc.
          --pe            engine              alternate persistence engine may be sip,
                                              not set by default.
          --persistent   -p [timeout]         persistent service
          --netmask      -M netmask           persistent granularity mask
          --real-server  -r server-address    server-address is host (and port)
          --gatewaying   -g                   gatewaying (direct routing) (default)
          --ipip         -i                   ipip encapsulation (tunneling)
          --masquerading -m                   masquerading (NAT)
          --weight       -w weight            capacity of real server
          --u-threshold  -x uthreshold        upper threshold of connections
          --l-threshold  -y lthreshold        lower threshold of connections
          --mcast-interface interface         multicast interface for connection sync
          --syncid sid                        syncid for connection sync (default=255)
          --connection   -c                   output of current IPVS connections
          --timeout                           output of timeout (tcp tcpfin udp)
          --daemon                            output of daemon information
          --stats                             output of statistics information
          --rate                              output of rate information
          --exact                             expand numbers (display exact values)
          --thresholds                        output of thresholds information
          --persistent-conn                   output of persistent connection info
          --nosort                            disable sorting output of service/server entries
          --sort                              does nothing, for backwards compatibility
          --ops          -o                   one-packet scheduling
          --numeric      -n                   numeric output of addresses and ports
          --sched-flags  -b flags             scheduler flags (comma-separated)


// 在 vip 上 添加 虚拟服务 (Add  a  virtual  service)
//   语法:  ipvsadm -A|E -t|u|f service-address [-s scheduler] [-p [timeout]] [-M netmask] [--pe persistence_engine] [-b sched-flags]
[root@lvs_director ~]# ipvsadm -A -t 192.168.175.100:80 -s rr  #注: -s scheduler 中 scheduler 默认为 wlc, 此处采用 rr 仅是为了方便测试观察效果

      注:
          --add-service     -A        add virtual service with options
          --tcp-service  -t service-address   service-address is host[:port]
          --scheduler    -s scheduler         one of rr|wrr|lc|wlc|lblc|lblcr|dh|sh|sed|nq,



// 查看效果(以数字显示)
[root@lvs_director ~]# ipvsadm -L -n
    IP Virtual Server version 1.2.1 (size=4096)
    Prot LocalAddress:Port Scheduler Flags
      -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
    TCP  192.168.175.100:80 rr   <------- 观察


[root@lvs_director ~]# ipvsadm -L
    IP Virtual Server version 1.2.1 (size=4096)
    Prot LocalAddress:Port Scheduler Flags
      -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
    TCP  localhost:http rr


// 在 virtual service 上 添加 real server (注: lvs DR 模式不支持 port 映射,所以不要再 rip 后指定 port, 即使用相同的端口)
//   语法: ipvsadm -a|e -t|u|f service-address -r server-address [options]

[root@lvs_director ~]# ipvsadm -a -t 192.168.175.100:80 -r 192.168.175.102 -g
[root@lvs_director ~]# ipvsadm -a -t 192.168.175.100:80 -r 192.168.175.103 -g
        注:
          --add-server      -a        add real server with options
          --tcp-service  -t service-address   service-address is host[:port]
          --real-server  -r server-address    server-address is host (and port)
          --masquerading -m                   masquerading (NAT)
          --gatewaying   -g                   gatewaying (direct routing) (default) (通过 gateway 直接响应,不用再经过director)
          --weight       -w weight            capacity of real server (weight 为 0 through to 65535. The default is 1.)
                                                                       weight 为 0 时 表示不再接受 new job 但仍为 既有的 jobs 提供服务

[root@lvs_director ~]# ipvsadm -L -n
      IP Virtual Server version 1.2.1 (size=4096)
      Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
      TCP  192.168.175.100:80 rr
        -> 192.168.175.102:80           Route   1      0          0
        -> 192.168.175.103:80           Route   1      0          0




// 测试一下
[root@client ~]# for i in $(seq 6); do curl 192.168.175.100:80; done
      vs_real_server02
      vs_real_server01
      vs_real_server02
      vs_real_server01
      vs_real_server02
      vs_real_server01


// 查看一下 the virtual server table 相关信息
[root@lvs_director ~]# ipvsadm -L -n
    IP Virtual Server version 1.2.1 (size=4096)
    Prot LocalAddress:Port Scheduler Flags
      -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
    TCP  192.168.175.100:80 rr
      -> 192.168.175.102:80           Route   1      0          3
      -> 192.168.175.103:80           Route   1      0          3



// 在 stdout 上显示 the IPVS table
[root@lvs_director ~]# ipvsadm-save
      -A -t localhost:http -s rr
      -a -t localhost:http -r localhost:http -g -w 1
      -a -t localhost:http -r localhost:http -g -w 1


[root@lvs_director ~]# ipvsadm-save -n    #-n     print out the table in numeric format.
      -A -t 192.168.175.100:80 -s rr
      -a -t 192.168.175.100:80 -r 192.168.175.102:80 -g -w 1
      -a -t 192.168.175.100:80 -r 192.168.175.103:80 -g -w 1



[root@lvs_director ~]# touch /etc/sysconfig/ipvsadm
[root@lvs_director ~]# ipvsadm-save -n > /etc/sysconfig/ipvsadm
[root@lvs_director ~]# systemctl start ipvsadm    # 注意, 文件 /etc/sysconfig/ipvsadm-config 中的配置可能会影响 ipvsadm.service 的某些行为
[root@lvs_director ~]# systemctl enable ipvsadm


至此, 一个简单的 dr 路由方式的 lvs 搭建完成
---------------------------------------------------------------------------------------------------







---------------------------------------------------------------------------------------------------
测试一下其他 某些 调度算法 或 选项

--------------------------------------------------

https://www.iyunv.com/thread-658681-1-1.html
      如果改规则的时候出现报错，内存分配问题（Memory allocation problem），解决办法，清掉规则，全部重新添加


// 测试一下 wrr
[root@lvs_director ~]# ipvsadm -C
[root@lvs_director ~]# ipvsadm -A -t 192.168.175.100:80 -s wrr
[root@lvs_director ~]# ipvsadm -a -t 192.168.175.100:80 -r 192.168.175.102 -g -w 4
[root@lvs_director ~]# ipvsadm -a -t 192.168.175.100:80 -r 192.168.175.103 -g


[root@lvs_director ~]# ipvsadm -L -n
    IP Virtual Server version 1.2.1 (size=4096)
    Prot LocalAddress:Port Scheduler Flags
      -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
    TCP  192.168.175.100:80 wrr
      -> 192.168.175.102:80           Route   4      0          5
      -> 192.168.175.103:80           Route   1      0          5



[root@client ~]# for i in {1..10}; do curl 192.168.175.100:80; done
        vs_real_server02
        vs_real_server01
        vs_real_server01
        vs_real_server01
        vs_real_server01
        vs_real_server02
        vs_real_server01
        vs_real_server01
        vs_real_server01
        vs_real_server01


[root@lvs_director ~]# ipvsadm -L -n
      IP Virtual Server version 1.2.1 (size=4096)
      Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
      TCP  192.168.175.100:80 wrr
        -> 192.168.175.102:80           Route   4      0          8
        -> 192.168.175.103:80           Route   1      0          2


--------------------------------------------------
// 测试一下 sh
[root@lvs_director ~]# ipvsadm -E -t 192.168.175.100:80 -s sh
[root@lvs_director ~]# ipvsadm -e -t 192.168.175.100:80 -r 192.168.175.102 -g -w 1


[root@lvs_director ~]# ipvsadm -L -n
    IP Virtual Server version 1.2.1 (size=4096)
    Prot LocalAddress:Port Scheduler Flags
      -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
    TCP  192.168.175.100:80 sh
      -> 192.168.175.102:80           Route   1      0          8
      -> 192.168.175.103:80           Route   1      0          2

[root@client ~]# for i in {1..10}; do curl 192.168.175.100:80; done
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02


[root@lvs_director ~]# ipvsadm -L -n
      IP Virtual Server version 1.2.1 (size=4096)
      Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
      TCP  192.168.175.100:80 sh
        -> 192.168.175.102:80           Route   1      0          0
        -> 192.168.175.103:80           Route   1      0          10




--------------------------------------------------


---------------------------------------------------------------------------------------------------
其他知识点
---------------------------------------------------------------------------------------------------

   -c, --connection
          Connection output. The list command with this option will list current IPVS connections.


[root@lvs_director ~]# ipvsadm -L -n -c
    IPVS connection entries
    pro expire state       source             virtual            destination
    TCP 04:56  NONE        192.168.175.30:0   192.168.175.100:80 192.168.175.102:80
    TCP 01:55  FIN_WAIT    192.168.175.30:41724 192.168.175.100:80 192.168.175.102:80
    TCP 01:55  FIN_WAIT    192.168.175.30:41734 192.168.175.100:80 192.168.175.102:80
    TCP 01:55  FIN_WAIT    192.168.175.30:41720 192.168.175.100:80 192.168.175.102:80

---------------------------------------------------------------------------------------------------
persistent 持久性


 -p, --persistent [timeout]
        Specify  that  a virtual service is persistent. If this option is specified, multiple requests from a client are redirected to the same real
        server selected for the first request.  Optionally, the timeout of persistent sessions may be specified  given  in  seconds,  otherwise  the
        default  of  300  seconds  will be used. This option may be used in conjunction with protocols such as SSL or FTP where it is important that
        clients consistently connect with the same real server.

        Note: If a virtual service is to handle FTP connections then persistence must be set for the virtual service if Direct Routing or Tunnelling
        is  used  as the forwarding mechanism. If Masquerading is used in conjunction with an FTP service than persistence is not necessary, but the
        ip_vs_ftp kernel module must be used.  This module may be manually inserted into the kernel using insmod(8).


[root@lvs_director ~]# ipvsadm -E -t 192.168.175.100:80 -s rr -p 300   # 单位: seconds 秒


[root@lvs_director ~]# ipvsadm-save -n

      -A -t 192.168.175.100:80 -s rr -p 300
      -a -t 192.168.175.100:80 -r 192.168.175.102:80 -g -w 1
      -a -t 192.168.175.100:80 -r 192.168.175.103:80 -g -w 1

[root@lvs_director ~]# ipvsadm -L -n

      IP Virtual Server version 1.2.1 (size=4096)
      Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
      TCP  192.168.175.100:80 rr persistent 300  <---- 观察
        -> 192.168.175.102:80           Route   1      0          0
        -> 192.168.175.103:80           Route   1      0          210


[root@client ~]# for i in {1..10}; do curl 192.168.175.100:80; done
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02
      vs_real_server02



----------------------------------------------------------------------------------------------------
防火墙标记/端口亲缘性


       -f, --fwmark-service integer
              Use  a  firewall-mark,  an  integer  value  greater than zero, to denote a virtual service instead of an
              address, port and protocol (UDP or TCP). The marking of packets with a firewall-mark is configured using
              the  -m|--mark option to iptables(8). It can be used to build a virtual service associated with the same
              real servers, covering multiple IP address, port and protocol triplets. If IPv6 addresses are used,  the
              -6 option must be used.

              Using  firewall-mark  virtual  services  provides  a convenient method of grouping together different IP
              addresses, ports and protocols into a single virtual service. This is useful for both  simplifying  con‐
              figuration if a large number of virtual services are required and grouping persistence across what would
              otherwise be multiple virtual services.


    https://access.redhat.com/documentation/en-US/Red_Hat_Enterprise_Linux/4/html-single/Virtual_Server_Administration/index.html
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-ftp-vsa
    https://www.lisenet.com/2015/setting-up-a-load-balancing-lvs-direct-routing-cluster-with-piranha/

    https://www.linuxtopia.org/online_books/linux_system_administration/redhat_cluster_configuration_and_management/s1-lvs-ftp.html
    http://www.austintek.com/LVS/LVS-HOWTO/HOWTO/LVS-HOWTO.fwmark.html

        fwmark is a way of aggregating an arbitary collection of VIP:port services
        into one virtual service (the entry made with ipvsadm -A). Thus a virtual
        service could be composed of multiple VIP:ports (e.g. VIP1:port1, VIP2:port2...VIPn:portn).
        This is usefull if the client needs to connect to all of the VIP:port services together on one realserver.

  Common uses for fwmark are

        aggregate VIP:http and VIP:https, so that when a client fills their shopping cart on VIP:http
        and they move to VIP:https (to give their credit card information), they will stay on the same realserver.

        with multi-port services like ftp (there are some wrinkles with ftp, since the 2nd port calls
        from the realserver rather than from the client - read the setup of ftp elsewhere in this section and in ftp).

        when the realserver is a squid. All traffic to port 80 (for all IPs) is aggregated with a fwmark.

    A minor advantage is that a realserver can be added, removed and re-weighted with one ipvsadm command.
    To enable fwmark, the packets coming into the director have to be labelled with a fwmark
    (some bits are flipped in the tcp packet). This is done with iptables (or ipchains).


[root@lvs_real_server01 ~]# yum -y install vsftpd
[root@lvs_real_server01 ~]# vim /etc/vsftpd/vsftpd.conf
    pasv_min_port=10000
    pasv_max_port=20000

[root@lvs_real_server01 ~]# systemctl start vsftpd
[root@lvs_real_server01 ~]# systemctl enable vsftpd



[root@lvs_real_server02 ~]# yum -y install vsftpd
[root@lvs_real_server02 ~]# vim /etc/vsftpd/vsftpd.conf
    pasv_min_port=10000
    pasv_max_port=20000

[root@lvs_real_server02 ~]# systemctl start vsftpd
[root@lvs_real_server02 ~]# systemctl enable vsftpd


[root@lvs_director ~]# iptables -t mangle -A PREROUTING -p tcp -d 192.168.175.100 --dport 21 -j MARK --set-mark 21
[root@lvs_director ~]# iptables -t mangle -A PREROUTING -p tcp -d 192.168.175.100 --dport 10000:20000 -j MARK --set-mark 21

[root@lvs_director ~]# ipvsadm -C
[root@lvs_director ~]# ipvsadm -A -f 21 -s rr -p 300
[root@lvs_director ~]# ipvsadm -a -f 21 -r 192.168.175.102 -g
[root@lvs_director ~]# ipvsadm -a -f 21 -r 192.168.175.103 -g

[root@lvs_director ~]# ipvsadm -L -n

      IP Virtual Server version 1.2.1 (size=4096)
      Prot LocalAddress:Port Scheduler Flags
        -> RemoteAddress:Port           Forward Weight ActiveConn InActConn
      FWM  21 rr persistent 300
        -> 192.168.175.102:0            Route   1      0          0
        -> 192.168.175.103:0            Route   1      0          0


[root@lvs_director ~]# ipvsadm-save -n
    -A -f 21 -s rr -p 300
    -a -f 21 -r 192.168.175.102:0 -g -w 1
    -a -f 21 -r 192.168.175.103:0 -g -w 1

[root@client ~]# yum -y install ftp

// 登录并执行一些操作, 见 https://github.com/yangsg/linux_training_notes/tree/master/ftp/anon7ftp7server
[root@client ~]# ftp 192.168.175.100


[root@lvs_director ~]# ipvsadm -L -n -c
        IPVS connection entries
        pro expire state       source             virtual            destination
        TCP 01:33  FIN_WAIT    192.168.175.30:58678 192.168.175.100:13294 192.168.175.103:13294
        TCP 01:33  FIN_WAIT    192.168.175.30:49000 192.168.175.100:15229 192.168.175.103:15229
        TCP 01:34  FIN_WAIT    192.168.175.30:45193 192.168.175.100:18541 192.168.175.103:18541
        TCP 01:41  FIN_WAIT    192.168.175.30:48020 192.168.175.100:21 192.168.175.103:21
        TCP 01:34  FIN_WAIT    192.168.175.30:34689 192.168.175.100:15209 192.168.175.103:15209
        TCP 01:33  FIN_WAIT    192.168.175.30:46546 192.168.175.100:12901 192.168.175.103:12901
        IP  00:35  NONE        192.168.175.30:0   0.0.0.21:0         192.168.175.103:0
        TCP 01:29  FIN_WAIT    192.168.175.30:33506 192.168.175.100:19324 192.168.175.103:19324
        TCP 01:35  FIN_WAIT    192.168.175.30:38834 192.168.175.100:19188 192.168.175.103:19188
        TCP 14:37  ESTABLISHED 192.168.175.30:48024 192.168.175.100:21 192.168.175.103:21
        TCP 01:21  FIN_WAIT    192.168.175.30:48022 192.168.175.100:21 192.168.175.103:21





