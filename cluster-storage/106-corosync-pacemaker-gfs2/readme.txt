

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









----------------------------------------------------------------------------------------------------
gfs2: global file system 2

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

// 添加主机名解析
[root@node01 ~]# vim /etc/hosts
    192.168.175.101 node01
    192.168.175.102 node02

[root@node02 ~]# vim /etc/hosts
    192.168.175.101 node01
    192.168.175.102 node02




----------------------------------------------------------------------------------------------------
配置 iscsi 主机

    加一块 8G 磁盘作为后端存储

        参考笔记:  https://github.com/yangsg/linux_training_notes/tree/master/cluster-ha-corosync-pacemaker


[root@iscsi ~]# lsblk -p
    NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    /dev/sda                      8:0    0   20G  0 disk
    ├─/dev/sda1                   8:1    0  200M  0 part /boot
    └─/dev/sda2                   8:2    0 19.8G  0 part
      ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
      └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
    /dev/sdb                      8:16   0    8G  0 disk  <----------观察
    /dev/sr0                     11:0    1 1024M  0 rom



// 安装 targetcli
[root@iscsi ~]# yum -y install targetcli
[root@iscsi ~]# rpm -q targetcli
    targetcli-2.1.fb46-7.el7.noarch

[root@iscsi ~]# systemctl start target
[root@iscsi ~]# systemctl enable target


   参考笔记  https://github.com/yangsg/linux_training_notes/tree/master/cluster-storage/099-iscsi-targetcli

[root@iscsi ~]# targetcli /backstores/block create name=disk01 dev=/dev/sdb  #创建 block 类型的后端存储
[root@iscsi ~]# targetcli /iscsi create iqn.2019-09.com.linux:target01       #创建 iSCSI target (initiator在login时会对其引用)
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/luns create /backstores/block/disk01  #创建 storage object 的逻辑存储单元
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls create iqn.2019-09.com.linux:client  #创建 initiator 连接用的 ACL
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals delete ip_address=0.0.0.0 ip_port=3260 #删除默认的入口
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/portals create ip_address=192.168.175.130      #创建自定义的入口
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute generate_node_acls=0   #使用 user-created ACLs' settings, 而非 the TPG-wide settings
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1 set attribute authentication=1       # 启用认证
[root@iscsi ~]# targetcli /iscsi/iqn.2019-09.com.linux:target01/tpg1/acls/iqn.2019-09.com.linux:client set auth userid=admin password=redhat #设置用户名和密码
[root@iscsi ~]# targetcli saveconfig   #保存配置


// 查看结果信息
[root@iscsi ~]# targetcli ls

      o- / ......................................................................................................................... [...]
        o- backstores .............................................................................................................. [...]
        | o- block .................................................................................................. [Storage Objects: 1]
        | | o- disk01 ........................................................................... [/dev/sdb (8.0GiB) write-thru activated]
        | |   o- alua ................................................................................................... [ALUA Groups: 1]
        | |     o- default_tg_pt_gp ....................................................................... [ALUA state: Active/optimized]
        | o- fileio ................................................................................................. [Storage Objects: 0]
        | o- pscsi .................................................................................................. [Storage Objects: 0]
        | o- ramdisk ................................................................................................ [Storage Objects: 0]
        o- iscsi ............................................................................................................ [Targets: 1]
        | o- iqn.2019-09.com.linux:target01 .................................................................................... [TPGs: 1]
        |   o- tpg1 .......................................................................................... [no-gen-acls, auth per-acl]
        |     o- acls .......................................................................................................... [ACLs: 1]
        |     | o- iqn.2019-09.com.linux:client ............................................................. [1-way auth, Mapped LUNs: 1]
        |     |   o- mapped_lun0 ................................................................................ [lun0 block/disk01 (rw)]
        |     o- luns .......................................................................................................... [LUNs: 1]
        |     | o- lun0 ..................................................................... [block/disk01 (/dev/sdb) (default_tg_pt_gp)]
        |     o- portals .................................................................................................... [Portals: 1]
        |       o- 192.168.175.130:3260 ............................................................................................. [OK]
        o- loopback ......................................................................................................... [Targets: 0]








