

https://github.com/haproxy/haproxy
https://www.haproxy.org/


haproxy官方文档:
    https://cbonte.github.io/haproxy-dconv/

keepalived 官方文档:
    https://keepalived.org/doc/   <--- 文档应该参考这里
    https://www.keepalived.org/   <--- 官网, 不过 document 已经 被 deprecated 了


  man keepalived.conf  <----较详细的配置解释
      https://www.systutorials.com/docs/linux/man/5-keepalived.conf/


关于负载均衡:
      The Load Balancer is a set of integrated software components that provide for balancing
      IP traffic across a set of real servers. It consists of two main technologies
      to monitor cluster members and cluster services: Keepalived and HAProxy.
      Keepalived uses Linux virtual server (LVS) to perform load balancing
      and failover tasks on the active and passive routers,
      while HAProxy performs load balancing and high-availability services to TCP and HTTP applications.


haproxy 可以执行 tcp(4层)调度 或 http(7层) 调度, haproxy 还支持 会话保持功能
lvs 属于 4层 调度, 没有 socket 的概念, 不受 socket 数量的限制
nginx 属于 7 层调度

----------------------------------------------------------------------------------------------------------------------------------
keepalived 的工作方式:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-lvs-overview-vsa
        https://en.wikipedia.org/wiki/Virtual_Router_Redundancy_Protocol


    (vrrp_instance)

  |--------virtual router(provide virtual service on VIP)--(mac:00-00-5E-00-01-XX, XX is the Virtual Router IDentifier (VRID) )--|
  |                     ^                                                                                                        |
  |                     |                                                                                                        |
  |                     | keepalived starts LVS Service and and monitors the health of the services                              |
  |                     |                                                                                                        |
  |                     |                                                                                                        |
  |               +--------------+                                     +---------------+                                         |
  |               |   keepalived |                                     |  keepalived   |                                         |
  |               |--------------|       VRRP                          |---------------|                                         |
  |               |active router |  ---------------------------------> |passive router |                                         |
  |               +--------------+    advert at periodic intervals     +---------------+                                         |
  |                                  (if receive: ok, else if not receive: fail, then elect master and advert)                   |
  |                                                                                                                              |
  |  On startup, all routers will join a multicast group.                                                                        |
  |                                                                                                                              |
  |  Physical routers within the virtual router must communicate within themselves                                               |
  |  using packets with multicast IP address 224.0.0.18 and IP protocol number 112                                               |
  |                                                                                                                              |
  |                                                                                                                              |
  |                                                                                                                              |
  |------------------------------------------------------------------------------------------------------------------------------|
                         |
                         |
                         | load balance
                         |
                         |   The active router also dynamically monitors the overall health of the specific services
                         |   on the real servers through three built-in health checks: simple TCP connect, HTTP, and HTTPS.
                         |   For TCP connect, the active router will periodically check that it can connect to the
                         |   real servers on a certain port. For HTTP and HTTPS, the active router
                         |   will periodically fetch a URL on the real servers and verify its content.
                         |
                         |
  |---------------------server pool---------------------------------|
  |                            |                                    |
  |                            |                                    |
  |           +----------------+----------------+                   |
  |           |                |                |                   |
  |           |                |                |                   |
  |      real server01    real server02    real server              |
  |                                                                 |
  |                                                                 |
  |                                                                 |
  |                                                                 |
  |-----------------------------------------------------------------|

      Keepalived performs failover on layer 4, or the Transport layer, upon which TCP conducts
      connection-based data transmissions. When a real server fails to reply to
      simple timeout TCP connection, keepalived detects that the server
      has failed and removes it from the server pool.


    双层配置: (适用于 static web pages)
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-keepalived-overview-vsa
    三层配置: (three-tier Keepalived Load Balancer)
      LVS router  ----->  real servers ------> shared data source
            This topology is also recommended for websites that access a central, highly available database for transactions
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-cm-vsa
    keepalived 的调度算法：
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-scheduling-vsa
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-initial-setup-vsa
    keepalived 的路由方式:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-routing-vsa

            A virtual server is a service configured to listen on a specific virtual IP
            A VIP is also known as a floating IP addresses.
    网络(ip和防火墙)配置:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-connect-vsa
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-fwm-sav-vsa


    多端口services(with fwmark and persistence):
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-multi-vsa
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-persistance-vsa#s2-lve-fwmarks-VSA

      ftp:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-ftp-vsa

        使用 virtual service 处理 ftp 服务时, 如果 是使用 dr 或 tun 模式, 则 必须设置 persistent.
        如果使用 nat 模式, 则 persistent 不是必须的, 但此时必须使用 ip_vs_ftp kernel module.
        见:
            https://github.com/yangsg/linux_training_notes/tree/master/cluster-lvs/101-lvs-direct-routing-demo01

    使用 keepalived (即 lvs)做负载均衡时的 条件:
          https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-lvs-setup-prereqs-vsa


    keepalived 负载均衡的初始配置:
          https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-initial-setup-vsa
          https://www.cnblogs.com/along1226/p/5027838.html

            vrrp_sync_group

    Note:
      Accessing the virtual IP from the load balancers or one of the real servers
      is not supported. Likewise, configuring a load balancer
      on the same machines as a real server is not supported.






----------------------------------------------------------------------------------------------------------------------------------
haproxy

    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-lvs-haproxy-vsa


      HAProxy offers load balanced services to HTTP and TCP-based services,
      such as Internet-connected services and web-based applications.

    haproxy 自身的 调度算法:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-haproxy-setup-vsa


----------------------------------------------------------------------------------------------------------------------------------
keepalived and haproxy  (keepalived 结合 haproxy)

  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s2-lvs-keepalived-haproxy-vsa

    Administrators can use both Keepalived and HAProxy together for a more robust and
    scalable high availability environment. Using the speed and scalability of HAProxy
    to perform load balancing for HTTP and other TCP-based services in conjunction
    with Keepalived failover services, administrators can increase availability
    by distributing load across real servers as well as ensuring continuity
    in the event of router unavailability by performing failover to backup routers.

      keepalived 负责 routers 的故障转移(failover)
      haproxy 为 基于 http 和 tcp 的 services 提供 负载均衡(load balance)



    3.7. turning on packet forwarding and nonlocal binding
      https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/s1-initial-setup-forwarding-vsa

        Load balancing in HAProxy and Keepalived at the same time also requires the ability to bind
        to an IP address that are nonlocal, meaning that it is not assigned to a device on the
        local system. This allows a running load balancer instance to bind to an IP that is not local for failover.
          启用路由转发:
            net.ipv4.ip_forward = 1

          启用非本地ip绑定:
            net.ipv4.ip_nonlocal_bind = 1

----------------------------------------------------------------------------------------------------------------------------------







