





                +------------------------vip: 192.168.175.100---------------------+
                |                                                                 |
                |          haproxy01               haproxy02                      |
                |            ip: 192.168.175.101      ip: 192.168.175.102         |
                |                                                                 |
                +------------------------------+----------------------------------+
                                               |
                                               |
                                               |
                             |----------------------------------|
                             |                                  |
                             |                                  |
                             |                                  |
               +----------------------------+      +----------------------------+
               |    bbs01.linux.com         |      |   blog01.linux.com         |
               |       ip: 192.168.175.121  |      |      ip: 192.168.175.131   |
               |                            |      |                            |
               |    bbs02.linux.com         |      |   blog02.linux.com         |
               |       ip: 192.168.175.122  |      |      ip: 192.168.175.132   |
               |                            |      |                            |
               +----------------------------+      +----------------------------+







----------------------------------------------------------------------------------------------------
初始化设置: 主机名, ip, 时钟同步 等


----------------------------------------------------------------------------------------------------
准备后端 4 台 real server 服务器

[root@bbs01 ~]# yum -y install httpd
[root@bbs01 ~]# systemctl start httpd
[root@bbs01 ~]# systemctl enable httpd

[root@bbs02 ~]# yum -y install httpd
[root@bbs02 ~]# systemctl start httpd
[root@bbs02 ~]# systemctl enable httpd

[root@blog01 ~]# yum -y install httpd
[root@blog01 ~]# systemctl start httpd
[root@blog01 ~]# systemctl enable httpd

[root@blog02 ~]# yum -y install httpd
[root@blog02 ~]# systemctl start httpd
[root@blog02 ~]# systemctl enable httpd

[root@bbs01 ~]# echo bbs01 > /var/www/html/index.html
[root@bbs02 ~]# echo bbs02 > /var/www/html/index.html
[root@blog01 ~]# echo blog01 > /var/www/html/index.html
[root@blog02 ~]# echo blog02 > /var/www/html/index.html


[root@haproxy01 ~]# for i in 121 122 131 132; do curl 192.168.175.$i; done
    bbs01
    bbs02
    blog01
    blog02

[root@haproxy02 ~]# for i in 121 122 131 132; do curl 192.168.175.$i; done
    bbs01
    bbs02
    blog01
    blog02



[root@haproxy01 ~]# yum -y install  haproxy
[root@haproxy02 ~]# yum -y install keepalived  haproxy


// 修改所有 httpd server 的  logformat 配置 让 httpd 能记录 真实的 client ip 而非 proxy 的 ip
// 此仅演示了 bbs01 的修改
[root@bbs01 ~]# vim /etc/httpd/conf/httpd.conf

    LogFormat "%{X-Forwarded-For}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined


[root@bbs01 ~]# systemctl restart httpd.service


----------------------------------------------------------------------------------------------------
配置 haproxy01  (仅与 haproxy 相关)

[root@haproxy01 ~]# yum -y install  haproxy


// 准备 haproxy 的 日志环境
//    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-haproxy-logging
[root@haproxy01 ~]# mkdir -p /var/lib/haproxy/dev
[root@haproxy01 ~]# vim /etc/rsyslog.conf

    # 使用 unix domain socket 的方式
    $ModLoad imuxsock
    $AddUnixListenSocket /var/lib/haproxy/dev/log
    # 注: 如果使用 udp 的方式, 可以启用如下两行;
    #$ModLoad imudp
    #$UDPServerRun 514

    local2.*                                                /var/log/haproxy.log

[root@haproxy01 ~]# systemctl restart rsyslog

// 设置 haproxy 配置
[root@haproxy01 ~]# cp /etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg.bak
[root@haproxy01 ~]# vim /etc/haproxy/haproxy.cfg

      # 注: 由于配置实在太多, 这里仅支持需要注意的地方
      #     现在暂时绑定到 dip, 后面与 keepalived 结合时,应该绑定到 vip,
      #     一步一步来
      listen admin_status
          bind 192.168.175.101:9088
      #略 略 略 略 略

      frontend web_service
          bind 192.168.175.101:80
      #略 略 略 略 略



[root@haproxy01 ~]# systemctl start haproxy.service
[root@haproxy01 ~]# systemctl enable haproxy.service

   注: 必要时应查看 `tail -f /var/log/messages`, 检查是否有某些错误信息

// 查看网络状态
[root@haproxy01 ~]# netstat -anptu | grep haproxy
    tcp        0      0 192.168.175.101:80      0.0.0.0:*               LISTEN      1649/haproxy
    tcp        0      0 192.168.175.101:9088    0.0.0.0:*               LISTEN      1649/haproxy