// 后续会在 iscsi target 上 创建 lvm, 添加 global_filter 可以避免因
// 本地系统使用 该 lvm 而导致 target 服务在启动时 无法为该磁盘设备创建 StorageObject
// 注意必要时 reboot 系统
// 更多细节见   https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/logical_volume_manager_administration/lvm_filters
[root@iscsi ~]# vim /etc/lvm/lvm.conf
        global_filter = [ "r|/dev/sdb|" ]




              // 查看 lvmetad 相关信息
              [root@iscsi ~]# grep -in 'use_lvmetad =' /etc/lvm/lvm.conf
                  940:  use_lvmetad = 1
              [root@iscsi ~]# ps -elf | grep lvmetad
                  4 S root        509      1  0  80   0 - 48145 poll_s 17:04 ?        00:00:00 /usr/sbin/lvmetad -f



              // 如下即为 在 未 设置  global_filter 时 且在 iscsi target 上创建 逻辑卷后 重启 iscsi 主机报的错误:
              // [root@iscsi ~]# systemctl status target
              ● target.service - Restore LIO kernel target configuration
                 Loaded: loaded (/usr/lib/systemd/system/target.service; enabled; vendor preset: disabled)
                 Active: active (exited) since Fri 2019-09-06 16:54:59 CST; 7min ago
                Process: 909 ExecStart=/usr/bin/targetctl restore (code=exited, status=0/SUCCESS)
               Main PID: 909 (code=exited, status=0/SUCCESS)
                 CGroup: /system.slice/target.service

              Sep 06 16:54:54 iscsi systemd[1]: Starting Restore LIO kernel target configuration...
              Sep 06 16:54:59 iscsi target[909]: Could not create StorageObject disk01: Cannot configure StorageObject because device /dev/sdb is already in use, skipped
              Sep 06 16:54:59 iscsi target[909]: Could not find matching StorageObject for LUN 0, skipped
              Sep 06 16:54:59 iscsi target[909]: Could not find matching TPG LUN 0 for MappedLUN 0, skipped
              Sep 06 16:54:59 iscsi systemd[1]: Started Restore LIO kernel target configuration.

              // 非正常现象
              [root@iscsi ~]# targetcli ls
              o- / ...................................................................................... [...]
                o- backstores ........................................................................... [...]
                | o- block ............(<--非正常现象, 未显示 disk01磁盘信息)..............[Storage Objects: 0]
                | o- fileio .............................................................. [Storage Objects: 0]
                | o- pscsi ............................................................... [Storage Objects: 0]
                | o- ramdisk ............................................................. [Storage Objects: 0]
                o- iscsi ......................................................................... [Targets: 1]
                | o- iqn.2019-09.com.linux:target01 ................................................. [TPGs: 1]
                |   o- tpg1 ....................................................... [no-gen-acls, auth per-acl]
                |     o- acls ....................................................................... [ACLs: 1]
                |     | o- iqn.2019-09.com.linux:client .......................... [1-way auth, Mapped LUNs: 0]
                |     o- luns ....................................................................... [LUNs: 0]
                |     o- portals ................................................................. [Portals: 1]
                |       o- 192.168.175.130:3260 .......................................................... [OK]
                o- loopback ...................................................................... [Targets: 0]



              // 正常现象
              // 设置 global_filter 后 并 reboot 后执行 pvs 的效果(正常情况是不会看到 /dev/sdb):
              [root@iscsi ~]# pvs
                    PV         VG     Fmt  Attr PSize  PFree
                    /dev/sda2  centos lvm2 a--  19.80g    0










----------------------------------------------------------------------------------------------------
配置 node01  (探索 iscsi target)

