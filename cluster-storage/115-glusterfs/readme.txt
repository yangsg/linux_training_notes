

GlusterFS


https://www.gluster.org/
https://docs.gluster.org/en/latest/
https://www.cnblogs.com/huangyanqi/p/8406534.html
https://blog.csdn.net/liuaigui/article/details/17331557
https://edu.51cto.com/lecturer/8205800.html

GlusterFS 架构:
    https://docs.gluster.org/en/latest/Quick-Start-Guide/Architecture/

    https://blog.51cto.com/11697257/2089478


----------------------------------------------------------------------------------------------------
一个重要的事件:
    glusterfs-3.9 中条带卷(Striped volumes)已经被废弃了, 官方推荐使用 sharding 作为替代方案

        https://lists.gluster.org/pipermail//gluster-devel/2016-August/050377.html
        https://www.linuxtechi.com/setup-glusterfs-storage-on-centos-7-rhel-7/

        原文:
            As *we* all are aware, striped volumes should not be used anymore. The
            replacement for this is sharding, available and stable since the latest
            3.7 releases and 3.8. Unfortunately users still create striped volumes,
            and some even write blog posts with examples.

            We should actively recommend users not to use striping anymore. This is
            a proposal to remove the striping xlator from the GlusterFS sources over
            the next two releases:

             - 3.9: prevent creation of new striped volumes, warn in the client logs
                    when striping is used

             - 3.10/4.0: remove the stripe xlator completely from the sources


    sharding 的更多信息:
          http://blog.gluster.org/introducing-shard-translator/
          https://staged-gluster-docs.readthedocs.io/en/release3.7.0beta1/Features/shard/

          https://blog.csdn.net/liuaigui/article/details/17314801
            Stripe 2.0
              GlusterFS处理超大文件的方法不够明智，一个文件大小可能增长超过一个brick容量。GlusterFS可以使用stripe进行条带化存储，
              但不够灵活，不可能混合存储条带化的文件和非条带化的文件。在大数据或hadoop应用下，超大文件是正常现象，
              这就限制了GlusterFS适用范围。4.0计划提出使用Shard xlator替换原先的条带，初始情况下所有文件都正常创建，
              当文件增长每超过预先设置的阈值(如64MB)，则按照特定 规则生成一个新文件，比如依据GFID和块索引号命名。
              这种模式下，所有数据块仍然按正常的Hash方式分布，扩展节点不需要按照之前的条带倍数进行，
              大文件的自修复拆分成多个较小文件在多个节点之间并发进行，数据块文件名命名模式不受重命名和硬链接影响。


    关于DHT:
          https://docs.gluster.org/en/latest/Quick-Start-Guide/Architecture/
          https://docs.gluster.org/en/latest/Quick-Start-Guide/Architecture/#dhtdistributed-hash-table-translator
          https://staged-gluster-docs.readthedocs.io/en/release3.7.0beta1/Features/dht/








----------------------------------------------------------------------------------------------------





    ----------------------------------------------------------------------------------------
    |                                                                                      |
    ----------------------------------------------------------------------------------------


-------------------------------------------|--------------------------------------------------------
                                           |
                                           | 挂载 (fuse, nfs)
                                           |
                                           |
      +-------------------------------------------------------------------------------------+
|-----|                              volume                                                 |----|
|     |                                                                                     |    |
|     +-------------------------------------------------------------------------------------+    |
|                                                                                                |
|                                                                                                |
|                                                                                                |
|      +--------+            +--------+             +--------+           +--------+              |
|      |        |            |        |             |        |           |        |              |
|      |        |------+     |        |------+      |        |------+    |        |------+       |
|      |        | brick|     |        | brick|      |        | brick|    |        | brick|       |
|      +--------+------+     +--------+------+      +--------+------+    +--------+------+       |
|                                                                                                |
|------------------------------------------------------------------------------------------------|





----------------------------------------------------------------------------------------------------
glusterfs分布式文件系统
  应用场景： 大数据存储、云平台数据存储
  glusterfs用于实现分布式存储, 应用于云平台数据的存储、视频流数据存储、集群的共享存储


glusterfs基本概念
  1、brick  集群中节点提供的挂载点目录
  2、volume  卷   提供给前端应用服务器的虚拟存储空间


glusterfs的特性：
  1.  PB级容量，数千个节点
  2.  高可用性
  3.  提升读/写性能
  4.  基于文件系统级别共享
  5.  无metadata(元数据)的存储方式, 使用弹性hash算法实现数据的定位
  6.  支持多种挂载方式[FUSE, NFS]


----------------------------------------------------------------------------------------------------
示例:

    node01 192.168.175.101
    node02 192.168.175.102
    node03 192.168.175.103
    node04 192.168.175.104
    node04 192.168.175.105

    client 192.168.175.200


     注: 如上 每个 node 添加了额外的 5个 2G 大小的硬盘, 方便练习使用

----------------------------------------------------------------------------------------------------
部署glusterfs集群
    1、项目环境准备

        1) 主机名称、IP地址
        2) 解析主机名
        3) 防火墙、SELinux
    4) ntp时间同步
    5) ssh密钥远程
    6) 配置glusterfs源




----------------------------------------------------------------------------------------------------
// 配置所有主机的ssh免密登录
[root@node01 ~]# ssh-keygen -t rsa
        Generating public/private rsa key pair.
        Enter file in which to save the key (/root/.ssh/id_rsa): <======= 直接回车
        Created directory '/root/.ssh'.
        Enter passphrase (empty for no passphrase): <======= 直接回车
        Enter same passphrase again: <======= 直接回车
        Your identification has been saved in /root/.ssh/id_rsa.
        Your public key has been saved in /root/.ssh/id_rsa.pub.
        The key fingerprint is:
        SHA256:pkclDMevMt4Kx6PVoJlXdN6UsnEhUh2CWbudCP+2ENE root@node01
        The key's randomart image is:
        +---[RSA 2048]----+
        |      ..o==.o.   |
        |       ++. =.o   |
        |        =.B E    |
        |       . B.% .   |
        |      . S.B +    |
        |     =oB.  o     |
        |    =.B+o . o    |
        |     *.o.  o .   |
        |    . ..    .    |
        +----[SHA256]-----+


