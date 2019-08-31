

                                  (vip: 192.168.175.100)
                       +----------------------------------------------+
                       |                                              |
                       |  nginx01                nginx02              |
                       |  ip: 192.168.175.101    ip: 192.168.175.102  |
                       |                                              |
                       +--------------------|-------------------------+
                                            |
                                            |
                            |---------------|---------------|
                            |                               |
                            |                               |
                            |                               |
                            |                               |
                       +----|-----------------+    +--------|-------------+
                       |  web01               |    | web02                |
                       |  ip: 192.168.175.121 |    | ip: 192.168.175.122  |
                       +----------------------+    +----------------------+


----------------------------------------------------------------------------------------------------
准备环境, 做好时间同步 等初始化步骤

----------------------------------------------------------------------------------------------------
准备 web01 和 web02 后端 服务器

// 准备 web01
[root@web01 ~]# yum -y install httpd
[root@web01 ~]# echo 'web01' > /var/www/html/index.html

[root@web01 ~]# vim /etc/httpd/conf/httpd.conf
    LogFormat "%{X-Real-IP}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

[root@web01 ~]# systemctl start httpd
[root@web01 ~]# systemctl enable httpd



// 准备web02
[root@web02 ~]# yum -y install httpd
[root@web02 ~]# echo 'web02' > /var/www/html/index.html

[root@web02 ~]# vim /etc/httpd/conf/httpd.conf
    LogFormat "%{X-Real-IP}i %l %u %t \"%r\" %>s %b \"%{Referer}i\" \"%{User-Agent}i\"" combined

[root@web02 ~]# systemctl start httpd
[root@web02 ~]# systemctl enable httpd

// 在 nginx 代理上测试
[root@nginx01 ~]# for i in 121 122; do curl 192.168.175.$i; done
    web01
    web02

[root@nginx02 ~]# for i in 121 122; do curl 192.168.175.$i; done
    web01
    web02


----------------------------------------------------------------------------------------------------
准备 nginx01 和 nginx02 作为代理服务器

    参考笔记:
    https://github.com/yangsg/linux_training_notes/blob/master/nginx/nginx02_server_basic/nginx7server/app/nginx/sites-available/proxy.upstream.demo01.com.conf

[root@nginx01 ~]# yum -y install nginx

// 配置nginx01
[root@nginx01 ~]# vim /etc/nginx/nginx.conf

        upstream WebServer {
            server 192.168.175.121 weight=1 max_fails=2 fail_timeout=5s;
            server 192.168.175.122 weight=1 max_fails=2 fail_timeout=5s;
        }

        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_pass http://WebServer;
        }


[root@nginx01 ~]# systemctl start nginx
[root@nginx01 ~]# systemctl enable nginx


// 配置nginx01
[root@nginx02 ~]# yum -y install nginx
[root@nginx02 ~]# rsync -av root@192.168.175.101:/etc/nginx/nginx.conf /etc/nginx/nginx.conf

[root@nginx02 ~]# systemctl start nginx
[root@nginx02 ~]# systemctl enable nginx



// 测试:
[root@nginx01 ~]# for i in 1 2; do curl 192.168.175.101; done
    web01
    web02

[root@nginx02 ~]# for i in 1 2; do curl 192.168.175.101; done
    web01
    web02




----------------------------------------------------------------------------------------------------
nginx 结合 keepalived 做高可用

    参考笔记:
        https://github.com/yangsg/linux_training_notes/tree/master/cluster-haproxy/101-keepalived-haproxy-web-http-7-layer-scheduling-demo01

    网上资料:
        https://docs.nginx.com/nginx/admin-guide/high-availability/ha-keepalived-nodes/

[root@nginx01 ~]# yum -y install keepalived
[root@nginx01 ~]# rpm -q keepalived
    keepalived-1.3.5-8.el7_6.5.x86_64

