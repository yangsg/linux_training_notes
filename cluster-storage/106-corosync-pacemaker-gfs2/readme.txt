

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/index
https://www.unixarena.com/2016/01/rhel7-configuring-gfs2-on-pacemakercorosync-cluster.html/



global file system 2


----------------------------------------------------------------------------------------------------
示例: cLVM + GFS2


                          messaging layer
           +-----HA Cluster(not ha)------+
           |                             |
           |                             |
           |    node01 (real server)     |
           |    ip: 192.168.175.101      |
           |                             |          iscsi
           |                             |          ip: 192.168.175.130
           |                             |
           |    node02  (real server)    |
           |    ip: 192.168.175.102      |
           |                             |
           +-----------------------------+



    注: 这里的 HA Clusster 并非是为 real servers 做高可用, 而是应该 gfs2 需要借助 Messaging Layer 传递信息,
        所以 这里将 real servers 放进 HA Cluster 中是为了借用 高可用集群提供的 Messaging Layer


----------------------------------------------------------------------------------------------------

1、在node01, node02上使用pacemaker创建HA集群
























