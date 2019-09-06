

网上资料:
        https://blog.51cto.com/11107124/1868577
        https://blog.51cto.com/jiayimeng/1874741
        https://www.iyunv.com/thread-18105-1-1.html


    https://www.suse.com/documentation/sle_ha/book_sleha/data/sec_ha_architecture.html
    https://clusterlabs.org/
    https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/high_availability_add-on_administration/ch-startup-haaa
    https://www.unixarena.com/2015/12/rhel-7-redhat-cluster-with-pacemaker-overview.html/




            ---------------------------------------
            Resource Agent (类型: lsb, ocf 等)
            ---------------------------------------
            Cluster Resource Manager (pacemaker)
            ---------------------------------------
            Messaging Layer  (corosync)
            ---------------------------------------
            node01  node02



        https://www.suse.com/documentation/sle_ha/book_sleha/data/sec_ha_architecture.html
        https://www.suse.com/documentation/sle-ha-12/singlehtml/book_sleha/book_sleha.html#sec.ha.architecture.layers

             RA                           RA
             ↑                            ↑
             |                            |
             |                            |                   Resource Layer
             |                            |                   --------------------------------
             ↓                            ↓
            LRM       PE ←-----CIB(xml)  LRM       CIB(xml, replica)
             ↑        ↑         ↑         ↑         ↑
             |        |         |         |         |
             |        |         |         |         |
             | |------|         |         |         |         Resource Allocation Layer
             | |                |         |         |
             | ↓                |         ↓         |
        (DC)CRM ----------------|        CRM ←------|
             ↑                            ↑
             |                            |                   --------------------------------
             |                            |                    Messaging and Infrastructure Layer
        Corosync/OpenAIS -------------- Corosync/OpenAIS
             |                            |
             |                            |
             |                            |
             ↓                            ↓
            node01                       node02



----------------------------------------------------------------------------------------------------
HA高可用集群的基本概念、体系结构


1、基本概念
  服务   service
    由多个资源组成
  资源   resource
  节点   node


资源类型

    1)  Primitive资源(主资源)
        a)  同一时间只能运行在同一个节点上

    2)  主从资源(Master/Slave资源)   【drbd分布式块设备】
        a)  依赖于Primitive资源
        b)  同一时间可以运行在两个节点上

    3)  Clone资源   fence_agent进程
        a)  同时运行在多个节点上的资源

    4)  资源组   resource group
        作用：保证多个资源可以同进同退


资源约束Constraint关系

    1)  顺序约束   order constraint
        a)  定义资源的启动顺序 【分数score】
    2)  排列约束    collation constraint
        a)  保证多个资源可在同一个节点上运行或者多个资源可同时转移
        b)  INFINITY  无穷大
    3)  位置约束  location constraint
        a)  定义资源对集群节点的依赖性
        b)  INFINITY   无穷大


noquorum policy   不满足法定票数策略
  法定票数：
    HA集群获得的票数高于总票数的一半

  不满足法定票数  noquorum
     freeze    默认策略
     stop
     ignore



----------------------------------------------------------------------------------------------------
pacemaker
  基于corosync作为HA集群的message layer，使用packmaker作为CRM集群资源管理层以构建高可用集群
  配置工具：
    pcs命令   依赖于pcsd服务

----------------------------------------------------------------------------------------------------
示例: pacemaker集群实现web服务高可用   cLVM


                         vip:192.168.175.100
       +-------------------------------------------------------------+
       |  node01                             node02                  |
       |  ip: 192.168.175.101                ip: 192.168.175.102     |
       +----------------------------|--------------------------------+
                                    |
                                    |
                         +----------|------------+
                         |  iscsi                |
                         |  ip: 192.168.175.130  |
                         +-----------------------+

----------------------------------------------------------------------------------------------------
准备工作
    配置IP、主机名称
    配置主机名的解析
    时间同步

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


