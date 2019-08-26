

http://www.linuxvirtualserver.org/
http://www.linuxvirtualserver.org/whatis.html
http://www.linuxvirtualserver.org/zh/index.html

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/index

LVS: Linux Virtual Server


---------------------------------------------------------------------------------------------------
VRRP 协议:
    https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol
    http://www2.elo.utfsm.cl/~tel242/exp/04/VRRP_protocol.pdf

    内容来自wiki:

          The Virtual Router Redundancy Protocol (VRRP) is a computer networking protocol that provides
          for automatic assignment of available Internet Protocol (IP) routers to participating hosts.
          This increases the availability and reliability of routing paths via
          automatic default gateway selections on an IP subnetwork.

          The protocol achieves this by creation of virtual routers, which are an abstract
          representation of multiple routers, i.e. master and backup routers, acting as a group.
          The default gateway of a participating host is assigned to the virtual router
          instead of a physical router. If the physical router that is routing packets
          on behalf of the virtual router fails, another physical router is selected
          to automatically replace it. The physical router that is forwarding packets
          at any given time is called the master router.

          VRRP provides information on the state of a router, not the routes
          processed and exchanged by that router. Each VRRP instance is limited,
          in scope, to a single subnet. It does not advertise IP routes beyond
          that subnet or affect the routing table in any way. VRRP can be used in Ethernet,
          MPLS and token ring networks with Internet Protocol Version 4 (IPv4), as well as IPv6.


          Implementation (VRRP 实现)

            A virtual router must use 00-00-5E-00-01-XX as its Media Access Control (MAC) address.
            The last byte of the address (XX) is the Virtual Router IDentifier (VRID),
            which is different for each virtual router in the network. This address
            is used by only one physical router at a time, and it will reply with
            this MAC address when an ARP request is sent for the virtual router's IP address.

            Physical routers within the virtual router must communicate within themselves
            using packets with multicast IP address 224.0.0.18 and IP protocol number 112.

            Routers have a priority of between 1 and 254 and the router with the highest priority
            will become the master. The default priority is 100; for MAC address owner the priority is always 255.

          Elections of master routers(主路由选举)
            A failure to receive a multicast packet from the master router for a period longer than three times
            the advertisement timer causes the backup routers to assume that the master router is dead.
            The virtual router then transitions into an unsteady state and an election process
            is initiated to select the next master router from the backup routers.
            This is fulfilled through the use of multicast packets.


            Backup router(s) are only supposed to send multicast packets during an election process.
            One exception to this rule is when a physical router is configured with a higher priority
            than the current master, which means that on connection to the network it will preempt the master status.
            This allows a system administrator to force a physical router to the master state immediately after booting,
            for example when that particular router is more powerful than others within the virtual router.
            The backup router with the highest priority becomes the master router by raising
            its priority above that of the current master. It will then take responsibility for
            routing packets sent to the virtual gateway's MAC address. In cases where backup routers
            all have the same priority, the backup router with the highest IP address becomes the master router.


            All physical routers acting as a virtual router must be in the same local area network (LAN) segment.
            Communication within the virtual router takes place periodically. This period can be adjusted
            by changing advertisement interval timers. The shorter the advertisement interval,
            the shorter the black hole period, though at the expense of more traffic in the network.
            Security is achieved by responding only to first hop packets, though other mechanisms
            are provided to reinforce this, particularly against local attacks. Election process
            is made orderly through the use of skew time, derived from a router's priority and
            used to reduce the chance of the thundering herd problem occurring during election.
            The skew time is given by the formula (256 − Priority)/256 (expressed in milliseconds).

            Backup router utilization can be improved by load sharing. For more on this, see RFC 5798.


            --------------------------
            https://en.wikipedia.org/wiki/Thundering_herd_problem
            Thundering herd problem


---------------------------------------------------------------------------------------------------

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


            http://www.linuxvirtualserver.org/zh/lvs3.html
            6.三种方法的优缺点比较

            三种IP负载均衡技术的优缺点归纳在下表中：
                |-----------------|------------------|------------------|--------------------|
                |_                | VS/NAT           |     VS/TUN       |     VS/DR          |
                |-----------------|------------------|------------------|--------------------|
                |Server           | any              |     Tunneling    |     Non-arp device |
                |-----------------|------------------|------------------|--------------------|
                |server network   | private          |     LAN/WAN      |     LAN            |
                |-----------------|------------------|------------------|--------------------|
                |server number    | low (10~20)      |     High (100)   |     High (100)     |
                |-----------------|------------------|------------------|--------------------|
                |server gateway   | load balancer    |     own router   |     Own router     |
                |-----------------|------------------|------------------|--------------------|

            注： 以上三种方法所能支持最大服务器数目的估计是假设调度器使用100M网卡，
                 调度器的硬件配置与后端服务器的硬件配置相同，而且是对一般Web服务。
                 使用更 高的硬件配置（如千兆网卡和更快的处理器）作为调度器，
                 调度器所能调度的服务器数量会相应增加。当应用不同时，
                 服务器的数目也会相应地改变。所以，以上数 据估计主要是为三种方法的伸缩性进行量化比较。



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

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-lvs-overview-vsa#s1-lvs-keepalived-VSA
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-keepalived-overview-vsa
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/keepalived_install_example1


keepalived