[root@node01 ~]# tree .ssh
        .ssh
        ├── id_rsa      <-------
        └── id_rsa.pub  <-------



[root@node01 ~]# ssh-copy-id root@192.168.175.101

[root@node01 ~]# tree .ssh/
        .ssh/
        ├── authorized_keys  <------
        ├── id_rsa
        ├── id_rsa.pub
        └── known_hosts

[root@node01 ~]# scp -r /root/.ssh/ root@192.168.175.102:/root/
[root@node01 ~]# scp -r /root/.ssh/ root@192.168.175.103:/root/
[root@node01 ~]# scp -r /root/.ssh/ root@192.168.175.104:/root/
[root@node01 ~]# scp -r /root/.ssh/ root@192.168.175.105:/root/
[root@node01 ~]# scp -r /root/.ssh/ root@192.168.175.200:/root/


[root@node01 ~]# for i in 101 102 103 104 105 200; do ssh 192.168.175.$i hostname; done
        node01
        node02
        node03
        node04
        node05
        client

[root@node01 ~]# vim /etc/hosts
      192.168.175.101   node01
      192.168.175.102   node02
      192.168.175.103   node03
      192.168.175.104   node04
      192.168.175.105   node05

[root@node01 ~]# for i in 101 102 103 104 105;
> do
> scp /etc/hosts  root@192.168.175.$i:/etc/hosts
> done


// 对如上的 scp 拷贝操作 确认一下
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'echo $(md5sum /etc/hosts) --- $(hostname)'
> done


// 确认 时间 是否 同步(一致)
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'echo $(date) --- $(hostname)' &
> done 2> /dev/null; wait 2> /dev/null


----------------------------------------------------------------------------------------------------
在集群所有节点上安装glusterfs服务器端软件 ，启动glusterd服务

//  安装 glusterfs server端 相关软件
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'yum -y install centos-release-gluster'  #安装 glusterfs-server 所在的 yum 源
> ssh root@192.168.175.$i 'yum -y install glusterfs-server glusterfs-fuse glusterfs'
> done


// 查看确认一下 安装结果
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'echo $(hostname)------------------'
> ssh root@192.168.175.$i 'rpm -q glusterfs-server glusterfs-fuse glusterfs'
> done

        node01------------------
        glusterfs-server-6.5-1.el7.x86_64
        glusterfs-fuse-6.5-1.el7.x86_64
        glusterfs-6.5-1.el7.x86_64
         略 略 略 略


// 启动 glusterd 服务 并设置为开机自启
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'systemctl start glusterd'
> ssh root@192.168.175.$i 'systemctl enable glusterd'
> done


// 查看观察一下 启动结果信息
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'echo $(hostname) ------------------------'
> ssh root@192.168.175.$i 'systemctl is-active glusterd'
> ssh root@192.168.175.$i 'systemctl is-enabled glusterd'
> done


// 查看观察一下 启动结果信息(详细) (注: 某些服务即使能够启动, 可能启动起来也可能包含错误信息, 所以这里小心起见, 再看一看详细信息)
[root@node01 ~]# for i in 101 102 103 104 105;
> do
> ssh root@192.168.175.$i 'echo $(hostname) ------------------------'
> ssh root@192.168.175.$i 'systemctl status glusterd'
> done




----------------------------------------------------------------------------------------------------
// 在 client端 安装 glusterfs 客户端相关的软件
[root@client ~]# yum -y install centos-release-gluster    #为了与服务端的 版本保持一致, 这里从 centos-release-gluster 对应的源下载安装
[root@client ~]# yum -y install glusterfs glusterfs-fuse

[root@client ~]# rpm -q glusterfs glusterfs-fuse
      glusterfs-6.5-1.el7.x86_64
      glusterfs-fuse-6.5-1.el7.x86_64


----------------------------------------------------------------------------------------------------
创建gluster集群【任意节点】


// 查看 一下 命令 gluster 的简要帮助(详细帮助见 `man gluster`)
[root@node01 ~]# gluster --help
       peer help                - display help for peer commands
       volume help              - display help for volume commands
       volume bitrot help       - display help for volume bitrot commands
       volume quota help        - display help for volume quota commands
       volume tier help         - display help for volume tier commands
       snapshot help            - display help for snapshot commands
       global help              - list global commands


// 查看 一下 gluster 子命令 peer 的简要帮助
[root@node01 ~]# gluster peer help

        gluster peer commands
        ======================

        peer detach { <HOSTNAME> | <IP-address> } [force] - detach peer specified by <HOSTNAME>
        peer help - display help for peer commands
        peer probe { <HOSTNAME> | <IP-address> } - probe peer specified by <HOSTNAME>
        peer status - list status of peers
        pool list - list all the nodes in the pool (including localhost)



[root@node01 ~]# gluster peer probe node02
    peer probe: success.

[root@node01 ~]# gluster peer probe node03
    peer probe: success.

[root@node01 ~]# gluster peer probe node04
    peer probe: success.

[root@node01 ~]# gluster peer probe node05
    peer probe: success.


