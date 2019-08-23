

http://www.linuxvirtualserver.org/
http://www.linuxvirtualserver.org/whatis.html

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/index

LVS: Linux Virtual Server



VRRP 协议:
https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol


lvs 调度算法: (Keepalived Scheduling Algorithms)
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-scheduling-vsa

      rr: Round-Robin Scheduling
      wrr: Weighted Round-Robin Scheduling
      lc: Least-Connection
      wlc: Weighted Least-Connections  (lvs 的默认(default)调度算法)
      sh: Source Hash Scheduling      (适用于会话保持) 注: 针对于共享的 session 存储, rr 等其他简单的调度算法也是 可行的
      dh: Destination Hash Scheduling (适用于cache server)

      其他:
          Locality-Based Least-Connection Scheduling
          Locality-Based Least-Connection Scheduling with Replication Scheduling
          Shortest Expected Delay
          Never Queue




lvs 路由方式(即 工作模式):
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-routing-vsa

CIP: Client IP
RIP: Real IP
DIP: Director IP (与 后端 real server 交互的IP)
VIP: Virtual IP  (对外提供服务的 IP)


NAT 模式: NAT Routing  (后端 server 的数量不要过多, 10-20个, VIP和DIP要 分属于两个不同的网络)
DR 模式: Direct Routing 直接路由
TUN 模式

----------------------------------------------------------------------------------------------------
NAT 模式:

           client ---| ↑
                     | |
                     | |
                     ↓ |  VIP
 (借助lvs的nat功能) director
                     | ↑  DIP
                     | |
                     | |
                     ↓ |
              -------|-|------------------------|
              | ↑            | ↑              | ↑
              | |            | |              | |
              | |            | |              | |
              | |            | |              | |
              ↓ |            ↓ |              ↓ |
        real server01    real server02     real server03
           RIP             RIP                RIP



↓ ↑

----------------------------------------------------------------------------------------------------
DR 模式: 直接路由模式, 顾名思义, real server 响应时直接返回给 client, 不再经过 director.

                           client <----------------------------------------------------
                             |                                                        ↑
                             |                                                        |
                             |                                                        |
                             |                                                        |
                             ↓                                                        |
 router仅知道vip在director上 router --------→|                                        |
                             ↓ ↑             |                                        |
                             | |             |                                        |
                             | |             |                                        |
                             | |             |                                        |
                             | |             |                                        |
                             | |             |                                        |
                             | |             |                                        |
                             ↓ ↑ VIP         |                                        |
  (director修改目的 mac)    director         |                                        |
                                 DIP         |                                        |
                                             |                                        |
                                             |                                        |
                                             ↓                                        |
                      -----------------------|----------|                             |
                      |              |                  |                             |
                      |              |                  |                             |
                      |              |                  |                             |
                      |              |                  |                             |
                      ↓              ↓                  ↓                             |
                real server01    real server02     real server03                      |
                   RIP             RIP                RIP                             |
                   VIP(hidden)     VIP(hidden)        VIP(hidden)                     |
                      ↓              ↓                  ↓                             |
                      ↓              ↓                  ↓                             |
                      ---------------------------------------------------------------→|





    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-direct-vsa#sect-lvs-Direct_Routing_Using_firewalld
    http://kb.linuxvirtualserver.org/wiki/Using_arp_announce/arp_ignore_to_disable_ARP

              arp_announce - INTEGER

                2 - Always use the best local address for this target.
                In this mode we ignore the source address in the IP packet
                and try to select local address that we prefer for talks with
                the target host. Such local address is selected by looking
                for primary IP addresses on all our subnets on the outgoing
                interface that include the target IP address. If no suitable
                local address is found we select the first local address
                we have on the outgoing interface or on all other interfaces,
                with the hope we will receive reply for our request and
                even sometimes no matter the source IP address we announce.

                The max value from conf/{all,interface}/arp_announce is used.


              arp_ignore - INTEGER
                1 - reply only if the target IP address is local address
                configured on the incoming interface

                The max value from conf/{all,interface}/arp_ignore is used
                when ARP request is received on the {interface}


              在 real server 上配置 arp_ignore 为 1 可以仅让 物理网卡上的 RIP 相应 同网段的 arp 请求.
              在 real server 上配置 arp_announce 为 2 则使其在通告(如 real server 发出 arp 广播请求)时
              不会告诉 router 或 其他主机 自己身上存在 vip,
              所以最后 DR 模式中 最终效果就是 router 仅知道 director 上存在 vip 和 dip,
              以及 real server 上存在 rip (而 real server 上的 vip 对于 router 来说是私有的或隐藏的),
              而当 router 收到 vip 上的 虚拟服务(virtual service) 的 数据包时, router 就会将 数据包
              转发给 director(因为 router 知道 director 拥有 vip), 然后 director 接受到数据包之后
              根据 调度算法 将 数据包中的 目的 mac address 修改为 其中一个 real server 的 rip 对应的 mac address.
              再将 修改了 目的 mac address 后的 数据包 发给 router, 再由 router 发送给 mac address 对应 real server.
              real server 检查到 数据包 的目的 ip 就是 自己(私有的或隐藏起来的) 的 vip 时, 于是并不会 将其丢弃,
              而是直接通过 gateway 向 client 发送其生成的响应(reply).





----------------------------------------------------------------------------------------------------




