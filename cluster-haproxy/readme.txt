

https://github.com/haproxy/haproxy
https://www.haproxy.org/


haproxy官方文档:
    https://cbonte.github.io/haproxy-dconv/

keepalived 官方文档:
    https://keepalived.org/doc/   <--- 文档应该参考这里
    https://www.keepalived.org/   <--- 官网, 不过 document 已经 被 deprecated 了


  man keepalived.conf
      https://www.systutorials.com/docs/linux/man/5-keepalived.conf/


关于负载均衡:
      The Load Balancer is a set of integrated software components that provide for balancing
      IP traffic across a set of real servers. It consists of two main technologies
      to monitor cluster members and cluster services: Keepalived and HAProxy.
      Keepalived uses Linux virtual server (LVS) to perform load balancing
      and failover tasks on the active and passive routers,
      while HAProxy performs load balancing and high-availability services to TCP and HTTP applications.


haproxy 可以执行 tcp(4层)调度 或 http(7层) 调度
lvs 属于 4层 调度
nginx 属于 7 层调度

---------------------------------------------------------------------------------------------------
keepalived 的工作方式:
        https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/load_balancer_administration/ch-lvs-overview-vsa

  |-------------------------------------------virtual router(provide virtual service on VIP)-------------------------------------|
  |                     ^                                                                                                        |
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
  |                                                                                                                              |
  |                                                                                                                              |
  |                                                                                                                              |
  |------------------------------------------------------------------------------------------------------------------------------|
                         |
                         |
                         | load balance
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

---------------------------------------------------------------------------------------------------
