// 在 node01 上观察一下 peer 状态信息 (即 node01 的 peer 的信息)
[root@node01 ~]# gluster peer status
            Number of Peers: 4

            Hostname: node02
            Uuid: 0250693e-87d3-4ddc-98ba-dd50bd15d7c1
            State: Peer in Cluster (Connected)

            Hostname: node03
            Uuid: a20baac0-f9fa-4a6a-9dbe-0d0c6e0f492b
            State: Peer in Cluster (Connected)

            Hostname: node04
            Uuid: fdadbcf9-0220-474e-ae96-531042e521fa
            State: Peer in Cluster (Connected)

            Hostname: node05
            Uuid: 85f4567b-5016-492c-bdaa-b745653e80ac
            State: Peer in Cluster (Connected)


// 在 node03 上观察一下 peer 状态信息 (即 node03 的 peer 的信息)
[root@node03 ~]# gluster peer status
            Number of Peers: 4

            Hostname: node01
            Uuid: b13e7713-59ec-43ba-a805-221ea22713d8
            State: Peer in Cluster (Connected)

            Hostname: node02
            Uuid: 0250693e-87d3-4ddc-98ba-dd50bd15d7c1
            State: Peer in Cluster (Connected)

            Hostname: node04
            Uuid: fdadbcf9-0220-474e-ae96-531042e521fa
            State: Peer in Cluster (Connected)

            Hostname: node05
            Uuid: 85f4567b-5016-492c-bdaa-b745653e80ac
            State: Peer in Cluster (Connected)


















----------------------------------------------------------------------------------------------------
Types of Volumes (Glusterfs 卷的类型)

      https://docs.gluster.org/en/latest/Quick-Start-Guide/Architecture/

Distributed Glusterfs Volume(分布式卷)
Replicated Glusterfs Volume(复制卷)
Striped Glusterfs Volume (条带卷/条纹卷)  (注: glusterfs 从 3.9 版本开始被废弃了, 推荐的替代方案是 sharding)
Distributed Replicated Glusterfs Volume (分布复制卷) <-----------较常用(在较新版本中可启用 sharding 特性)


----------------------------------------------------------------------------------------------------
分布式卷

      以整个文件为单位，不同的文件分散存储在不同的brick上，适用于存储大量小文件
      无brick数量的限制
      默认类型
      卷容量 === 所有brick容量之和
      提升数据读写速度，无可靠性


// 查看一下 gluster 的子命令 volume 的简要帮助
[root@client ~]# gluster volume help  | less

    gluster volume commands
    ========================

    volume add-brick <VOLNAME> [<stripe|replica> <COUNT> [arbiter <COUNT>]] <NEW-BRICK> ... [force] - add brick to volume <VOLNAME>
    volume barrier <VOLNAME> {enable|disable} - Barrier/unbarrier file operations on a volume
    volume clear-locks <VOLNAME> <path> kind {blocked|granted|all}{inode [range]|entry [basename]|posix [range]} - Clear locks held on path
    volume create <NEW-VOLNAME> [stripe <COUNT>] [replica <COUNT> [arbiter <COUNT>]] [disperse [<COUNT>]] [disperse-data <COUNT>] [redundancy <COUNT>] [transport <tcp|rdma|tcp,rdma>] <NEW-BRICK>... [force] - create a new volume of specified type with mentioned bricks
    volume delete <VOLNAME> - delete volume specified by <VOLNAME>
    volume get <VOLNAME|all> <key|all> - Get the value of the all options or given option for volume <VOLNAME> or all option. gluster volume get all all is to get all global options
    volume heal <VOLNAME> [enable | disable | full |statistics [heal-count [replica <HOSTNAME:BRICKNAME>]] |info [summary | split-brain] |split-brain {bigger-file <FILE> | latest-mtime <FILE> |source-brick <HOSTNAME:BRICKNAME> [<FILE>]} |granular-entry-heal {enable | disable}] - self-heal commands on volume specified by <VOLNAME>
    volume help - display help for volume commands
    volume info [all|<VOLNAME>] - list information of all volumes
    volume list - list all volumes in cluster
    volume log <VOLNAME> rotate [BRICK] - rotate the log file for corresponding volume/brick
    volume log rotate <VOLNAME> [BRICK] - rotate the log file for corresponding volume/brick NOTE: This is an old syntax, will be deprecated from next release.
    volume profile <VOLNAME> {start|info [peek|incremental [peek]|cumulative|clear]|stop} [nfs] - volume profile operations
    volume rebalance <VOLNAME> {{fix-layout start} | {start [force]|stop|status}} - rebalance operations
    volume remove-brick <VOLNAME> [replica <COUNT>] <BRICK> ... <start|stop|status|commit|force> - remove brick from volume <VOLNAME>
    volume replace-brick <VOLNAME> <SOURCE-BRICK> <NEW-BRICK> {commit force} - replace-brick operations
    volume reset <VOLNAME> [option] [force] - reset all the reconfigured options
    volume reset-brick <VOLNAME> <SOURCE-BRICK> {{start} | {<NEW-BRICK> commit}} - reset-brick operations
    volume set <VOLNAME> <KEY> <VALUE> - set options for volume <VOLNAME>
    volume set <VOLNAME> group  <GROUP> - This option can be used for setting multiple pre-defined volume optionswhere group_name is a file under /var/lib/glusterd/groups containing onekey, value pair per line
    volume start <VOLNAME> [force] - start volume specified by <VOLNAME>
    volume statedump <VOLNAME> [[nfs|quotad] [all|mem|iobuf|callpool|priv|fd|inode|history]... | [client <hostname:process-id>]] - perform statedump on bricks
    volume status [all | <VOLNAME> [nfs|shd|<BRICK>|quotad|tierd]] [detail|clients|mem|inode|fd|callpool|tasks|client-list] - display status of all or specified volume(s)/brick
    volume stop <VOLNAME> [force] - stop volume specified by <VOLNAME>
    volume sync <HOSTNAME> [all|<VOLNAME>] - sync the volume information from a peer
    volume top <VOLNAME> {open|read|write|opendir|readdir|clear} [nfs|brick <brick>] [list-cnt <value>] |
    volume top <VOLNAME> {read-perf|write-perf} [bs <size> count <count>] [brick <brick>] [list-cnt <value>] - volume top operations

