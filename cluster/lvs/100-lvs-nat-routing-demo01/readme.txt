


---------------------------------------------------------------------------------------------------
先准备如下图所示的环境, 同时配置好时间同步, 在 real server 上安装好 演示用的 httpd 软件


                                                     |--- lvs_real_server01
                                                     |       rip:    192.168.40.101
                                                     |       gateway:192.168.40.100
                                                     |
    client  <---------->  lsv_director <------------>|
                   <->vip: 192.168.175.100           |
                      dip: 192.168.40.100<->        |
                                                     |
                                                     |--- lvs_real_server02
                                                             rip:    192.168.40.102
                                                             gateway:192.168.40.100


---------------------------------------------------------------------------------------------------
配置两台 real servers:

在两台 real server 上 设置并启动 相应的服务(本示例用 httpd 服务作为演示)

[root@lvs_real_server01 ~]# echo lvs_real_server01  > /var/www/html/index.html
[root@lvs_real_server01 ~]# systemctl start httpd
[root@lvs_real_server01 ~]# systemctl enable httpd

// 测试一下是否可以正常访问
[root@lsv_director ~]# curl 192.168.40.101
    lvs_real_server01



[root@lvs_real_server02 ~]# echo lvs_real_server02  > /var/www/html/index.html
[root@lvs_real_server02 ~]# systemctl start httpd
[root@lvs_real_server02 ~]# systemctl enable httpd

// 测试一下是否可以正常访问
[root@lsv_director ~]# curl 192.168.40.102
    lvs_real_server02

---------------------------------------------------------------------------------------------------
配置 lsv_director server:

// 启用 ip_forward 功能
[root@lsv_director ~]# vim /etc/sysctl.conf
      net.ipv4.ip_forward=1

    注: 可使用命令 `echo 1 > /proc/sys/net/ipv4/ip_forward`  或 `sysctl -w net.ipv4.ip_forward=1` 临时启用路由转发功能

[root@lsv_director ~]# sysctl -p   #  当-p没有接文件路径时，则默认加载文件/etc/sysctl.conf中的配置
      net.ipv4.ip_forward = 1



// 下载 the virtual server table in the Linux kernel 的管理工具
[root@lsv_director ~]# yum -y install ipvsadm
[root@lsv_director ~]# rpm -q ipvsadm
      ipvsadm-1.27-7.el7.x86_64


// 查看帮助
[root@lsv_director ~]# man ipvsadm   # 在线 man page 见:   https://linux.die.net/man/8/ipvsadm
[root@lsv_director ~]# ipvsadm --help | less

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