[root@nginx01 ~]# vim /etc/keepalived/keepalived.conf

      ! Configuration File for keepalived

      global_defs {
         router_id nginx01
      }

      #注: vrrp_instance 定义用于将 director(调度器) 加到虚拟组中,以实现互为备份
      vrrp_instance web_server_group {
          state MASTER
          interface ens33
          virtual_router_id 55   #作为 00-00-5E-00-01-XX 中的 XX, 所以范围为 0 到 255, 见 https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol
          priority 100           #选举 master 时,谁优先级高,谁就当 master(数字越大,优先级越高)
          advert_int 1           #master 和 slave确定后, master 隔 advert_int 秒发送心跳信息
          authentication {
              auth_type PASS
              auth_pass 1234
          }
          virtual_ipaddress {
              192.168.175.100
          }
      }





[root@nginx02 ~]# yum -y install keepalived
[root@nginx02 ~]# rsync -av root@192.168.175.101:/etc/keepalived/keepalived.conf /etc/keepalived/keepalived.conf

[root@nginx02 ~]# vim /etc/keepalived/keepalived.conf

      ! Configuration File for keepalived

      global_defs {
         router_id nginx02
      }

      #注: vrrp_instance 定义用于将 director(调度器) 加到虚拟组中,以实现互为备份
      vrrp_instance web_server_group {
          state BACKUP
          interface ens33
          virtual_router_id 55   #作为 00-00-5E-00-01-XX 中的 XX, 所以范围为 0 到 255, 见 https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol
          priority 80           #选举 master 时,谁优先级高,谁就当 master(数字越大,优先级越高)
          advert_int 1           #master 和 slave确定后, master 隔 advert_int 秒发送心跳信息
          authentication {
              auth_type PASS
              auth_pass 1234
          }
          virtual_ipaddress {
              192.168.175.100
          }
      }


// 实时观察日志:
[root@nginx01 ~]# tail -f  /var/log/messages
[root@nginx02 ~]# tail -f /var/log/messages


[root@nginx01 ~]# systemctl start keepalived
[root@nginx02 ~]# systemctl start keepalived

[root@nginx01 ~]# systemctl enable keepalived
[root@nginx02 ~]# systemctl enable keepalived



// 观察 nginx01 上实时日志的内容:

        即在 [root@nginx01 ~]# tail -f  /var/log/messages 后 被捕获的内容

      Aug 31 10:33:27 nginx01 systemd: Starting LVS and VRRP High Availability Monitor...
      Aug 31 10:33:27 nginx01 Keepalived[17234]: Starting Keepalived v1.3.5 (03/19,2017), git commit v1.3.5-6-g6fa32f2
      Aug 31 10:33:27 nginx01 Keepalived[17234]: Opening file '/etc/keepalived/keepalived.conf'.
      Aug 31 10:33:27 nginx01 systemd: PID file /var/run/keepalived.pid not readable (yet?) after start.
      Aug 31 10:33:27 nginx01 Keepalived[17235]: Starting Healthcheck child process, pid=17236
      Aug 31 10:33:27 nginx01 Keepalived[17235]: Starting VRRP child process, pid=17237
      Aug 31 10:33:27 nginx01 systemd: Started LVS and VRRP High Availability Monitor.
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: Registering Kernel netlink reflector
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: Registering Kernel netlink command channel
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: Registering gratuitous ARP shared channel
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: Opening file '/etc/keepalived/keepalived.conf'.
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: VRRP_Instance(web_server_group) removing protocol VIPs.
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: Using LinkWatch kernel netlink reflector...
      Aug 31 10:33:27 nginx01 Keepalived_vrrp[17237]: VRRP sockpool: [ifindex(2), proto(112), unicast(0), fd(10,11)]
      Aug 31 10:33:27 nginx01 kernel: nf_conntrack version 0.5.0 (7810 buckets, 31240 max)
      Aug 31 10:33:27 nginx01 kernel: IPVS: Registered protocols (TCP, UDP, SCTP, AH, ESP)
      Aug 31 10:33:27 nginx01 kernel: IPVS: Connection hash table configured (size=4096, memory=64Kbytes)
      Aug 31 10:33:27 nginx01 kernel: IPVS: Creating netns size=2040 id=0
      Aug 31 10:33:27 nginx01 kernel: IPVS: ipvs loaded.
      Aug 31 10:33:27 nginx01 Keepalived_healthcheckers[17236]: Opening file '/etc/keepalived/keepalived.conf'.
      Aug 31 10:33:28 nginx01 Keepalived_vrrp[17237]: VRRP_Instance(web_server_group) Transition to MASTER STATE
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: VRRP_Instance(web_server_group) Entering MASTER STATE
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: VRRP_Instance(web_server_group) setting protocol VIPs.
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: VRRP_Instance(web_server_group) Sending/queueing gratuitous ARPs on ens33 for 192.168.175.100
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:29 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:34 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:34 nginx01 Keepalived_vrrp[17237]: VRRP_Instance(web_server_group) Sending/queueing gratuitous ARPs on ens33 for 192.168.175.100
      Aug 31 10:33:34 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:34 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:34 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100
      Aug 31 10:33:34 nginx01 Keepalived_vrrp[17237]: Sending gratuitous ARP on ens33 for 192.168.175.100


