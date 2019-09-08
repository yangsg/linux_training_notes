

GlusterFS


https://www.gluster.org/
https://docs.gluster.org/en/latest/

GlusterFS 架构:
    https://docs.gluster.org/en/latest/Quick-Start-Guide/Architecture/

    https://blog.51cto.com/11697257/2089478






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
Striped Glusterfs Volume (条带卷/条纹卷)


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
        |   node01(/dev/sdb)    |=====> gluster volume(data_volume01_distributed)
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
























----------------------------------------------------------------------------------------------------
网上资料:
https://www.linuxtechi.com/setup-glusterfs-storage-on-centos-7-rhel-7/