// 查看进程
[root@haproxy01 ~]# ps -elf | grep haproxy
    4 S root       1647      1  0  80   0 - 11169 do_wai 14:52 ?        00:00:00 /usr/sbin/haproxy-systemd-wrapper -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid
    4 S haproxy    1648   1647  0  80   0 - 12137 do_wai 14:52 ?        00:00:00 /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -Ds
    1 S haproxy    1649   1648  0  80   0 - 12137 ep_pol 14:52 ?        00:00:00 /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -Ds



// 客户端测试 haproxy01
[root@client ~]# vim /etc/hosts

    192.168.175.101 bbs.linux.com
    192.168.175.101 blog.linux.com


[root@client ~]# for i in {1..4}; do curl bbs.linux.com; done
    bbs02
    bbs01
    bbs02
    bbs01

[root@client ~]# for i in {1..4}; do curl blog.linux.com; done
    blog01
    blog02
    blog01
    blog02






----------------------------------------------------------------------------------------------------
配置 haproxy02  (仅与 haproxy 相关)

[root@haproxy02 ~]# yum -y install  haproxy


// 准备 haproxy 的 日志环境
//    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-haproxy-logging
[root@haproxy02 ~]# mkdir -p /var/lib/haproxy/dev
[root@haproxy02 ~]# vim /etc/rsyslog.conf

    # 使用 unix domain socket 的方式
    $ModLoad imuxsock
    $AddUnixListenSocket /var/lib/haproxy/dev/log
    # 注: 如果使用 udp 的方式, 可以启用如下两行;
    #$ModLoad imudp
    #$UDPServerRun 514

    local2.*                                                /var/log/haproxy.log




[root@haproxy02 ~]# systemctl restart rsyslog


// 设置 haproxy 配置 (将 haproxy01 对应的配置文件拷贝过来 然后修改)
[root@haproxy02 ~]# rsync -av root@192.168.175.101:/etc/haproxy/haproxy.cfg /etc/haproxy/haproxy.cfg
[root@haproxy02 ~]# vim /etc/haproxy/haproxy.cfg

      # 注: 由于配置实在太多, 这里仅支持需要注意的地方
      #     现在暂时绑定到 dip, 后面与 keepalived 结合时,应该绑定到 vip,
      #     一步一步来
      listen admin_status
          bind 192.168.175.102:9088
      #略 略 略 略 略

      frontend web_service
          bind 192.168.175.102:80
      #略 略 略 略 略



[root@haproxy02 ~]# systemctl start haproxy.service
[root@haproxy02 ~]# systemctl enable haproxy.service


   注: 必要时应查看 `tail -f /var/log/messages`, 检查是否有某些错误信息

// 查看网络状态
[root@haproxy02 ~]# netstat -anptu | grep haproxy
    tcp        0      0 192.168.175.102:80      0.0.0.0:*               LISTEN      1337/haproxy
    tcp        0      0 192.168.175.102:9088    0.0.0.0:*               LISTEN      1337/haproxy

// 查看进程
[root@haproxy02 ~]# ps -elf | grep haproxy
    4 S root       1335      1  0  80   0 - 11169 do_wai 15:13 ?        00:00:00 /usr/sbin/haproxy-systemd-wrapper -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid
    4 S haproxy    1336   1335  0  80   0 - 12137 do_wai 15:13 ?        00:00:00 /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -Ds
    1 S haproxy    1337   1336  0  80   0 - 12137 ep_pol 15:13 ?        00:00:00 /usr/sbin/haproxy -f /etc/haproxy/haproxy.cfg -p /run/haproxy.pid -Ds




// 客户端测试 haproxy02
[root@client ~]# vim /etc/hosts

    192.168.175.102 bbs.linux.com
    192.168.175.102 blog.linux.com



[root@client ~]# for i in {1..4}; do curl bbs.linux.com; done
    bbs02
    bbs01
    bbs02
    bbs01


[root@client ~]# for i in {1..4}; do curl blog.linux.com; done
    blog01
    blog02
    blog01
    blog02





----------------------------------------------------------------------------------------------------
配置 haproxy01  (keepalived 与 haproxy 结合)

// 启用非本地 ip 绑定功能(即允许当 vip 还不存在时 仍可将服务绑定到该 ip 上)
// 注: 如不想配置 net.ipv4.ip_nonlocal_bind, 则 haproxy 在 bind 时执行类似 *:80 或 0.0.0.0:80 的bind 即可.
[root@haproxy01 ~]# vim /etc/sysctl.conf

    net.ipv4.ip_nonlocal_bind = 1

