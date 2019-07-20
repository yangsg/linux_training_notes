


mha4mysql:
      MHA for MySQL: Master High Availability Manager and tools for MySQL (MHA) for automating master failover and fast master switch.

mha4mysql 可以保证数据的 一致性(consistency), 结合 semi-sync 几乎(最大限度) 保证 no data loss.


MHA works with the most common two-tier single master and multiple slaves environments

MHA Manager 通常运行在 一台专用的 server 上(或 2 台, 为了 高可用)
MHA Manager can monitor lots of (even 100+) masters from single server
When monitoring master server, MHA just sends ping packets to master every N seconds (default 3) and it does not send heavy queries.


---------------------------------------------------------------------------------------------------

本示例 采用 1 主 3 从 的复制拓扑结构:

    主要是考虑 1主3从 相比 1主2从, 3台 slaves 能更好 scale out reading traffic,
    而对于一般的网站而言大部分查询都是 select 查询.
    而 假如 有 1 台 server 宕机了, 则还剩 3 台 servers, 此时 仍能保持 为 1主2从,
    此时 执行一些 耗时的 操作(如backups, analytic queries, batch jobs) 从 维护方便 和 性能
    影响考虑还是可以接受的. 总之, 应尽可能降低 出现 1主1从 的风险, 使管理员在 维护时
    至少保证有 1主2从 的环境, 这样可以降低 管理员的 维护压力 和 在线的性能影响.

    更多此类问题的讨论见:
        https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Other_HA_Solutions.md
        https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/UseCases.md


  注:
    实际生产环境中, 可考虑采用 mha + semi-sync 结合的方式, 这样还能尽可能保证完整性(几乎 no data loss).
    而 全同步复制 需要使用 NDB Cluster, 虽然 数据完整性 能保证, 但 其 降低了 性能 且 不支持 innodb, 所以通常不会采用,
    而如果对 数据 的 完整性(no data loss) 的 要求再高一点儿, 可以 考虑 设置
    rpl_semi_sync_master_wait_for_slave_count 为 大于 1 的 某个相应值.


manager :   192.168.175.100  <----- 生产环境中 最好 manager server 也弄 2 台以上, 保证 manager 本身的高可用
master  :   192.168.175.101
slave01 :   192.168.175.102
slave02 :   192.168.175.103
slave03 :   192.168.175.104

  对应的 replication 的 拓扑结构如下:

              M(RW)                                       M(RW), promoted from S1
               |                                           |
        +------+------+        --(master crash)-->   +-----+------+
      S1(R)  S2(R)  S3(R)                          S2(R)        S3(R)


  如上的 拓扑结构 可以很容易的 就 配置成如下 结构:

             M(RW)<--->M2(R,candidate_master=1)           M(RW), promoted from M2
              |                                            |
       +------+------+        --(master crash)-->   +------+------+
      S(R)         S2(R)                          S1(R)      S2(R)



---------------------------------------------------------------------------------------------------
搭建 本地 yum repo 服务器

因为 外网 网速 太慢, 所有这次 准备自己 搭建 一台 简单的 local yum repo 服务器, 通过该 server 安装 mysql 软件.
具体步骤见:
      https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver


---------------------------------------------------------------------------------------------------
master 上 安装 mysql

// 配置 本地 yum 源, 参考 https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver
[root@master01 ~]# vim /etc/yum.repos.d/000-local-yum.repo

        [000-local-yum]
        name=000-local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0



[root@master ~]# yum repolist | grep local-yum
[root@master ~]# yum clean metadata
[root@master ~]# yum -y install mysql-community-server

[root@master ~]# rpm -q mysql-community-server
          mysql-community-server-5.7.26-1.el7.x86_64

[root@master ~]# yum list installed  mysql-community-server

[root@master ~]# systemctl start mysqld
[root@master ~]# systemctl enable mysqld.service
[root@master ~]# systemctl status mysqld.service

[root@master ~]# grep 'temporary password' /var/log/mysqld.log
        2019-07-18T02:35:40.301694Z 1 [Note] A temporary password is generated for root@localhost: O0MNuVV!7?#)

[root@master ~]# mysql -u root -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit

[root@master ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2067/mysqld

[root@master ~]# ps -elf | grep mysql
    1 S mysql      2067      1  0  80   0 - 279982 poll_s 15:52 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


---------------------------------------------------------------------------------------------------
在 slave01, slave02 上安装 mysql, 方法 与 如上 master 安装方法一样 (此处略)




---------------------------------------------------------------------------------------------------
































---------------------------------------------------------------------------------------------------













---------------------------------------------------------------------------------------------------
网上资料:


yoshinorim/mha4mysql-manager
    https://github.com/yoshinorim/mha4mysql-manager/wiki
    https://github.com/yoshinorim/mha4mysql-manager
    https://www.percona.com/blog/2016/09/02/mha-quickstart-guide/


http://www.ttlsa.com/mysql/step-one-by-one-deploy-mysql-mha-cluster/


mha 之外的 其他一些 解决方案的 缺点 和 问题(重要):
      https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Other_HA_Solutions.md

mha 体系结构
https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Architecture.md

  MHA Components:
      MHA Manager has manager programs such as monitoring MySQL master, controlling master failover, etc.

  MHA Node:
      MHA Node has failover helper scripts such as parsing MySQL binary/relay logs,
      identifying relay log position from which relay logs should be applied to other slaves,
      applying events to the target slave, etc. MHA Node runs on each MySQL server.

  When MHA Manager does failover, MHA manager connects MHA Node via SSH and executes MHA Node commands when needed.


  MHA has a couple of extention points. For example, MHA can call any custom script
  to update master's ip address (updating global catalog database that manages master's ip address,
  updating virtual ip, etc). This is because how to manage IP address depends on
  users' environments and MHA does not want to force one approach.


mha 的优点:
  https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Advantages.md

      * [Master failover and slave promotion can be done very quickly](#master-failover-and-slave-promotion-can-be-done-very-quickly)
      * [Master crash does not result in data inconsistency](#master-crash-does-not-result-in-data-inconsistency)
      * [No need to modify current MySQL settings](#no-need-to-modify-current-mysql-settings)
      * [No need to increase lots of servers](#no-need-to-increase-lots-of-servers)
      * [No performance penalty](#no-performance-penalty)
      * [Works with any storage engine](#works-with-any-storage-engine)


mha 的典型用例:
  https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/UseCases.md


