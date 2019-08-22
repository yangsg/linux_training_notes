

http://www.linuxvirtualserver.org/
http://www.linuxvirtualserver.org/whatis.html

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/index



VRRP 协议:
https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol


lvs 调度算法: (Keepalived Scheduling Algorithms)
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-scheduling-vsa

      rr: Round-Robin Scheduling
      wrr: Weighted Round-Robin Scheduling
      lc: Least-Connection
      wlc: Weighted Least-Connections
      sh: Source Hash Scheduling      (适用于会话保持) 注: 针对于共享的 session 存储, rr 等其他简单的调度算法也是 可行的
      dh: Destination Hash Scheduling (适用于cache server)

      其他:
          Locality-Based Least-Connection Scheduling
          Locality-Based Least-Connection Scheduling with Replication Scheduling
          Shortest Expected Delay
          Never Queue




lvs 路由方式:
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-routing-vsa


























