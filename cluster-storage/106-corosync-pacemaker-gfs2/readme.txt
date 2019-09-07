

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/index
https://www.unixarena.com/2016/01/rhel7-configuring-gfs2-on-pacemakercorosync-cluster.html/

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/ch-clustsetup-gfs2
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/high_availability_add-on_administration/ch-startup-haaa

----------------------------------------------------------------------------------------------------
DLM: Distributed Lock Manager, 即 分布式锁管理器
      https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/6/html/high_availability_add-on_overview/ch-dlm

        Lock Manager 是 一种通用集群架构服务(service), 为 其他的 集群架构 组件 提供了一种 同步(synchronize)访问共享资源的机制.
                     其扮演者 交通警察 的角色.

            DLM 运行在 每个 cluster node 上, lock management  被分布在 集群中的 所有 nodes 上,
            GFS2 和 CLVM 使用了 lock manager 中的 locks. GFS2 使用 lock manager 中的 locks 来
            同步(synchronize) 到 file system metadata (on shared storage) 的访问. CLVM 使用 lock manager 中的 locks
            来同步 对 LVM volumes 和 volume groups (also on shared storage) 的 更新(updates).

----------------------------------------------------------------------------------------------------
cLVM: cluster LVM, 即 集群逻辑卷

  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/logical_volume_manager_administration/lvm_cluster_overview

    The Red Hat High Availability Add-On provides support for LVM volumes in two distinct cluster configurations:

      HA-LVM:
            High availability LVM volumes (HA-LVM) in an active/passive failover configurations
            in which only a single node of the cluster accesses the storage at any one time.

      CLVM:
            LVM volumes that use the Clustered Logical Volume (CLVM) extensions in an active/active configurations
            in which more than one node of the cluster requires access to the storage at the same time.
            CLVM is part of the Resilient Storage Add-On.


CLVM 或 HA-LVM 的选择:

      选择 CLVMD 的情况: 如果 集群中的 多个 nodes 需要 同时 对 active/active system
                  中的 LVM volumes 做 read/write 访问时, 那么你必须使用 CLVMD.
      - If multiple nodes of the cluster require simultaneous read/write access to
        LVM volumes in an active/active system, then you must use CLVMD.
        CLVMD provides a system for coordinating activation of and changes to LVM volumes
        across nodes of a cluster concurrently. CLVMD's clustered-locking service provides
        protection to LVM metadata as various nodes of the cluster interact with volumes
        and make changes to their layout. This protection is contingent upon appropriately
        configuring the volume groups in question, including setting locking_type to 3
        in the lvm.conf file and setting the clustered flag on any volume group
        that will be managed by CLVMD and activated simultaneously across multiple cluster nodes.

      选择 HA-LVM 的情况: 如果高可用集群被配置为 以 active/passive 的方式来管理 shared resources,
                   且一次仅只有一个  成员需要 访问给定的 LVM volume 时, 那么你可以使用 HA-LVM.
                   而无需 CLVMD 的 clustered-locking service.
      - If the high availability cluster is configured to manage shared resources
        in an active/passive manner with only one single member needing access
        to a given LVM volume at a time, then you can use HA-LVM without the CLVMD clustered-locking service



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
前期准备:
      时间同步
      主机名解析



----------------------------------------------------------------------------------------------------
1、在node01, node02上使用pacemaker创建HA集群
