----------------------------------------------------------------------------------------------------
配置 node01

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
在任意节点上创建逻辑卷/dev/vg01/lv01，并格式为ext4文件系统

[root@node01 ~]# pvcreate /dev/sdb
[root@node01 ~]# vgcreate vg01 /dev/sdb
[root@node01 ~]# lvcreate -l 100%FREE -n lv01 vg01

[root@node01 ~]# mkfs.ext4 /dev/vg01/lv01
      mke2fs 1.42.9 (28-Dec-2013)
      Filesystem label=
      OS type: Linux
      Block size=4096 (log=2)
      Fragment size=4096 (log=2)
      Stride=0 blocks, Stripe width=1024 blocks
      524288 inodes, 2096128 blocks
      104806 blocks (5.00%) reserved for the super user
      First data block=0
      Maximum filesystem blocks=2147483648
      64 block groups
      32768 blocks per group, 32768 fragments per group
      8192 inodes per group
      Superblock backups stored on blocks:
        32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632

      Allocating group tables: done
      Writing inode tables: done
      Creating journal (32768 blocks): done
      Writing superblocks and filesystem accounting information: done

// 在 node01 上列出逻辑卷
[root@node01 ~]# lvscan
      ACTIVE            '/dev/vg01/lv01' [<8.00 GiB] inherit  <----观察(在 node01 上能看到创建的 逻辑卷)
      ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
      ACTIVE            '/dev/centos/root' [17.80 GiB] inherit

// 在 node02 上列出逻辑卷
[root@node02 ~]# lvscan
    ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit    #注:可以观察到, 在 node02上 没有看到创建的 逻辑卷
    ACTIVE            '/dev/centos/root' [17.80 GiB] inherit






----------------------------------------------------------------------------------------------------
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
    node01: Successfully destroyed cluster
    node02: Successfully destroyed cluster

    Sending 'pacemaker_remote authkey' to 'node01', 'node02'
    node01: successful distribution of the file 'pacemaker_remote authkey'
    node02: successful distribution of the file 'pacemaker_remote authkey'
    Sending cluster config files to the nodes...
    node01: Succeeded
    node02: Succeeded

    Synchronizing pcsd certificates on nodes node01, node02...
    node02: Success
    node01: Success
    Restarting pcsd on the nodes in order to reload the certificates...
    node02: Success
    node01: Success


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
       Last updated: Thu Sep  5 22:52:36 2019
       Last change: Thu Sep  5 22:51:26 2019 by hacluster via crmd on node01
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
       Last updated: Thu Sep  5 22:54:16 2019
       Last change: Thu Sep  5 22:51:26 2019 by hacluster via crmd on node01
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


// 因为集群中仅有两个节点(偶数), 所以这里讲 no-quorum-policy 设置为 ignore, 使其不满足法定票数时依然提供服务
[root@node01 ~]# pcs property set no-quorum-policy=ignore
[root@node01 ~]# crm_verify -L -V  #再次验证


----------------------------------------------------------------------------------------------------
创建集群逻辑卷(cLVM: cluster LVM)，在集群所有节点上完成如下操作

  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/high_availability_add-on_administration/s1-exclusiveactive-haaa

    注: 因为资源属于集群, 而不属于节点, 所以如 vip, httpd, iscsi 等这种资源应该由集群来分配管理(如设置, 启动 或 挂载等)

--------------
针对 node01

[root@node01 ~]# lvscan
    ACTIVE            '/dev/vg01/lv01' [<8.00 GiB] inherit
    ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
    ACTIVE            '/dev/centos/root' [17.80 GiB] inherit


// 禁止系统激活逻辑卷
[root@node01 ~]# lvmconf --enable-halvm --services --startstopservices
    Warning: Stopping lvm2-lvmetad.service, but it can still be activated by:
      lvm2-lvmetad.socket
    Removed symlink /etc/systemd/system/sysinit.target.wants/lvm2-lvmetad.socket.