[root@haproxy01 ~]# sysctl -p
    net.ipv4.ip_nonlocal_bind = 1

[root@haproxy01 ~]# sysctl net.ipv4.ip_nonlocal_bind
    net.ipv4.ip_nonlocal_bind = 1


// 安装 keepalived
[root@haproxy01 ~]# yum -y install keepalived



// keepalived 的文档:
//      https://keepalived.org/doc/
// keepalived 的 官网:
//      https://www.keepalived.org/
//  `man keepalived.conf`  其中 man page 包含了最详细的参数解释
//   在线man page 见 https://www.systutorials.com/docs/linux/man/5-keepalived.conf/
// 注: keepalived.conf 的 单行注释以 符号 '#' or '!' 开始
[root@haproxy01 ~]# vim /etc/keepalived/keepalived.conf

      ! Configuration File for keepalived

      global_defs {
         router_id haproxy01
      }

      #注: vrrp_instance 定义用于将 director(调度器) 加到虚拟组中,以实现互为备份
      vrrp_instance web_service_group {
          state MASTER
          interface ens33
          virtual_router_id 55   #作为 00-00-5E-00-01-XX 中的 XX, 所以范围为 0 到 255, 见 https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol
          priority 100    #选举 master 时,谁优先级高,谁就当 master(数字越大,优先级越高)
          advert_int 1    # master 和 slave确定后, master 隔 advert_int 秒发送心跳信息
          authentication {
              auth_type PASS
              auth_pass 1234
          }
          virtual_ipaddress {
              192.168.175.100
          }
      }


// 修改 haproxy 配置 (将 virtual service 绑定到 vip)
[root@haproxy01 ~]# vim /etc/haproxy/haproxy.cfg

      # 注: 由于配置实在太多, 这里仅支持需要注意的地方
      #     将 virtual service 绑定到 vip,
      listen admin_status
          bind 192.168.175.100:9088  # 注: 这种方式需要启用 net.ipv4.ip_nonlocal_bind, 否则应使用类似 *:9088 或 0.0.0.0:9088 这种绑定方式
      #略 略 略 略 略

      frontend web_service
        bind 192.168.175.100:80 # 注: 这种方式需要启用 net.ipv4.ip_nonlocal_bind, 否则应使用类似 *:80 或 0.0.0.0:80 这种绑定方式
      #略 略 略 略 略


[root@haproxy01 ~]# systemctl restart haproxy




----------------------------------------------------------------------------------------------------
配置 haproxy02  (keepalived 与 haproxy 结合)

// 启用非本地 ip 绑定功能(即允许当 vip 还不存在时 仍可将服务绑定到该 ip 上)
// 注: 如不想配置 net.ipv4.ip_nonlocal_bind, 则 haproxy 在 bind 时执行类似 *:80 或 0.0.0.0:80 的bind 即可.
[root@haproxy02 ~]# vim /etc/sysctl.conf

    net.ipv4.ip_nonlocal_bind = 1

[root@haproxy02 ~]# sysctl -p
    net.ipv4.ip_nonlocal_bind = 1

[root@haproxy02 ~]# sysctl net.ipv4.ip_nonlocal_bind
    net.ipv4.ip_nonlocal_bind = 1


// 安装 keepalived
[root@haproxy02 ~]# yum -y install keepalived



// keepalived 的文档:
//      https://keepalived.org/doc/
// keepalived 的 官网:
//      https://www.keepalived.org/
//  `man keepalived.conf`  其中 man page 包含了最详细的参数解释
//   在线man page 见 https://www.systutorials.com/docs/linux/man/5-keepalived.conf/
// 注: keepalived.conf 的 单行注释以 符号 '#' or '!' 开始
[root@haproxy02 ~]# rsync -av root@192.168.175.101:/etc/keepalived/keepalived.conf  /etc/keepalived/keepalived.conf
[root@haproxy02 ~]# vim /etc/keepalived/keepalived.conf

      ! Configuration File for keepalived

      global_defs {
         router_id haproxy02
      }

      #注: vrrp_instance 定义用于将 director(调度器) 加到虚拟组中,以实现互为备份
      vrrp_instance web_service_group {
          state BACKUP
          interface ens33
          virtual_router_id 55   #作为 00-00-5E-00-01-XX 中的 XX, 所以范围为 0 到 255, 见 https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol
          priority 80    #选举 master 时,谁优先级高,谁就当 master(数字越大,优先级越高)
          advert_int 1    # master 和 slave确定后, master 隔 advert_int 秒发送心跳信息
          authentication {
              auth_type PASS
              auth_pass 1234
          }
          virtual_ipaddress {
              192.168.175.100
          }
      }