// 观察 nginx02 上实时日志的内容:

        即在 [root@nginx02 ~]# tail -f  /var/log/messages 后 被捕获的内容

      Aug 31 10:34:05 localhost systemd: Starting LVS and VRRP High Availability Monitor...
      Aug 31 10:34:05 localhost Keepalived[1678]: Starting Keepalived v1.3.5 (03/19,2017), git commit v1.3.5-6-g6fa32f2
      Aug 31 10:34:05 localhost Keepalived[1678]: Opening file '/etc/keepalived/keepalived.conf'.
      Aug 31 10:34:05 localhost systemd: PID file /var/run/keepalived.pid not readable (yet?) after start.
      Aug 31 10:34:05 localhost Keepalived[1679]: Starting Healthcheck child process, pid=1680
      Aug 31 10:34:05 localhost Keepalived[1679]: Starting VRRP child process, pid=1681
      Aug 31 10:34:05 localhost systemd: Started LVS and VRRP High Availability Monitor.
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: Registering Kernel netlink reflector
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: Registering Kernel netlink command channel
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: Registering gratuitous ARP shared channel
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: Opening file '/etc/keepalived/keepalived.conf'.
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: VRRP_Instance(web_server_group) removing protocol VIPs.
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: Using LinkWatch kernel netlink reflector...
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: VRRP_Instance(web_server_group) Entering BACKUP STATE
      Aug 31 10:34:05 localhost Keepalived_vrrp[1681]: VRRP sockpool: [ifindex(2), proto(112), unicast(0), fd(10,11)]
      Aug 31 10:34:05 localhost kernel: nf_conntrack version 0.5.0 (7810 buckets, 31240 max)
      Aug 31 10:34:05 localhost kernel: IPVS: Registered protocols (TCP, UDP, SCTP, AH, ESP)
      Aug 31 10:34:05 localhost kernel: IPVS: Connection hash table configured (size=4096, memory=64Kbytes)
      Aug 31 10:34:05 localhost kernel: IPVS: Creating netns size=2040 id=0
      Aug 31 10:34:05 localhost kernel: IPVS: ipvs loaded.
      Aug 31 10:34:05 localhost Keepalived_healthcheckers[1680]: Opening file '/etc/keepalived/keepalived.conf'.


// 尝试抓包观察 vrrp 协议数据包
[root@nginx01 ~]# yum -y install tcpdump
[root@nginx02 ~]# yum -y install tcpdump

    tcpdump 使用笔记见:
        https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/01-full/150-tcpdump.txt
    vrrp 协议见:
        https://github.com/yangsg/linux_training_notes/tree/master/cluster-lvs