// 编辑lvm配置文件，把系统逻辑卷排除出去
// 即 除了 系统逻辑卷之外, 其他的逻辑卷应由 集群激活
[root@node01 ~]# vim /etc/lvm/lvm.conf

        volume_list = [ "centos" ]
        #注: 如果机器中没有其他的逻辑卷，此行需要写成volume_list=[ ]


// 重新生成系统启动镜像(boot image)文件, 使其不会尝试 激活有 集群(cluster)控制的 卷组
[root@node01 ~]# dracut -H -f /boot/initramfs-$(uname -r).img $(uname -r)
[root@node01 ~]# reboot   #需要重新启动系统


-----------------
针对 node02

[root@node02 ~]# lvscan
    ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
    ACTIVE            '/dev/centos/root' [17.80 GiB] inherit



// 禁止系统激活逻辑卷
[root@node02 ~]# lvmconf --enable-halvm --services --startstopservices
    Warning: Stopping lvm2-lvmetad.service, but it can still be activated by:
      lvm2-lvmetad.socket
    Removed symlink /etc/systemd/system/sysinit.target.wants/lvm2-lvmetad.socket.



// 编辑lvm配置文件，把系统逻辑卷排除出去
// 即 除了 系统逻辑卷之外, 其他的逻辑卷应由 集群激活
[root@node02 ~]# vim /etc/lvm/lvm.conf

        volume_list = [ "centos" ]
        #注: 如果机器中没有其他的逻辑卷，此行需要写成volume_list=[ ]


// 重新生成系统启动镜像(boot image)文件, 使其不会尝试 激活有 集群(cluster)控制的 卷组
[root@node02 ~]# dracut -H -f /boot/initramfs-$(uname -r).img $(uname -r)
[root@node02 ~]# reboot   #需要重新启动系统


-----------------
重启后查看效果

[root@node01 ~]# lvscan
      inactive          '/dev/vg01/lv01' [<8.00 GiB] inherit <----观察(能查看到逻辑卷 '/dev/vg01/lv01',且为 非激活(inactive)状态 )
      ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
      ACTIVE            '/dev/centos/root' [17.80 GiB] inherit

[root@node02 ~]# lvscan
      inactive          '/dev/vg01/lv01' [<8.00 GiB] inherit <----观察(能查看到逻辑卷 '/dev/vg01/lv01',且为 非激活(inactive)状态 )
      ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
      ACTIVE            '/dev/centos/root' [17.80 GiB] inherit




----------------------------------------------------------------------------------------------------
创建web服务资源

与创建的资源:
          ip
          httpd
          fs
          lvm


// 列出查看所有可用的 RA
[root@node01 ~]# pcs resource list | less

      略 略 略 略 略 略 略 略 略
      格式:[<standard>:[<provider>:]]<type>

      lsb:netconsole - netconsole
      lsb:network - Bring up/down networking
      ocf:heartbeat:apache - Manages an Apache Web server instance
      ocf:heartbeat:clvm - clvmd
      ocf:heartbeat:dhcpd - Chrooted ISC DHCP server resource agent.
      ocf:heartbeat:docker - Docker container resource agent.
      ocf:heartbeat:IPaddr - Manages virtual IPv4 and IPv6 addresses (Linux specific
                             version)
      ocf:heartbeat:IPaddr2 - Manages virtual IPv4 and IPv6 addresses (Linux specific
                              version)
      ocf:heartbeat:SendArp - Broadcasts unsolicited ARP announcements
      ocf:heartbeat:tomcat - Manages a Tomcat servlet environment instance
                                 status to an HTML file
      service:corosync - systemd unit file for corosync
      service:corosync-notifyd - systemd unit file for corosync-notifyd
      service:crm_mon - systemd unit file for crm_mon
                                               org.freedesktop.hostname1
      service:haproxy - systemd unit file for haproxy
      service:httpd - systemd unit file for httpd
      systemd:pacemaker - systemd unit file for pacemaker
      systemd:pcsd - systemd unit file for pcsd

      略 略 略 略 略 略 略 略 略