// 修改 haproxy 配置 (将 virtual service 绑定到 vip)
[root@haproxy02 ~]# vim /etc/haproxy/haproxy.cfg

      # 注: 由于配置实在太多, 这里仅支持需要注意的地方
      #     将 virtual service 绑定到 vip,
      listen admin_status
          bind 192.168.175.100:9088  # 注: 这种方式需要启用 net.ipv4.ip_nonlocal_bind, 否则应使用类似 *:9088 或 0.0.0.0:9088 这种绑定方式
      #略 略 略 略 略

      frontend web_service
        bind 192.168.175.100:80 # 注: 这种方式需要启用 net.ipv4.ip_nonlocal_bind, 否则应使用类似 *:80 或 0.0.0.0:80 这种绑定方式
      #略 略 略 略 略


[root@haproxy02 ~]# systemctl restart haproxy

----------------------------------------------------------------------------------------------------

[root@haproxy01 ~]# systemctl start keepalived
[root@haproxy01 ~]# systemctl enable keepalived

[root@haproxy02 ~]# systemctl start keepalived
[root@haproxy02 ~]# systemctl enable keepalived


[root@haproxy01 ~]# ip addr show ens33
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:f6:f0:83 brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.101/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet 192.168.175.100/32 scope global ens33   <---- 观察
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fef6:f083/64 scope link
           valid_lft forever preferred_lft forever


[root@haproxy02 ~]# ip addr show ens33
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:82:ac:0f brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.102/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe82:ac0f/64 scope link
           valid_lft forever preferred_lft forever


[root@haproxy01 ~]# netstat -anptu | grep haproxy
    tcp        0      0 192.168.175.100:80      0.0.0.0:*               LISTEN      17455/haproxy
    tcp        0      0 192.168.175.100:9088    0.0.0.0:*               LISTEN      17455/haproxy


[root@haproxy02 ~]# netstat -anptu | grep haproxy
    tcp        0      0 192.168.175.100:80      0.0.0.0:*               LISTEN      16902/haproxy
    tcp        0      0 192.168.175.100:9088    0.0.0.0:*               LISTEN      16902/haproxy


// 在 client测试  VIP 上绑定的 virtual service (此时 master 为 haproxy01)
[root@client ~]# cat /etc/hosts

    192.168.175.100 bbs.linux.com
    192.168.175.100 blog.linux.com

// 可以 监视 haproxy 日志, 用于观察后续测试
[root@haproxy01 ~]# tail -f /var/log/haproxy.log
[root@haproxy02 ~]# tail -f /var/log/haproxy.log


[root@client ~]# for i in {1..4}; do curl bbs.linux.com; done
    bbs01
    bbs02
    bbs01
    bbs02

[root@client ~]# for i in {1..4}; do curl blog.linux.com; done
    blog01
    blog02
    blog01
    blog02


// 测试故障转移(failover)
[root@haproxy01 ~]# systemctl stop keepalived

[root@haproxy01 ~]# ip addr show ens33
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 00:0c:29:f6:f0:83 brd ff:ff:ff:ff:ff:ff
    inet 192.168.175.101/24 brd 192.168.175.255 scope global ens33
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fef6:f083/64 scope link
       valid_lft forever preferred_lft forever

[root@haproxy02 ~]# ip addr show ens33
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:82:ac:0f brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.102/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever
        inet 192.168.175.100/32 scope global ens33  <----观察
           valid_lft forever preferred_lft forever
        inet6 fe80::20c:29ff:fe82:ac0f/64 scope link
           valid_lft forever preferred_lft forever


// 可以 监视 haproxy 日志, 用于观察后续测试
[root@haproxy01 ~]# tail -f /var/log/haproxy.log
[root@haproxy02 ~]# tail -f /var/log/haproxy.log




[root@client ~]# for i in {1..4}; do curl bbs.linux.com; done
    bbs01
    bbs02
    bbs01
    bbs02

[root@client ~]# for i in {1..4}; do curl blog.linux.com; done
    blog01
    blog02
    blog01
    blog02



----------------------------------------------------------------------------------------------------

访问统计报告页面:

    http://192.168.175.100:9088/haproxy-status


更多信息见 http://cbonte.github.io/haproxy-dconv/configuration-1.5.html#9




----------------------------------------------------------------------------------------------------
注:

  如果修改 /etc/haproxy/haproxy.cfg 时 没有修改端口, 可以尝试使用:
    systemctl reload haproxy




