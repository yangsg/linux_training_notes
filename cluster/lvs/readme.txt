

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
DR 模式: 直接路由模式

    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-direct-vsa#sect-lvs-Direct_Routing_Using_firewalld
    http://kb.linuxvirtualserver.org/wiki/Using_arp_announce/arp_ignore_to_disable_ARP








----------------------------------------------------------------------------------------------------




