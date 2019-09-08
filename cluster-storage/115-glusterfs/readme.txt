

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


// 在 node01 上观察一下 peer 状态信息
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


// 在 node03 上观察一下 peer 状态信息
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
网上资料:
https://www.linuxtechi.com/setup-glusterfs-storage-on-centos-7-rhel-7/