// 查看指定 RA 的描述
[root@client ~]# pcs resource describe ocf:heartbeat:IPaddr2


// 创建 ip 资源(注:不论该ip资源创建于哪个节点, 创建出来的资源属于集群,不属于节点)
[root@node01 ~]# pcs resource create web_vip ocf:heartbeat:IPaddr2 ip=192.168.175.100 cidr_netmask=24 --group webgroup

// 显示 当前所有 配置的资源
[root@node01 ~]# pcs resource show
     Resource Group: webgroup
         web_vip  (ocf::heartbeat:IPaddr2): Started node01 <----注: 资源创建出来以后,就直接分配给某个节点了

// 查看一下 node01 上的 ip 信息
[root@node01 ~]# ip a
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
    link/ether 00:0c:29:d7:f9:47 brd ff:ff:ff:ff:ff:ff
    inet 192.168.175.101/24 brd 192.168.175.255 scope global ens33
       valid_lft forever preferred_lft forever
    inet 192.168.175.100/24 brd 192.168.175.255 scope global secondary ens33 <----- 观察(即 vip 已经被集群分配给 node01 了)
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fed7:f947/64 scope link
       valid_lft forever preferred_lft forever


// 查看一下 ocf:heartbeat:LVM 的描述
[root@client ~]# pcs resource describe ocf:heartbeat:LVM

// 创建lvm资源,指定为集群准备的卷组名
[root@node01 ~]# pcs resource create web_lvm ocf:heartbeat:LVM volgrpname=vg01 exclusive=true --group webgroup


// 显示 当前所有 配置的资源
[root@node01 ~]#  pcs resource show
     Resource Group: webgroup
         web_vip  (ocf::heartbeat:IPaddr2): Started node01
         web_lvm  (ocf::heartbeat:LVM): Started node01  <------观察


[root@node01 ~]# lvscan
  ACTIVE            '/dev/vg01/lv01' [<8.00 GiB] inherit  <-----观察(集群激活了逻辑卷资源)
  ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
  ACTIVE            '/dev/centos/root' [17.80 GiB] inherit


[root@node02 ~]# lvscan
    inactive          '/dev/vg01/lv01' [<8.00 GiB] inherit <-----观察
    ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
    ACTIVE            '/dev/centos/root' [17.80 GiB] inherit


[root@node01 ~]# yum -y install httpd
[root@node02 ~]# yum -y install httpd


[root@node01 ~]# df -hT
    Filesystem              Type      Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root xfs        18G  2.0G   16G  12% /
    devtmpfs                devtmpfs  478M     0  478M   0% /dev
    tmpfs                   tmpfs     489M   53M  436M  11% /dev/shm
    tmpfs                   tmpfs     489M  6.8M  482M   2% /run
    tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
    /dev/sda1               xfs       197M  103M   95M  52% /boot
    tmpfs                   tmpfs      98M     0   98M   0% /run/user/0


// 创建文件系统资源,挂载逻辑卷
[root@node01 ~]# pcs resource create web_fs ocf:heartbeat:Filesystem device=/dev/vg01/lv01 directory=/var/www/html fstype=ext4 --group webgroup

[root@node01 ~]# pcs resource show
     Resource Group: webgroup
         web_vip  (ocf::heartbeat:IPaddr2): Started node01
         web_lvm  (ocf::heartbeat:LVM): Started node01
         web_fs (ocf::heartbeat:Filesystem):  Started node01 <----观察