// nginx01 上 抓包观察, master 周期性的 组播 心跳信息(组播ip: 224.0.0.18, vrid 55, 即00-00-5E-00-01-XX 中的 XX, proto VRRP (112) 即 ip protocol number: 112)
[root@nginx01 ~]# tcpdump -i ens33 -nn -vvv vrrp
      tcpdump: listening on ens33, link-type EN10MB (Ethernet), capture size 262144 bytes
      10:53:30.289929 IP (tos 0xc0, ttl 255, id 1201, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 224.0.0.18: vrrp 192.168.175.101 > 224.0.0.18: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"
      10:53:31.291562 IP (tos 0xc0, ttl 255, id 1202, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 224.0.0.18: vrrp 192.168.175.101 > 224.0.0.18: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"


// nginx02 上抓包观察
[root@nginx02 ~]# tcpdump -i ens33 -nn -vvv vrrp
      tcpdump: listening on ens33, link-type EN10MB (Ethernet), capture size 262144 bytes
      10:53:21.266885 IP (tos 0xc0, ttl 255, id 1192, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 224.0.0.18: vrrp 192.168.175.101 > 224.0.0.18: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"
      10:53:22.269041 IP (tos 0xc0, ttl 255, id 1193, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 224.0.0.18: vrrp 192.168.175.101 > 224.0.0.18: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"



----------------------------------------------------------------------------------------------------
让 keepalived 采用单播 unicast 发送心跳通知

      因为某些云平台底层网络禁止 组播, 现采用 unicast 单播的方式 让 master 发送心跳信息

[root@nginx01 ~]# vim /etc/keepalived/keepalived.conf

        #因某些云平台底层网络禁止了组播, 所以这里改为 单播方式 通知心跳信息
        #参考:
        #  https://docs.nginx.com/nginx/admin-guide/high-availability/ha-keepalived-nodes/
        unicast_src_ip    192.168.175.101

        unicast_peer {
            192.168.175.102
        }

[root@nginx02 ~]# vim /etc/keepalived/keepalived.conf

    #因某些云平台底层网络禁止了组播, 所以这里改为 单播方式 通知心跳信息
    #参考:
    #  https://docs.nginx.com/nginx/admin-guide/high-availability/ha-keepalived-nodes/
    unicast_src_ip    192.168.175.102

    unicast_peer {
        192.168.175.101
    }



[root@nginx01 ~]# systemctl restart keepalived
[root@nginx02 ~]# systemctl restart keepalived


// 在 nginx01 上 抓包 观察 改为单播方式后 心跳通知的 数据包
[root@nginx01 ~]# tcpdump -i ens33 -nn -vvv vrrp
      tcpdump: listening on ens33, link-type EN10MB (Ethernet), capture size 262144 bytes
      11:22:15.339163 IP (tos 0xc0, ttl 255, id 195, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 192.168.175.102: vrrp 192.168.175.101 > 192.168.175.102: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"
          11:22:16.340473 IP (tos 0xc0, ttl 255, id 196, offset 0, flags [none], proto VRRP (112), length 40)
              192.168.175.101 > 192.168.175.102: vrrp 192.168.175.101 > 192.168.175.102: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"


// 在 nginx02 上 抓包 观察 改为单播方式后 心跳通知的 数据包
[root@nginx02 ~]# tcpdump -i ens33 -nn -vvv vrrp
      tcpdump: listening on ens33, link-type EN10MB (Ethernet), capture size 262144 bytes
      11:22:18.336459 IP (tos 0xc0, ttl 255, id 198, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 192.168.175.102: vrrp 192.168.175.101 > 192.168.175.102: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"
      11:22:19.337662 IP (tos 0xc0, ttl 255, id 199, offset 0, flags [none], proto VRRP (112), length 40)
          192.168.175.101 > 192.168.175.102: vrrp 192.168.175.101 > 192.168.175.102: VRRPv2, Advertisement, vrid 55, prio 100, authtype simple, intvl 1s, length 20, addrs: 192.168.175.100 auth "1234^@^@^@^@"




----------------------------------------------------------------------------------------------------
