----------------------------------------------------------------------------------------------------
分布式卷的示例演示:

        +-----------------------+
        |   node01(/dev/sdb)    |=====> gluster volume(data_volume01_distributed) <------ client(/testdir01_distributed)
        |   node02(/dev/sdb)    |
        +-----------------------+





[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
        └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
      /dev/sdb                      8:16   0    2G  0 disk  <---------
      /dev/sdc                      8:32   0    2G  0 disk  <---------
      /dev/sdd                      8:48   0    2G  0 disk  <---------
      /dev/sde                      8:64   0    2G  0 disk  <---------
      /dev/sdf                      8:80   0    2G  0 disk  <---------
      /dev/sr0                     11:0    1 1024M  0 rom


[root@node01 ~]# mkdir /data01_distributed
[root@node01 ~]# mkfs.ext4 /dev/sdb
[root@node01 ~]# vim /etc/fstab
      /dev/sdb  /data01_distributed                   ext4    defaults        0 0

[root@node01 ~]# mount -a
[root@node01 ~]# df -hT | grep /dev/sdb
    /dev/sdb                ext4      2.0G  6.0M  1.8G   1% /data01_distributed <-----观察(大小 2G)


[root@node02 ~]# mkdir /data01_distributed
[root@node02 ~]# mkfs.ext4 /dev/sdb
[root@node01 ~]# vim /etc/fstab
      /dev/sdb  /data01_distributed                   ext4    defaults        0 0

[root@node02 ~]# mount -a
[root@node02 ~]# df -hT | grep /dev/sdb
      /dev/sdb                ext4      2.0G  6.0M  1.8G   1% /data01_distributed <-----观察(大小 2G)



// 查看一下 创建 volume 的语法
[root@node01 ~]# gluster volume help | grep create
      volume create <NEW-VOLNAME> [stripe <COUNT>] [replica <COUNT> [arbiter <COUNT>]] [disperse [<COUNT>]] [disperse-data <COUNT>] [redundancy <COUNT>] [transport <tcp|rdma|tcp,rdma>] <NEW-BRICK>... [force] - create a new volume of specified type with mentioned bricks


// 创建分布式卷
// 注: 创建卷的操作可以在 集群中的任意 node 上执行, 创建出来的 volume 属于集群而不属于机器
[root@node01 ~]# gluster volume create data_volume01_distributed \
                      node01:/data01_distributed/br1 \
                      node02:/data01_distributed/br1

      volume create: data_volume01_distributed: success: please start the volume to access data


// 启动卷
[root@node01 ~]# gluster volume start data_volume01_distributed
      volume start: data_volume01_distributed: success


// 列出集群中的所有卷
[root@node01 ~]# gluster volume list
      data_volume01_distributed



// 查看 卷 data_volume01_distributed 的信息
[root@node01 ~]# gluster volume info data_volume01_distributed

      Volume Name: data_volume01_distributed
      Type: Distribute  <-----观察
      Volume ID: f43bc40d-0e15-4f88-8e76-fe3ea4326137
      Status: Started
      Snapshot Count: 0
      Number of Bricks: 2
      Transport-type: tcp
      Bricks:
      Brick1: node01:/data01_distributed/br1
      Brick2: node02:/data01_distributed/br1
      Options Reconfigured:
      transport.address-family: inet
      nfs.disable: on


// 客户端使用卷
[root@client ~]# mkdir /testdir01_distributed

// 挂载卷
// 注: 因为 volume 属于集群而非属于机器, 所以可以通过任意一个 node 挂载
[root@client ~]# mount -t glusterfs node01:/data_volume01_distributed  /testdir01_distributed
[root@client ~]# df -hT
      Filesystem                        Type            Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root           xfs              18G  1.9G   16G  11% /
      devtmpfs                          devtmpfs        478M     0  478M   0% /dev
      tmpfs                             tmpfs           489M     0  489M   0% /dev/shm
      tmpfs                             tmpfs           489M  6.8M  482M   2% /run
      tmpfs                             tmpfs           489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1                         xfs             197M  103M   95M  53% /boot
      tmpfs                             tmpfs            98M     0   98M   0% /run/user/0
      node01:/data_volume01_distributed fuse.glusterfs  3.9G   52M  3.6G   2% /testdir01_distributed  <------观察(大小3.9G ~ 2G + 2G)



[root@client ~]# vim /etc/fstab
      node01:/data_volume01_distributed  /testdir01_distributed  glusterfs   defaults,_netdev        0 0

[root@client ~]# umount /testdir01_distributed/
[root@client ~]# df -hT
      Filesystem                        Type            Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root           xfs              18G  1.9G   16G  11% /
      devtmpfs                          devtmpfs        478M     0  478M   0% /dev
      tmpfs                             tmpfs           489M     0  489M   0% /dev/shm
      tmpfs                             tmpfs           489M  6.8M  482M   2% /run
      tmpfs                             tmpfs           489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1                         xfs             197M  103M   95M  53% /boot
      tmpfs                             tmpfs            98M     0   98M   0% /run/user/0
      node01:/data_volume01_distributed fuse.glusterfs  3.9G   52M  3.6G   2% /testdir01_distributed  <----观察



// 创建文件查看分布式卷的 效果
[root@client ~]# touch /testdir01_distributed/{1..10}.txt

// 在 client 端查看
[root@client ~]# ls /testdir01_distributed/
        10.txt  1.txt  2.txt  3.txt  4.txt  5.txt  6.txt  7.txt  8.txt  9.txt <---观察(从client的角度看,所有文件存储在一个地方)

// 在 node01 上查看
[root@node01 ~]# ls /data01_distributed/br1/
      4.txt  8.txt  9.txt  <--观察(从分布式卷实现的角度看, 多个文件时按文件为单位分散存储在不同的 bricks 中的)

// 在 node02 上查看
[root@node02 ~]# ls /data01_distributed/br1/
      10.txt  1.txt  2.txt  3.txt  5.txt  6.txt  7.txt <-----观察








----------------------------------------------------------------------------------------------------
复制卷


      每个文件会被复制为brick数量份，分散存储
      创建时需要使用参数replica指定文件被复制的份数，该数字要和brick数量一致
      提供文件可靠性






----------------------------------------------------------------------------------------------------
复制卷的示例演示:

        +-----------------------+
        |   node01(/dev/sdc)    |=====> gluster volume(data_volume02_replicated) <------ client(/testdir02_replicated)
        |   node02(/dev/sdc)    |
        +-----------------------+

        注: 本示例中包含了 某些错误的 案例


[root@node01 ~]# lsblk -p
      NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
      /dev/sda                      8:0    0   20G  0 disk
      ├─/dev/sda1                   8:1    0  200M  0 part /boot
      └─/dev/sda2                   8:2    0 19.8G  0 part
        ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
          └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
          /dev/sdb                      8:16   0    2G  0 disk /data01_distributed
          /dev/sdc                      8:32   0    2G  0 disk
          /dev/sdd                      8:48   0    2G  0 disk
          /dev/sde                      8:64   0    2G  0 disk
          /dev/sdf                      8:80   0    2G  0 disk
          /dev/sr0                     11:0    1 1024M  0 rom


[root@node01 ~]# mkdir /data02_replicated
[root@node01 ~]# mkfs.ext4 /dev/sdc


[root@node01 ~]# vim /etc/fstab
    /dev/sdc  /data02_replicated                   ext4    defaults        0 0


[root@node01 ~]# mount -a
[root@node01 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sdc                ext4      2.0G  6.0M  1.8G   1% /data02_replicated  <----观察(大小为2G)


[root@node02 ~]# mkdir /data02_replicated
[root@node02 ~]# mkfs.ext4 /dev/sdc

[root@node02 ~]# vim /etc/fstab
    /dev/sdc  /data02_replicated                   ext4    defaults        0 0


// 注: 这里为了演示一个 错误案例, 所以并没有执行  `mount -a` 命令执行挂载操作


// 查看一下 创建 volume 的语法
[root@node01 ~]# gluster volume help | grep create
      volume create <NEW-VOLNAME> [stripe <COUNT>] [replica <COUNT> [arbiter <COUNT>]] [disperse [<COUNT>]] [disperse-data <COUNT>] [redundancy <COUNT>] [transport <tcp|rdma|tcp,rdma>] <NEW-BRICK>... [force] - create a new volume of specified type with mentioned bricks

[root@node01 ~]# gluster volume create data_volume02_replicated  replica 2 \
> node01:/data02_replicated/br1 \
> node02:/data02_replicated/br1
Replica 2 volumes are prone to split-brain. Use Arbiter or Replica 3 to avoid this. See: http://docs.gluster.org/en/latest/Administrator%20Guide/Split%20brain%20and%20ways%20to%20deal%20with%20it/.
Do you still want to continue?
 (y/n) y
volume create: data_volume02_replicated: failed: Staging failed on node02. Error: The brick node02:/data02_replicated/br1 is being created in the root partition. It is recommended that you don't use the system's root partition for storage backend. Or use 'force' at the end of the command if you want to override this behavior. <----error 信息

        注: 这里的错误提示 'The brick node02:/data02_replicated/br1 is being created in the root partition.' 是由
            node02 中未将 /dev/sdc 挂载到目录 /data02_replicated 而引起的

    注: 如上 脑裂的 信息见  https://docs.gluster.org/en/latest/Administrator%20Guide/Split%20brain%20and%20ways%20to%20deal%20with%20it/


// 在 node02 上挂载 /dev/sdc 到目录 /data02_replicated
[root@node02 ~]# mount -a
[root@node02 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sdc                ext4      2.0G  6.0M  1.8G   1% /data02_replicated


[root@node01 ~]# gluster volume create data_volume02_replicated  replica 2 \
> node01:/data02_replicated/br1 \
> node02:/data02_replicated/br1
Replica 2 volumes are prone to split-brain. Use Arbiter or Replica 3 to avoid this. See: http://docs.gluster.org/en/latest/Administrator%20Guide/Split%20brain%20and%20ways%20to%20deal%20with%20it/.
Do you still want to continue?
 (y/n) y <====== 输入y
volume create: data_volume02_replicated: failed: /data02_replicated/br1 is already part of a volume <----error 信息


[root@node01 ~]# ls /data02_replicated/
      br1  lost+found

// 删除目录 /data02_replicated/ 下的 br1 目录
[root@node01 ~]# rm -rf /data02_replicated/br1/


// 创建 复制卷
//  注: 创建复制卷时 复制的份数要与 bricks 的个数保持一致
//  注: 创建卷的操作可以在 集群中的任意 node 上执行, 创建出来的 volume 属于集群而不属于机器
[root@node01 ~]# gluster volume create data_volume02_replicated  replica 2 \
                      node01:/data02_replicated/br1 \
                      node02:/data02_replicated/br1

Replica 2 volumes are prone to split-brain. Use Arbiter or Replica 3 to avoid this. See: http://docs.gluster.org/en/latest/Administrator%20Guide/Split%20brain%20and%20ways%20to%20deal%20with%20it/.
Do you still want to continue?
 (y/n) y <====== 输入y
volume create: data_volume02_replicated: success: please start the volume to access data

// 启动卷
[root@node01 ~]# gluster volume start data_volume02_replicated
      volume start: data_volume02_replicated: success


// 列出集群中的卷
[root@node01 ~]# gluster volume list
      data_volume01_distributed
      data_volume02_replicated


[root@node01 ~]# gluster volume info data_volume02_replicated

      Volume Name: data_volume02_replicated
      Type: Replicate  <------------观察
      Volume ID: f686095e-f0d8-4b0d-9172-5ee52898d880
      Status: Started
      Snapshot Count: 0
      Number of Bricks: 1 x 2 = 2
      Transport-type: tcp
      Bricks:
      Brick1: node01:/data02_replicated/br1
      Brick2: node02:/data02_replicated/br1
      Options Reconfigured:
      transport.address-family: inet
      nfs.disable: on
      performance.client-io-threads: off




// 客户端使用卷
[root@client ~]# mkdir /testdir02_replicated

// 挂载卷
// 注: 因为 volume 属于集群而非属于机器, 所以可以通过任意一个 node 挂载
[root@client ~]# vim /etc/fstab
      node01:/data_volume02_replicated  /testdir02_replicated  glusterfs   defaults,_netdev        0 0

[root@client ~]# mount -a
[root@client ~]# df -hT
      Filesystem                        Type            Size  Used Avail Use% Mounted on
      /dev/mapper/centos-root           xfs              18G  1.9G   16G  11% /
      devtmpfs                          devtmpfs        478M     0  478M   0% /dev
      tmpfs                             tmpfs           489M     0  489M   0% /dev/shm
      tmpfs                             tmpfs           489M  6.8M  482M   2% /run
      tmpfs                             tmpfs           489M     0  489M   0% /sys/fs/cgroup
      /dev/sda1                         xfs             197M  103M   95M  53% /boot
      tmpfs                             tmpfs            98M     0   98M   0% /run/user/0
      node01:/data_volume01_distributed fuse.glusterfs  3.9G   52M  3.6G   2% /testdir01_distributed
      node01:/data_volume02_replicated  fuse.glusterfs  2.0G   26M  1.8G   2% /testdir02_replicated  <----观察(大小 2G=2G=2G)


// 创建文件查看复制式卷的 效果
[root@client ~]# for i in {1..5};
> do
>   head -c 1M < /dev/urandom > /testdir02_replicated/${i}.txt
> done

[root@client ~]# ls /testdir02_replicated
      1.txt  2.txt  3.txt  4.txt  5.txt

// 在 client 端查看
[root@client ~]# for i in {1..5};
> do
>   md5sum /testdir02_replicated/${i}.txt
> done
        424625b1fc84745e0ea55192bcbca88d  /testdir02_replicated/1.txt
        dadd6fe95c2568d7abc0a98a0ba71c09  /testdir02_replicated/2.txt
        38adf5f8f7fd3e8da5932eaf50f975f7  /testdir02_replicated/3.txt
        cc5d40637e9f74e6166d95ee9b16268d  /testdir02_replicated/4.txt
        8cb172f940dd95e4d9f64fab9c563049  /testdir02_replicated/5.txt


[root@node01 ~]# ls /data02_replicated/br1/
        1.txt  2.txt  3.txt  4.txt  5.txt

// 在 node01 上查看
[root@node01 ~]# for i in {1..5};
> do
>   md5sum /data02_replicated/br1/${i}.txt
> done
        424625b1fc84745e0ea55192bcbca88d  /data02_replicated/br1/1.txt
        dadd6fe95c2568d7abc0a98a0ba71c09  /data02_replicated/br1/2.txt
        38adf5f8f7fd3e8da5932eaf50f975f7  /data02_replicated/br1/3.txt
        cc5d40637e9f74e6166d95ee9b16268d  /data02_replicated/br1/4.txt
        8cb172f940dd95e4d9f64fab9c563049  /data02_replicated/br1/5.txt


[root@node02 ~]# ls /data02_replicated/br1/
        1.txt  2.txt  3.txt  4.txt  5.txt

[root@node02 ~]# for i in {1..5};
> do
>   md5sum /data02_replicated/br1/${i}.txt
> done
        424625b1fc84745e0ea55192bcbca88d  /data02_replicated/br1/1.txt
        dadd6fe95c2568d7abc0a98a0ba71c09  /data02_replicated/br1/2.txt
        38adf5f8f7fd3e8da5932eaf50f975f7  /data02_replicated/br1/3.txt
        cc5d40637e9f74e6166d95ee9b16268d  /data02_replicated/br1/4.txt
        8cb172f940dd95e4d9f64fab9c563049  /data02_replicated/br1/5.txt


            可以看到, 观察的结果 不论是在  volume 中(通过client观察),
            还是在 brick中(通过node01 和 node02 观察) 都是相同的,
            这说明了 每个文件会被复制为brick数量份，分散存储











----------------------------------------------------------------------------------------------------
条带卷

    提升读写性能，适用于大文件的存储
    创建时通过stripe的参数指定文件被条带的次数, 该数量要和brick数量一致







----------------------------------------------------------------------------------------------------
条带卷的示例演示:

      注: 因为该 glusterfs 版本不支持 条带卷 特性,
          所以该示例无法成功完成, 所以应该直接忽略


        +-----------------------+
        |   node01(/dev/sdd)    |=====> gluster volume(data_volume03_striped) <------ client(/testdir03_striped)
        |   node02(/dev/sdd)    |
        +-----------------------+




[root@node01 ~]# lsblk -p
        NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
        /dev/sda                      8:0    0   20G  0 disk
        ├─/dev/sda1                   8:1    0  200M  0 part /boot
        └─/dev/sda2                   8:2    0 19.8G  0 part
          ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
          └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
        /dev/sdb                      8:16   0    2G  0 disk /data01_distributed
        /dev/sdc                      8:32   0    2G  0 disk /data02_replicated
        /dev/sdd                      8:48   0    2G  0 disk  <------------观察
        /dev/sde                      8:64   0    2G  0 disk
        /dev/sdf                      8:80   0    2G  0 disk
        /dev/sr0                     11:0    1 1024M  0 rom




[root@node01 ~]# mkdir /data03_striped
[root@node01 ~]# mkfs.ext4 /dev/sdd

[root@node01 ~]# vim /etc/fstab
      /dev/sdd  /data03_striped                   ext4    defaults        0 0

[root@node01 ~]# mount -a
[root@node01 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sdd                ext4      2.0G  6.0M  1.8G   1% /data03_striped  <-----观察(大小2G)


[root@node02 ~]# mkdir /data03_striped
[root@node02 ~]# mkfs.ext4 /dev/sdd
[root@node02 ~]# vim /etc/fstab
      /dev/sdd  /data03_striped                   ext4    defaults        0 0


[root@node02 ~]# mount -a
[root@node02 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sdd                ext4      2.0G  6.0M  1.8G   1% /data03_striped  <-----观察(大小2G)


// 查看一下 创建 volume 的语法
[root@node01 ~]# gluster volume help | grep create
      volume create <NEW-VOLNAME> [stripe <COUNT>] [replica <COUNT> [arbiter <COUNT>]] [disperse [<COUNT>]] [disperse-data <COUNT>] [redundancy <COUNT>] [transport <tcp|rdma|tcp,rdma>] <NEW-BRICK>... [force] - create a new volume of specified type with mentioned bricks













----------------------------------------------------------------------------------------------------
分布复制卷 Distributed Replicated Glusterfs Volume

  存储大量的小文件，并提升文件的可靠性
  brick数量是replica参数的复制数的整倍数

      https://docs.gluster.org/en/latest/Quick-Start-Guide/Architecture/


----------------------------------------------------------------------------------------------------
分布复制卷示例:


        +----------------------------+
        |  +----------------+        |
        |  |node01(/dev/sde)|        |=====> gluster volume(data_volume04_distributed_replicated) <------ client(/testdir04_distributed_replicated)
        |  |node02(/dev/sde)|        |
        |  +----------------+        |
        |  +----------------+        |  (其中, node01和node02的/dev/sde互为复制brick,node03和node04的/dev/sde互为复制brick)
        |  |node03(/dev/sde)|        |
        |  |node04(/dev/sde)|        |
        |  +----------------+        |
        +----------------------------+


    注: 分布式复制卷中, 顺序也是很重要的, 因为 毗连(adjacent) 的 bricks 互为彼此的复制(replicas)
            adjacent bricks become replicas of each other.



[root@node01 ~]# lsblk -p
        NAME                        MAJ:MIN RM  SIZE RO TYPE MOUNTPOINT
        /dev/sda                      8:0    0   20G  0 disk
        ├─/dev/sda1                   8:1    0  200M  0 part /boot
        └─/dev/sda2                   8:2    0 19.8G  0 part
          ├─/dev/mapper/centos-root 253:0    0 17.8G  0 lvm  /
          └─/dev/mapper/centos-swap 253:1    0    2G  0 lvm  [SWAP]
        /dev/sdb                      8:16   0    2G  0 disk /data01_distributed
        /dev/sdc                      8:32   0    2G  0 disk /data02_replicated
        /dev/sdd                      8:48   0    2G  0 disk /data03_striped
        /dev/sde                      8:64   0    2G  0 disk
        /dev/sdf                      8:80   0    2G  0 disk
        /dev/sr0                     11:0    1 1024M  0 rom




[root@node01 ~]# mkdir /data04_distributed_replicated
[root@node01 ~]# mkfs.ext4 /dev/sde

[root@node01 ~]# vim /etc/fstab
      /dev/sde  /data04_distributed_replicated                   ext4    defaults        0 0

[root@node01 ~]# mount -a
[root@node01 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sde                ext4      2.0G  6.0M  1.8G   1% /data04_distributed_replicated  <-----观察(大小2G)


[root@node02 ~]# mkdir /data04_distributed_replicated
[root@node02 ~]# mkfs.ext4 /dev/sde

[root@node02 ~]# vim /etc/fstab
      /dev/sde  /data04_distributed_replicated                   ext4    defaults        0 0

[root@node02 ~]# mount -a
[root@node02 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sde                ext4      2.0G  6.0M  1.8G   1% /data04_distributed_replicated  <-----观察(大小2G)



[root@node03 ~]# mkdir /data04_distributed_replicated
[root@node03 ~]# mkfs.ext4 /dev/sde

[root@node03 ~]# vim /etc/fstab
      /dev/sde  /data04_distributed_replicated                   ext4    defaults        0 0

[root@node03 ~]# mount -a
[root@node03 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sde                ext4      2.0G  6.0M  1.8G   1% /data04_distributed_replicated  <-----观察(大小2G)



[root@node04 ~]# mkdir /data04_distributed_replicated
[root@node04 ~]# mkfs.ext4 /dev/sde

[root@node04 ~]# vim /etc/fstab
      /dev/sde  /data04_distributed_replicated                   ext4    defaults        0 0

[root@node04 ~]# mount -a
[root@node04 ~]# df -hT
      Filesystem              Type      Size  Used Avail Use% Mounted on
      /dev/sde                ext4      2.0G  6.0M  1.8G   1% /data04_distributed_replicated  <-----观察(大小2G)


// 查看一下 创建 volume 的语法
[root@node01 ~]# gluster volume help | grep create
      volume create <NEW-VOLNAME> [stripe <COUNT>] [replica <COUNT> [arbiter <COUNT>]] [disperse [<COUNT>]] [disperse-data <COUNT>] [redundancy <COUNT>] [transport <tcp|rdma|tcp,rdma>] <NEW-BRICK>... [force] - create a new volume of specified type with mentioned bricks



// 创建分布式复制卷
// 注: 创建卷的操作可以在 集群中的任意 node 上执行, 创建出来的 volume 属于集群而不属于机器
[root@node01 ~]# gluster volume create data_volume04_distributed_replicated replica 2 \
                    node01:/data04_distributed_replicated/br1 \
                    node02:/data04_distributed_replicated/br1 \
                    node03:/data04_distributed_replicated/br1 \
                    node04:/data04_distributed_replicated/br1

    Replica 2 volumes are prone to split-brain. Use Arbiter or Replica 3 to avoid this. See: http://docs.gluster.org/en/latest/Administrator%20Guide/Split%20brain%20and%20ways%20to%20deal%20with%20it/.
    Do you still want to continue?
     (y/n) y
    volume create: data_volume04_distributed_replicated: success: please start the volume to access data
`


// 启动卷
[root@node01 ~]# gluster volume start data_volume04_distributed_replicated
      volume start: data_volume04_distributed_replicated: success


// 列出集群中的所有卷
[root@node01 ~]# gluster volume list
      data_volume01_distributed
      data_volume02_replicated
      data_volume04_distributed_replicated <-----


// 查看 卷 data_volume04_distributed_replicated 的信息
[root@node01 ~]# gluster volume info data_volume04_distributed_replicated

        Volume Name: data_volume04_distributed_replicated
        Type: Distributed-Replicate  <------------观察
        Volume ID: 0c92a504-971a-46c7-a73c-919e36bc9a45
        Status: Started
        Snapshot Count: 0
        Number of Bricks: 2 x 2 = 4
        Transport-type: tcp
        Bricks:
        Brick1: node01:/data04_distributed_replicated/br1
        Brick2: node02:/data04_distributed_replicated/br1
        Brick3: node03:/data04_distributed_replicated/br1
        Brick4: node04:/data04_distributed_replicated/br1
        Options Reconfigured:
        performance.client-io-threads: off
        nfs.disable: on
        transport.address-family: inet


// 客户端使用卷
[root@client ~]# mkdir /testdir04_distributed_replicated
      node01:/data_volume04_distributed_replicated  /testdir04_distributed_replicated  glusterfs   defaults,_netdev        0 0


// 挂载卷
// 注: 因为 volume 属于集群而非属于机器, 所以可以通过任意一个 node 挂载
[root@client ~]# mount -a
[root@client ~]# df -hT
    Filesystem                                   Type            Size  Used Avail Use% Mounted on
    /dev/mapper/centos-root                      xfs              18G  1.9G   16G  11% /
    devtmpfs                                     devtmpfs        478M     0  478M   0% /dev
    tmpfs                                        tmpfs           489M     0  489M   0% /dev/shm
    tmpfs                                        tmpfs           489M  6.7M  482M   2% /run
    tmpfs                                        tmpfs           489M     0  489M   0% /sys/fs/cgroup
    /dev/sda1                                    xfs             197M  103M   95M  53% /boot
    node01:/data_volume02_replicated             fuse.glusterfs  2.0G   31M  1.8G   2% /testdir02_replicated
    node01:/data_volume04_distributed_replicated fuse.glusterfs  3.9G   52M  3.6G   2% /testdir04_distributed_replicated <----观察(大小4G~(2G+2G+2G+2G)/2)
    node01:/data_volume01_distributed            fuse.glusterfs  3.9G   52M  3.6G   2% /testdir01_distributed
    tmpfs                                        tmpfs            98M     0   98M   0% /run/user/0


[root@client ~]# for i in {1..10};
> do
>   head -c 10M < /dev/urandom > /testdir04_distributed_replicated/${i}.txt
> done


// 在 client 端查看
[root@client ~]# ls -lh /testdir04_distributed_replicated/
      total 100M
      -rw-r--r-- 1 root root 10M Sep  9 12:12 10.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 1.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 2.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 3.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 4.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 5.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 6.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 7.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 8.txt
      -rw-r--r-- 1 root root 10M Sep  9 12:12 9.txt


// 在 node01 上查看
[root@node01 ~]# ls -lh /data04_distributed_replicated/br1/
      total 31M
      -rw-r--r-- 2 root root 10M Sep  9 12:12 4.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 8.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 9.txt

// 在 node02 上查看 (可发现与 node01 相同, 即 node01 和 node02 的 brick 互为复制)
[root@node02 ~]# ls -lh /data04_distributed_replicated/br1/
      total 31M
      -rw-r--r-- 2 root root 10M Sep  9 12:12 4.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 8.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 9.txt

// 在 node03 上查看
[root@node03 ~]# ls -lh /data04_distributed_replicated/br1/
      total 71M
      -rw-r--r-- 2 root root 10M Sep  9 12:12 10.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 1.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 2.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 3.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 5.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 6.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 7.txt


// 在 node04 上查看 (可发现与 node03 相同, 即 node03 和 node04 的 brick 互为复制)
[root@node04 ~]# ls -lh /data04_distributed_replicated/br1/
      total 71M
      -rw-r--r-- 2 root root 10M Sep  9 12:12 10.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 1.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 2.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 3.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 5.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 6.txt
      -rw-r--r-- 2 root root 10M Sep  9 12:12 7.txt








----------------------------------------------------------------------------------------------------






























----------------------------------------------------------------------------------------------------
网上资料:
https://www.linuxtechi.com/setup-glusterfs-storage-on-centos-7-rhel-7/