[root@node01 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root xfs        18G  2.0G   16G  12% /
      devtmpfs                devtmpfs  478M     0  478M   0% /dev
      tmpfs                   tmpfs     489M   53M  436M  11% /dev/shm
      tmpfs                   tmpfs     489M  6.8M  482M   2% /run
      tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1               xfs       197M  103M   95M  52% /boot
      tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
      /dev/mapper/vg01-lv01   ext4      7.8G   36M  7.3G   1% /var/www/html <------观察


[root@node01 ~]# echo 'pcs web test' > /var/www/html/index.html



// 创建Apache资源
[root@node01 ~]# pcs resource describe ocf:heartbeat:apache
[root@node01 ~]# pcs resource create web_service ocf:heartbeat:apache configfile="/etc/httpd/conf/httpd.conf" --group webgroup
[root@node01 ~]# pcs resource show
   Resource Group: webgroup
       web_vip  (ocf::heartbeat:IPaddr2): Started node01
       web_lvm  (ocf::heartbeat:LVM): Started node01
       web_fs (ocf::heartbeat:Filesystem):  Started node01
       web_service  (ocf::heartbeat:apache):  Started node01  <-------观察

// 注: 集群资源属于集群, 所以正常情况下 在集群中的 任意节点都应该能看到这些集群资源
[root@node02 ~]# pcs resource show
     Resource Group: webgroup
         web_vip  (ocf::heartbeat:IPaddr2): Started node01
         web_lvm  (ocf::heartbeat:LVM): Started node01
         web_fs (ocf::heartbeat:Filesystem):  Started node01
         web_service  (ocf::heartbeat:apache):  Started node01


[root@node01 ~]# ps aux | grep httpd
      root      10706  0.0  0.4 247928  4996 ?        Ss   13:04   0:00 /sbin/httpd -DSTATUS -f /etc/httpd/conf/httpd.conf -c PidFile /var/run/httpd.pid
      apache    10707  0.0  0.4 247928  4368 ?        S    13:04   0:00 /sbin/httpd -DSTATUS -f /etc/httpd/conf/httpd.conf -c PidFile /var/run/httpd.pid
      apache    10708  0.0  0.4 247928  4392 ?        S    13:04   0:00 /sbin/httpd -DSTATUS -f /etc/httpd/conf/httpd.conf -c PidFile /var/run/httpd.pid
      apache    10709  0.0  0.4 247928  4368 ?        S    13:04   0:00 /sbin/httpd -DSTATUS -f /etc/httpd/conf/httpd.conf -c PidFile /var/run/httpd.pid
      apache    10710  0.0  0.4 247928  4432 ?        S    13:04   0:00 /sbin/httpd -DSTATUS -f /etc/httpd/conf/httpd.conf -c PidFile /var/run/httpd.pid
      apache    10711  0.0  0.4 247928  4392 ?        S    13:04   0:00 /sbin/httpd -DSTATUS -f /etc/httpd/conf/httpd.conf -c PidFile /var/run/httpd.pid

[root@node01 ~]# netstat -anptu | grep httpd
      tcp6       0      0 :::80                   :::*                    LISTEN      10706/httpd
      tcp6       0      0 :::443                  :::*                    LISTEN      10706/httpd



// 客户端访问测试
[root@client ~]# curl 192.168.175.100
    pcs web test

[root@node01 ~]# yum -y install elinks
[root@node01 ~]# elinks http://192.168.175.100   #使用 elinks 访问



----------------------------------------------------------------------------------------------------
测试资源转移:

// 方式一: 停止运行资源的当前节点的集群服务
[root@node01 ~]# pcs cluster stop node01
      node01: Stopping Cluster (pacemaker)...
      node01: Stopping Cluster (corosync)...

// 观察资源转移结果
[root@node01 ~]# ip a
    1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
        link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
        inet 127.0.0.1/8 scope host lo
           valid_lft forever preferred_lft forever
        inet6 ::1/128 scope host
           valid_lft forever preferred_lft forever
    2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
        link/ether 00:0c:29:d7:f9:47 brd ff:ff:ff:ff:ff:ff
        inet 192.168.175.101/24 brd 192.168.175.255 scope global ens33
           valid_lft forever preferred_lft forever   (观察, vip 已经不在 node01 上了)
        inet6 fe80::20c:29ff:fed7:f947/64 scope link
           valid_lft forever preferred_lft forever

[root@node02 ~]# pcs resource show
     Resource Group: webgroup
         web_vip  (ocf::heartbeat:IPaddr2): Started node02
         web_lvm  (ocf::heartbeat:LVM): Started node02
         web_fs (ocf::heartbeat:Filesystem):  Started node02
         web_service  (ocf::heartbeat:apache):  Started node02

[root@node02 ~]# ip a
        1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN qlen 1
            link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
            inet 127.0.0.1/8 scope host lo
               valid_lft forever preferred_lft forever
            inet6 ::1/128 scope host
               valid_lft forever preferred_lft forever
        2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP qlen 1000
            link/ether 00:0c:29:52:8e:39 brd ff:ff:ff:ff:ff:ff
            inet 192.168.175.102/24 brd 192.168.175.255 scope global ens33
               valid_lft forever preferred_lft forever
            inet 192.168.175.100/24 brd 192.168.175.255 scope global secondary ens33  <----观察
               valid_lft forever preferred_lft forever
            inet6 fe80::20c:29ff:fe52:8e39/64 scope link
               valid_lft forever preferred_lft forever

[root@node02 ~]# lvscan
      ACTIVE            '/dev/vg01/lv01' [<8.00 GiB] inherit  <-----观察
      ACTIVE            '/dev/centos/swap' [2.00 GiB] inherit
      ACTIVE            '/dev/centos/root' [17.80 GiB] inherit

[root@node02 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root xfs        18G  2.0G   16G  12% /
      devtmpfs                devtmpfs  478M     0  478M   0% /dev
      tmpfs                   tmpfs     489M   53M  436M  11% /dev/shm
      tmpfs                   tmpfs     489M  6.8M  482M   2% /run
      tmpfs                   tmpfs     489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1               xfs       197M  103M   95M  52% /boot
      tmpfs                   tmpfs      98M     0   98M   0% /run/user/0
      /dev/mapper/vg01-lv01   ext4      7.8G   36M  7.3G   1% /var/www/html  <-----观察


[root@node02 ~]# netstat -antpu | grep httpd
      tcp6       0      0 :::80                   :::*                    LISTEN      1804/httpd
      tcp6       0      0 :::443                  :::*                    LISTEN      1804/httpd

[root@client ~]# curl 192.168.175.100
    pcs web test


--------------------------------------------------
// 方式二: 设置某个节点为从节点

      [root@node01 ~]# pcs cluster start node01
            node01: Starting Cluster (corosync)...
            node01: Starting Cluster (pacemaker)...

      [root@node01 ~]# pcs cluster status
            Cluster Status:
             Stack: corosync
             Current DC: node02 (version 1.1.19-8.el7_6.4-c3c624ea3d) - partition with quorum
             Last updated: Fri Sep  6 13:21:51 2019
             Last change: Fri Sep  6 13:04:51 2019 by root via cibadmin on node01
             2 nodes configured
             4 resources configured

            PCSD Status:
              node01: Online
              node02: Online


      [root@node01 ~]# pcs resource show
           Resource Group: webgroup
               web_vip  (ocf::heartbeat:IPaddr2): Started node02
               web_lvm  (ocf::heartbeat:LVM): Started node02
               web_fs (ocf::heartbeat:Filesystem):  Started node02
               web_service  (ocf::heartbeat:apache):  Started node02


// 设置某个节点为从节点
[root@node01 ~]# pcs node standby node02  #设置 node02 为从节点

[root@node01 ~]# pcs resource show
     Resource Group: webgroup
         web_vip  (ocf::heartbeat:IPaddr2): Started node01
         web_lvm  (ocf::heartbeat:LVM): Started node01
         web_fs (ocf::heartbeat:Filesystem):  Started node01
         web_service  (ocf::heartbeat:apache):  Started node01









----------------------------------------------------------------------------------------------------
演示资源约束:

          [root@node01 ~]# pcs cluster status
                Cluster Status:
                 Stack: corosync
                 Current DC: node02 (version 1.1.19-8.el7_6.4-c3c624ea3d) - partition with quorum
                 Last updated: Fri Sep  6 13:38:21 2019
                 Last change: Fri Sep  6 13:23:01 2019 by root via cibadmin on node01
                 2 nodes configured
                 4 resources configured

                PCSD Status:
                  node01: Online
                  node02: Online


          [root@node01 ~]# pcs node attribute node02
                Node Attributes:
                 node02: standby=on

          [root@node01 ~]# pcs resource show
                 Resource Group: webgroup
                     web_vip  (ocf::heartbeat:IPaddr2): Started node01
                     web_lvm  (ocf::heartbeat:LVM): Started node01
                     web_fs (ocf::heartbeat:Filesystem):  Started node01
                     web_service  (ocf::heartbeat:apache):  Started node01

            // 取消 node02 的 standby 模式
            [root@node01 ~]# pcs node unstandby node02
            // 删除 集群资源
            [root@node01 ~]# pcs resource delete web_vip
            [root@node01 ~]# pcs resource delete web_lvm
            [root@node01 ~]# pcs resource delete web_fs
            [root@node01 ~]# pcs resource delete web_service



// 创建 ip 资源
[root@node01 ~]# pcs resource create web_vip ocf:heartbeat:IPaddr2 \
                    ip=192.168.175.100 \
                    cidr_netmask=24

[root@node01 ~]# pcs resource show
   web_vip  (ocf::heartbeat:IPaddr2): Started node01

// 创建 apache 资源
[root@node01 ~]# pcs resource create web_service ocf:heartbeat:apache \
                    configfile="/etc/httpd/conf/httpd.conf"

[root@node01 ~]# pcs resource show
       web_vip  (ocf::heartbeat:IPaddr2): Started node01
       web_service  (ocf::heartbeat:apache):  Started node02 <-----观察(此时资源 web_service 和 web_vip 不在同一节点上)

// 创建排列(colocation)约束,让 web_service 随 web_vip 同进同退
[root@node01 ~]# pcs constraint colocation add web_service with web_vip INFINITY

[root@node01 ~]# pcs resource show
       web_vip  (ocf::heartbeat:IPaddr2): Started node01
       web_service  (ocf::heartbeat:apache):  Started node01  <-----观察(web_service 跑到了 web_vip 的节点上)

      注: 约束和约束之间是有传递性, 即如果 C 随着  B 走, B 随着 A 走, 则 C 自然也会跟着 A 走, 即:
              A <----- B <-----C  =>  A <---- C
          所以不用 添加 C 随着 A 走 的约束


[root@node01 ~]# pcs constraint order web_vip then web_service
      Adding web_vip web_service (kind: Mandatory) (Options: first-action=start then-action=start)


// 创建顺序约束
[root@node01 ~]# pcs constraint order web_vip then web_service
      Adding web_vip web_service (kind: Mandatory) (Options: first-action=start then-action=start)

[root@node01 ~]# pcs constraint show
      Location Constraints:
      Ordering Constraints:
        start web_vip then start web_service (kind:Mandatory)
        Colocation Constraints:
          web_service with web_vip (score:INFINITY)
          Ticket Constraints:











----------------------------------------------------------------------------------------------------
其他一些指令 或 资料:

    重启集群
        pcs cluster stop --all
        pcs cluster start --all



相关文件:
/etc/corosync/corosync.conf
/var/log/cluster/corosync.log

    man corosync.conf
    rpm -ql corosync
    rpm -ql pacemaker