[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sr0                     11:0    1 1024M  0 rom


[root@node01 ~]# yum -y install iscsi-initiator-utils
[root@node01 ~]# rpm -q iscsi-initiator-utils
    iscsi-initiator-utils-6.2.0.874-10.el7.x86_64

[root@node01 ~]# systemctl start iscsi iscsid
[root@node01 ~]# systemctl enable iscsi iscsid

[root@node01 ~]# ls /etc/iscsi/
    initiatorname.iscsi  iscsid.conf

[root@node01 ~]# vim /etc/iscsi/initiatorname.iscsi
    InitiatorName=iqn.2019-09.com.linux:client


[root@node01 ~]# vim /etc/iscsi/iscsid.conf

        node.session.auth.authmethod = CHAP

        node.session.auth.username = admin
        node.session.auth.password = redhat

[root@node01 ~]# systemctl restart iscsid

// 探测后端 iscsi target
[root@node01 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01

[root@node01 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.130:3260 -l
      Logging in to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] (multiple)
      Login to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] successful.


[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk  <-----观察(多了一块磁盘, /dev/sdb 即对应于通过 iscsi 协议连接的 后端存储)
      /dev/sr0                     11:0    1 1024M  0 rom




----------------------------------------------------------------------------------------------------
配置 node02

[root@node02 ~]# lsblk -p
    NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
    /dev/sda                      8:0    0   20G  0 disk  <---------- 观察, 此时仅有一块磁盘
    ├─/dev/sda1                   8:1    0  200M  0 part /boot
    └─/dev/sda2                   8:2    0 19.8G  0 part
      ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
      └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
    /dev/sr0                     11:0    1 1024M  0 rom




[root@node02 ~]# yum -y install iscsi-initiator-utils
[root@node02 ~]# rpm -q iscsi-initiator-utils
    iscsi-initiator-utils-6.2.0.874-10.el7.x86_64

[root@node02 ~]# systemctl start iscsi iscsid
[root@node02 ~]# systemctl enable iscsi iscsid

[root@node02 ~]# ls /etc/iscsi/
    initiatorname.iscsi  iscsid.conf

[root@node02 ~]# vim /etc/iscsi/initiatorname.iscsi
    InitiatorName=iqn.2019-09.com.linux:client


[root@node02 ~]# vim /etc/iscsi/iscsid.conf

        node.session.auth.authmethod = CHAP

        node.session.auth.username = admin
        node.session.auth.password = redhat

[root@node02 ~]# systemctl restart iscsid


// 探测后端 iscsi target
[root@node02 ~]# iscsiadm -m discovery -t st -p 192.168.175.130
      192.168.175.130:3260,1 iqn.2019-09.com.linux:target01

[root@node02 ~]# iscsiadm -m node -T iqn.2019-09.com.linux:target01 -p 192.168.175.130:3260 -l
      Logging in to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] (multiple)
      Login to [iface: default, target: iqn.2019-09.com.linux:target01, portal: 192.168.175.130,3260] successful.

[root@node02 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk <-----观察(多了一块磁盘, /dev/sdb 即对应于通过 iscsi 协议连接的 后端存储)
      /dev/sr0                     11:0    1 1024M  0 rom




----------------------------------------------------------------------------------------------------
在node01, node02上使用pacemaker创建HA集群

    参考笔记:  https://github.com/yangsg/linux_training_notes/tree/master/cluster-ha-corosync-pacemaker

创建集群

// 在每个集群节点上安装集群软件
[root@node01 ~]# yum install -y corosync pacemaker pcs fence-agents-all
[root@node02 ~]# yum install -y corosync pacemaker pcs fence-agents-all

// 观察, 安装完如上 软件包时, 会自动 创建 节点认证用的 用户 hacluster
[root@node01 ~]# grep 'hacluster' /etc/passwd
    hacluster:x:189:189:cluster user:/home/hacluster:/sbin/nologin
[root@node02 ~]# grep 'hacluster' /etc/passwd
    hacluster:x:189:189:cluster user:/home/hacluster:/sbin/nologin



// 为 认证用户 hacluster 设置密码
[root@node01 ~]# echo "redhat" | passwd --stdin hacluster
[root@node02 ~]# echo "redhat" | passwd --stdin hacluster

// 启动 每个集群节点上的 pcsd 服务 并设置为开机自启
[root@node01 ~]# systemctl start pcsd
[root@node01 ~]# systemctl enable pcsd

[root@node02 ~]# systemctl start pcsd
[root@node02 ~]# systemctl enable pcsd


// 查看一下 pcs  命令的简要帮助
[root@node01 ~]# pcs --help

      Usage: pcs [-f file] [-h] [commands]...
      Control and configure pacemaker and corosync.

      Options:
          -h, --help         Display usage and exit.
          -f file            Perform actions on file instead of active CIB.
          --debug            Print all network traffic and external commands run.
          --version          Print pcs version information. List pcs capabilities if
                             --full is specified.
          --request-timeout  Timeout for each outgoing request to another node in
                             seconds. Default is 60s.
          --force            Override checks and errors, the exact behavior depends on
                             the command. WARNING: Using the --force option is
                             strongly discouraged unless you know what you are doing.

      Commands:
          cluster     Configure cluster options and nodes.
          resource    Manage cluster resources.
          stonith     Manage fence devices.
          constraint  Manage resource constraints.
          property    Manage pacemaker properties.
          acl         Manage pacemaker access control lists.
          qdevice     Manage quorum device provider on the local host.
          quorum      Manage cluster quorum settings.
          booth       Manage booth (cluster ticket manager).
          status      View cluster status.
          config      View and manage cluster configuration.
          pcsd        Manage pcs daemon.
          node        Manage cluster nodes.
          alert       Manage pacemaker alerts.


// 认证集群节点[任意节点]
[root@node01 ~]# pcs cluster auth node01 node02
    Username: hacluster <=====输入用户名
    Password:           <=====输入密码
    node02: Authorized
    node01: Authorized

// 创建集群并启动集群[任意节点]
[root@node01 ~]# pcs cluster setup --name mycluster node01 node02
    Destroying cluster on nodes: node01, node02...
    node01: Stopping Cluster (pacemaker)...
    node02: Stopping Cluster (pacemaker)...
    node02: Successfully destroyed cluster
    node01: Successfully destroyed cluster

    Sending 'pacemaker_remote authkey' to 'node01', 'node02'
    node02: successful distribution of the file 'pacemaker_remote authkey'
    node01: successful distribution of the file 'pacemaker_remote authkey'
    Sending cluster config files to the nodes...
    node01: Succeeded
    node02: Succeeded

    Synchronizing pcsd certificates on nodes node01, node02...
    node02: Success
    node01: Success
    Restarting pcsd on the nodes in order to reload the certificates...
    node02: Success
    node01: Success

     // 注: 如上命令如果加上 --start --enable 选项, 则可以直接 在指定节点上 start 并 enable 该 cluster, 如:
     //            `pcs cluster --start --enable setup --name mycluster node01 node02`


[root@node01 ~]# pcs cluster start node01 node02
    node02: Starting Cluster (corosync)...
    node01: Starting Cluster (corosync)...
    node01: Starting Cluster (pacemaker)...
    node02: Starting Cluster (pacemaker)...

[root@node01 ~]# pcs cluster enable node01 node02
    node01: Cluster Enabled
    node02: Cluster Enabled


// 查看集群状态信息
[root@node01 ~]# pcs cluster status
      Cluster Status:
       Stack: corosync
       Current DC: node01 (version 1.1.19-8.el7_6.4-c3c624ea3d) - partition with quorum
       Last updated: Sat Sep  7 21:00:16 2019
       Last change: Sat Sep  7 21:00:15 2019 by hacluster via crmd on node01
       2 nodes configured
       0 resources configured

      PCSD Status:
        node01: Online
        node02: Online


// 注: 其实正常情况下载集群任意一个节点上都应该能查看到 集群的状态
[root@node02 ~]# pcs cluster status
      Cluster Status:
       Stack: corosync
       Current DC: node01 (version 1.1.19-8.el7_6.4-c3c624ea3d) - partition with quorum
       Last updated: Sat Sep  7 21:00:52 2019
       Last change: Sat Sep  7 21:00:15 2019 by hacluster via crmd on node01
       2 nodes configured
       0 resources configured

      PCSD Status:
        node02: Online
        node01: Online


// 查看 corosync 和 pacemaker 服务
[root@node01 ~]# systemctl is-active corosync pacemaker
    active
    active

[root@node02 ~]# systemctl is-active corosync pacemaker
    active
    active


----------------------------------------------------------------------------------------------------
调整集群属性

// 验证集群的正确性
[root@node01 ~]# crm_verify -L -V
       error: unpack_resources: Resource start-up disabled since no STONITH resources have been defined <----观察报错信息(没有STONITH resources)
       error: unpack_resources: Either configure some or disable STONITH with the stonith-enabled option
       error: unpack_resources: NOTE: Clusters with shared data need STONITH to ensure data integrity
    Errors found during check: config not valid


// 因为用于练习的集群环境中没有 fence设备, 所以这里 将 集群的 stonith 属性禁用掉
[root@node01 ~]# pcs property set stonith-enabled=false
[root@node01 ~]# crm_verify -L -V   #再次验证

    注: 如果集群中有 fence 设备, 则应使用 如 pcs stonith create 这样的命令去创建


// 因为集群中仅有两个节点(偶数), 所以这里将 no-quorum-policy 设置为 ignore, 使其不满足法定票数时依然提供服务
[root@node01 ~]# pcs property set no-quorum-policy=ignore
[root@node01 ~]# crm_verify -L -V  #再次验证



----------------------------------------------------------------------------------------------------
在所有节点安装cLVM及gfs2需要的软件

      https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/ch-clustsetup-gfs2


[root@node01 ~]# yum -y install lvm2-cluster gfs2-utils
[root@node01 ~]# lvmconf --enable-cluster
        注: 如上命令会 修改文件  /etc/lvm/lvm.conf  中的如下两项设置为:
            locking_type = 3
            use_lvmetad = 0


                注: locking_type 为 3 的含义如下:
                   3
                     LVM uses built-in clustered locking with clvmd.
                     This is incompatible with lvmetad. If use_lvmetad is enabled,
                     LVM prints a warning and disables lvmetad use.


[root@node01 ~]# reboot




[root@node02 ~]# yum -y install lvm2-cluster gfs2-utils
[root@node02 ~]# lvmconf --enable-cluster
        注: 如上命令会 修改文件  /etc/lvm/lvm.conf  中的如下两项设置为:
            locking_type = 3
            use_lvmetad = 0

[root@node02 ~]# reboot




----------------------------------------------------------------------------------------------------
在任意节点创建cLVM及gfs2需要的资源 (即与 clvm 和 gfs2 相关的资源都由 集群统一来管理)

    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/ch-clustsetup-gfs2

无 stonith 设备:
// 因为 当前联系环境中 没有 fence 设备, 所以此处创建资源时 禁用了 stonith 特性
[root@node01 ~]# pcs resource create dlm ocf:pacemaker:controld \
                      allow_stonith_disabled=true \
                      op monitor interval=30s clone interleave=true ordered=true

[root@node01 ~]# pcs resource create clvmd ocf:heartbeat:clvm \
                      op monitor interval=30s clone interleave=true ordered=true


    有 stonith 设备:
       注: 如果有 fence 设备, 应该使用 如下命令来创建 dlm 和 clvmd 集群资源
          pcs resource create dlm ocf:pacemaker:controld op monitor interval=30s on-fail=fence clone interleave=true ordered=true
          pcs resource create clvmd ocf:heartbeat:clvm op monitor interval=30s on-fail=fence clone interleave=true ordered=true


// 查看创建的资源
[root@node01 ~]# pcs resource show
     Clone Set: dlm-clone [dlm]
         Started: [ node01 node02 ]
     Clone Set: clvmd-clone [clvmd]
         Started: [ node01 node02 ]

// 创建资源约束，保证资源正常的启动顺序、多个资源同进同退(Set up clvmd and dlm dependency and start up order.):
      因为 clvm 依赖 dlm 中的 locks, 所以 clvmd 必须在 dlm  之后 start, 且 clvmd 必须 运行在 与 dlm 相同的 node 上.
[root@node01 ~]# pcs constraint order start dlm-clone then clvmd-clone      #先启动 dlm-clone 后启动 clvmd-clone
    Adding dlm-clone clvmd-clone (kind: Mandatory) (Options: first-action=start then-action=start)

[root@node01 ~]# pcs constraint colocation add clvmd-clone with dlm-clone   #让 clvmd-clone 跟随 dlm-clone 同进同退


// 查看创建的约束
[root@node01 ~]# pcs constraint show
    Location Constraints:
    Ordering Constraints:
      start dlm-clone then start clvmd-clone (kind:Mandatory)
    Colocation Constraints:
      clvmd-clone with dlm-clone (score:INFINITY)
    Ticket Constraints:





----------------------------------------------------------------------------------------------------
在任意节点创建逻辑卷

      https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/ch-clustsetup-gfs2

[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk  <-------观察
      /dev/sr0                     11:0    1 1024M  0 rom


[root@node01 ~]# pvcreate /dev/sdb

[root@node01 ~]# vgcreate -cy vg01 /dev/sdb
      Clustered volume group "vg01" successfully created

   选项描述:
       -c|--clustered y|n
              Create a clustered VG using clvmd if LVM is compiled with cluster support.  This allows multiple hosts to share a VG on
              shared devices.  clvmd and a lock manager must be configured and running.  (A clustered VG using clvmd is different from a
              shared VG using lvmlockd.)  See clvmd(8) for more information about clustered VGs.


          Warning(警告)

            When you create volume groups with CLVM on shared storage, you must ensure that all nodes in the cluster
            have access to the physical volumes that constitute the volume group. Asymmetric cluster
            configurations in which some nodes have access to the storage and others do not are not supported.

            When managing volume groups using CLVMD to allow for concurrent activation of volumes
            across multiple nodes, the volume groups must have the clustered flag enabled.
            This flag allows CLVMD to identify the volumes it must manage, which is what
            enables CLVMD to maintain LVM metadata continuity. Failure to adhere to this
            configuration renders the configuration unsupported by Red Hat and may result in storage corruption and loss of data.


[root@node01 ~]# lvcreate -l 100%FREE -n lv01 vg01


[root@node01 ~]# vgdisplay vg01
      --- Volume group ---
      VG Name               vg01
      System ID
      Format                lvm2
      Metadata Areas        1
      Metadata Sequence No  2
      VG Access             read/write
      VG Status             resizable
      Clustered             yes  <-----------观察
      Shared                no
      MAX LV                0
      Cur LV                1
      Open LV               0
      Max PV                0
      Cur PV                1
      Act PV                1
      VG Size               <8.00 GiB
      PE Size               4.00 MiB
      Total PE              2047
      Alloc PE / Size       2047 / <8.00 GiB
      Free  PE / Size       0 / 0
      VG UUID               y9eZI1-Abb6-Ak7c-ivvB-V5B1-4Ie8-qfJPWo




[root@node01 ~]# lvscan
      ACTIVE            '/dev/vg01/lv01' [<8.00 GiB] inherit  <---------------观察
      ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
      ACTIVE            '/dev/centos/root' [17.80 GiB] inherit

[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    8G  0 disk
      └─/dev/mapper/vg01-lv01     253:2    0    8G  0 lvm  <------观察
      /dev/sr0                     11:0    1 1024M  0 rom


// 使用  GFS2 文件系统格式化 逻辑卷, 每个 node 都需要一个 日志区域(One journal is required for each node that mounts the file system)
// 所以请确保 为 集群中的 每个 node 创建足够的 journals. (所以 journals 的个数应该 大于或等于 集群中 nodes 的个数)
[root@node01 ~]# mkfs.gfs2 -j2 -p lock_dlm -t mycluster:lock_tb_01 /dev/vg01/lv01
          /dev/vg01/lv01 is a symbolic link to /dev/dm-2
          This will destroy any data on /dev/dm-2
          Are you sure you want to proceed? [y/n] y
          Discarding device contents (may take a while on large devices): Done
          Adding journals: Done
          Building resource groups: Done
          Creating quota file: Done
          Writing superblock and syncing: Done
          Device:                    /dev/vg01/lv01
          Block size:                4096
          Device size:               8.00 GB (2096128 blocks)
          Filesystem size:           8.00 GB (2096126 blocks)
          Journals:                  2
          Journal size:              32MB
          Resource groups:           34
          Locking protocol:          "lock_dlm"
          Lock table:                "mycluster:lock_tb_01"
          UUID:                      283f5f71-8934-4d06-892b-e516af949e55



  注:
      LockProtoName
          Specifies the name of the locking protocol to use. The lock protocol for a cluster is lock_dlm.

      LockTableName
          This parameter is specified for a GFS2 file system in a cluster configuration.
          It has two parts separated by a colon (no spaces) as follows: ClusterName:FSName
          ClusterName, the name of the cluster for which the GFS2 file system is being created.
          FSName, the file system name, can be 1 to 16 characters long. The name must be unique
          for all lock_dlm file systems over the cluster,
          and for all file systems (lock_dlm and lock_nolock) on each local node.

           注: ClusterName:FSName 中 ClusterName 为集群名, FSName 长度为 1 到 16 个 characters, 且对于 cluster 中
               的所有文件系统(lock_dlm and lock_nolock)来说 该名字必须是唯一的.

       -j journals
              The number of journals for mkfs.gfs2 to create.  At least one journal is required for each  machine  that
              will  mount  the filesystem concurrently.  If this option is not specified, only one journal will be cre‐
              ated. This number may be used as an indicator of the number of nodes in the cluster in order to  optimize
              the  layout of the filesystem. As such, it is best to set this option with the maximum number of mounters
              in mind than to add more journals later.

       -p protocol
              Specify the locking protocol to use when no locking protocol is specified at mount time. Valid locking protocols are:

                 lock_dlm
                        This is the default. It enables DLM-based locking for use in shared storage configurations.

                 lock_nolock
                        This enables single-node locking

      Warning(警告)

          When you create the GFS2 filesystem, it is important to specify a correct value for
          the -t LockTableName option. The correct format is ClusterName:FSName.
          Failure to specify a correct value will prevent the filesystem from mounting.
          Additionally, the file system name must be unique.
          For more information on the options for the mkfs.gfs2 command, see Section 3.1, “Making a File System”.

              https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/global_file_system_2/ch-manage#s1-manage-makefs


[root@node01 ~]# blkid /dev/vg01/lv01
      /dev/vg01/lv01: LABEL="mycluster:lock_tb_01" UUID="283f5f71-8934-4d06-892b-e516af949e55" TYPE="gfs2"


----------------------------------------------------------------------------------------------------
在任意节点上创建资源挂载集群逻辑卷 (即挂载的操作也应该当成集群资源让 集群来帮助挂载, 而不是自己去编辑 /etc/fstab 挂载)


无 stonith 设备:
// 因为当前联系环境中 没有 fence 设备, 所以使用 如下的命令创建
[root@node01 ~]# pcs resource create clusterfs ocf:heartbeat:Filesystem \
                    device=/dev/vg01/lv01 \
                    directory=/mnt \
                    fstype=gfs2 options="noatime,nodiratime" op monitor interval=10s clone interleave=true


          有 stonith 设备:
          [root@node01 ~]# pcs resource create clusterfs ocf:heartbeat:Filesystem \
                              device=/dev/vg01/lv01 \
                              directory=/mnt \
                              fstype="gfs2" options="noatime,nodiratime" op monitor interval=10s on-fail=fence clone interleave=true


// 查看创建的集群资源
[root@node01 ~]# pcs resource show
     Clone Set: dlm-clone [dlm]
         Started: [ node01 node02 ]
     Clone Set: clvmd-clone [clvmd]
         Started: [ node01 node02 ]
     Clone Set: clusterfs-clone [clusterfs]  <------观察
         Started: [ node01 node02 ]


// 创建 GFS2 的约束(Set up GFS2 and clvmd dependency and startup order. GFS2 must start after clvmd and must run on the same node as clvmd.)
[root@node01 ~]# pcs constraint order start clvmd-clone then clusterfs-clone
      Adding clvmd-clone clusterfs-clone (kind: Mandatory) (Options: first-action=start then-action=start)

[root@node01 ~]# pcs constraint colocation add clusterfs-clone with clvmd-clone


// 查看创建的约束
[root@node01 ~]# pcs constraint show
    Location Constraints:
    Ordering Constraints:
      start dlm-clone then start clvmd-clone (kind:Mandatory)
      start clvmd-clone then start clusterfs-clone (kind:Mandatory)  <-----观察
    Colocation Constraints:
      clvmd-clone with dlm-clone (score:INFINITY)
      clusterfs-clone with clvmd-clone (score:INFINITY)  <-----观察
    Ticket Constraints:




[root@node01 ~]# df -hT
    Filesystem              Type      Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root xfs        18G  2.0G   16G  12% /
    devtmpfs                devtmpfs  478M     0  478M   0% /dev
    tmpfs                   tmpfs     489M   75M  414M  16% /dev/shm
    tmpfs                   tmpfs     489M   13M  476M   3% /run
    tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
    /dev/sda1               xfs       197M  103M   95M  53% /boot
    tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
    /dev/mapper/vg01-lv01   gfs2      8.0G   67M  8.0G   1% /mnt  <------------观察


[root@node02 ~]# df -hT
    Filesystem              Type      Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root xfs        18G  2.0G   16G  12% /
    devtmpfs                devtmpfs  478M     0  478M   0% /dev
    tmpfs                   tmpfs     489M   60M  429M  13% /dev/shm
    tmpfs                   tmpfs     489M   13M  476M   3% /run
    tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
    /dev/sda1               xfs       197M  103M   95M  53% /boot
    tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
    /dev/mapper/vg01-lv01   gfs2      8.0G   67M  8.0G   1% /mnt  <------------观察


[root@node01 ~]# mount |grep lv01
      /dev/mapper/vg01-lv01 on /mnt type gfs2 (rw,noatime,nodiratime)







----------------------------------------------------------------------------------------------------
测试:

[root@node01 ~]# touch /mnt/node01.txt
[root@node02 ~]# ls /mnt/
    node01.txt

[root@node02 ~]# touch /mnt/node02.txt
[root@node01 ~]# ls /mnt/
    node01.txt  node02.txt


至此结束


----------------------------------------------------------------------------------------------------

[root@node01 ~]# rpm -ql lvm2-cluster
        /usr/sbin/clvmd
        /usr/share/man/man8/clvmd.8.gz

[root@node01 ~]# rpm -ql gfs2-utils
        /usr/lib/udev/rules.d/82-gfs2-withdraw.rules
        /usr/sbin/fsck.gfs2
        /usr/sbin/gfs2_convert
        /usr/sbin/gfs2_edit
        /usr/sbin/gfs2_grow
        /usr/sbin/gfs2_jadd
        /usr/sbin/gfs2_withdraw_helper
        /usr/sbin/glocktop
        /usr/sbin/mkfs.gfs2
        /usr/sbin/tunegfs2
        /usr/share/doc/gfs2-utils-3.1.10
        /usr/share/doc/gfs2-utils-3.1.10/COPYING.applications
        /usr/share/doc/gfs2-utils-3.1.10/COPYING.libraries
        /usr/share/doc/gfs2-utils-3.1.10/COPYRIGHT
        /usr/share/doc/gfs2-utils-3.1.10/README.contributing
        /usr/share/doc/gfs2-utils-3.1.10/README.licence
        /usr/share/doc/gfs2-utils-3.1.10/README.tests
        /usr/share/doc/gfs2-utils-3.1.10/gfs2.txt
        /usr/share/doc/gfs2-utils-3.1.10/journaling.txt
        /usr/share/man/man5/gfs2.5.gz
        /usr/share/man/man8/fsck.gfs2.8.gz
        /usr/share/man/man8/gfs2_convert.8.gz
        /usr/share/man/man8/gfs2_edit.8.gz
        /usr/share/man/man8/gfs2_grow.8.gz
        /usr/share/man/man8/gfs2_jadd.8.gz
        /usr/share/man/man8/glocktop.8.gz
        /usr/share/man/man8/mkfs.gfs2.8.gz
        /usr/share/man/man8/tunegfs2.8.gz




































