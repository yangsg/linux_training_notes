
本文档 主要 结合 如下两个文档 的内容, 搭 一个 mha + semi_sync 的简单集群
    https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/005-gtid-utf8mb4-rpm-mha4mysql
    https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/004-gtid-utf8mb4-rpm-semi-sync-replication



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

注:
    如下hostname 为 master 和 slave01 等可能并不太好,
    因它们之间的角色是可以相互转换的,可能类似 host 或 server 等的名字更好一点儿

manager :   192.168.175.110   mha4mysql-node  mha4mysql-manager <----- 生产环境中 最好 manager server 也弄 2 台以上, 保证 manager 本身的高可用
master  :   192.168.175.100   mha4mysql-node     semisync_master.so  semisync_slave.so  <--- 因随时可能在 角色 master 和 角色 slave 之间相互切换
slave01 :   192.168.175.101   mha4mysql-node     semisync_master.so  semisync_slave.so
slave02 :   192.168.175.102   mha4mysql-node     semisync_master.so  semisync_slave.so
slave03 :   192.168.175.103   mha4mysql-node     semisync_master.so  semisync_slave.so

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
前期一些其他准备:

// 设置时区, 同步时间:
      https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/001-one-master-to-one-slave-simplest

// 为熵池 提供一个好的 采集方案:
      https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/01-full/031-rngd.txt

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
在 slave01, slave02, slave03 上安装 mysql, 方法 与 如上 master 安装方法一样 (此处略)




---------------------------------------------------------------------------------------------------
1. 先搭建 mha 可用 基础的 one master to three slaves 的 replication 拓扑环境

注意:
     该例中 除了包含 纯粹的 1主3从 的 replication 拓扑结构的配置外,
     还直接包含了 mha 需要的基础配置,
     因为 mha 环境中 master <---> slave 之间 角色之间不稳定,
     是可以在特定条件下随时 相互转换 的.

--------------------
master 端 replication 设置

[root@master ~]# vim /etc/my.cnf

            [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
            loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

            [mysql]
            default-character-set = utf8mb4

            [mysqlbinlog]
            set_charset=utf8mb4

            [mysqld]
            # 设置 mysql 字符集为 utf8mb4
            character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
            character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
            collation-server = utf8mb4_unicode_ci

            # 启用 skip-name-resolve 不仅能优化性能(特别是在 DNS 很慢或有许多hosts时),
            # 还能 解决 本示例中 权限的问题, 因为本示例中 用户都是基于 ip 地址创建并授权的,
            # 如 'repluser'@'192.168.175.102', 如果不启用 skip-name-resolve,
            # 则 在某时候 可能会去 检查账号 'repluser'@'slave02' 的授权, 因为本示例未对 'repluser'@'slave02'
            # 授权, 导致 因权限拒绝 而 访问失败, 从而无法正常实现 replication 功能.
            #   --skip-name-resolve:  Don't resolve hostnames. All hostnames are IP's or 'localhost'.
            #   https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_skip-name-resolve
            #   https://dev.mysql.com/doc/refman/5.7/en/host-cache.html
            skip-name-resolve=ON


            # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
            log-bin=master-bin
            server-id=100   # server-id 范围: 1 and (232)−1
            gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
            enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

            # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
            #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
            #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency

            # 注:
            #    因为是在 mha 高可用环境中, 所有 master 的 角色不是一成不变的, 其本省也 可能转换成 slave 角色,
            #    所以同样需要其 扮演 slave 时的 slave 相关配置
            # 此例中 打算 使用 TABLE 记录 master_info 和 relay_log_info
            # 一些 mysql replication 的 最佳实践(best practices) 指南 见 https://www.percona.com/sites/default/files/presentations/Replication-webinar.pdf
            master_info_repository=TABLE
            relay_log_info_repository=TABLE
            relay-log-recovery=1

            # 如下 2 行 是与 半同步复制 相关的设置
            # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
            #     有因为 在 mha 中, mysql server 的角色 会在 master <--> slave 时间相互切换, 即 mysql server
            #     有 扮演 master 和 slave 这两种不同角色的机会, 所以对于 同一 mysql server,
            #     要 同时 安装 和 启用 semi-sync replication 的 semisync_master.so 插件 和 semisync_slave.so 插件
            # 注: 安装插件的方式 如 plugin-load-add 和 INSTALL PLUGIN 仅能 择其一,
            #     即使用了 plugin-load-add 安装 就不要再使用 INSTALL PLUGIN 方式安装, 或
            #     使用过 INSTALL PLUGIN 安装就 不要再 使用 plugin-load-add 方式安装, 否则会报错
            #     关于插件安装方式 见
            #     https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html
            #     https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html
            plugin-load-add='rpl_semi_sync_master=semisync_master.so'  # 加载半同步复制的 semisync_master.so 插件
            plugin-load-add='rpl_semi_sync_slave=semisync_slave.so'    # 加载半同步复制的 semisync_slave.so 插件
            rpl_semi_sync_master_enabled=1                             # 启用半同步复制的 master 插件
            rpl_semi_sync_master_timeout=1000                          # 1 second # 默认为 10 seconds
            rpl_semi_sync_slave_enabled=1                              # 启用半同步复制的 slave 插件

            # 更多 与 半同步复制 相关的 系统变量 或 状态变量 见:
            #    https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html
            #    https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html
            #    https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html




// 重启 mysql server, 以 应用 如上的配置
[root@master ~]# systemctl restart mysqld

// 查看验证 插件 semisync_master.so 和 semisync_slave.so 是否被 安装加载
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
        +----------------------+---------------+
        | PLUGIN_NAME          | PLUGIN_STATUS |
        +----------------------+---------------+
        | rpl_semi_sync_master | ACTIVE        | <----
        | rpl_semi_sync_slave  | ACTIVE        | <----
        +----------------------+---------------+


// 查看验证 相关的 'rpl_semi_sync%' 配置 是否 生效
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
        +-------------------------------------------+------------+
        | Variable_name                             | Value      |
        +-------------------------------------------+------------+
        | rpl_semi_sync_master_enabled              | ON         | <---------
        | rpl_semi_sync_master_timeout              | 1000       |
        | rpl_semi_sync_master_trace_level          | 32         |
        | rpl_semi_sync_master_wait_for_slave_count | 1          |
        | rpl_semi_sync_master_wait_no_slave        | ON         |
        | rpl_semi_sync_master_wait_point           | AFTER_SYNC |
        | rpl_semi_sync_slave_enabled               | ON         | <---------
        | rpl_semi_sync_slave_trace_level           | 32         |
        +-------------------------------------------+------------+

// 查看 此时 相关的 'Rpl_semi_sync%' 状态
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
        +--------------------------------------------+-------+
        | Variable_name                              | Value |
        +--------------------------------------------+-------+
        | Rpl_semi_sync_master_clients               | 0     |
        | Rpl_semi_sync_master_net_avg_wait_time     | 0     |
        | Rpl_semi_sync_master_net_wait_time         | 0     |
        | Rpl_semi_sync_master_net_waits             | 0     |
        | Rpl_semi_sync_master_no_times              | 0     |
        | Rpl_semi_sync_master_no_tx                 | 0     |
        | Rpl_semi_sync_master_status                | ON    |
        | Rpl_semi_sync_master_timefunc_failures     | 0     |
        | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
        | Rpl_semi_sync_master_tx_wait_time          | 0     |
        | Rpl_semi_sync_master_tx_waits              | 0     |
        | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
        | Rpl_semi_sync_master_wait_sessions         | 0     |
        | Rpl_semi_sync_master_yes_tx                | 0     |
        | Rpl_semi_sync_slave_status                 | OFF   |
        +--------------------------------------------+-------+



// 创建 专用于 replication 的 user. 参见 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
// 注:
//     create user 的步骤有 许多 问题 或 细节要考虑, 所以为了 最大的 灵活性, 最好 按部就班 的 按如下的 步骤 和 语法
//     来 创建用户(尤其是 涉及 replication 的 拓扑结构中), 具体原因见
//     https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/003-gtid-utf8mb4-rpm-multi-source-replication
//     或 参考   http://www.unixfbi.com/155.html   中 “复制账号重复问题”
mysql> USE mysql;
mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.100' IDENTIFIED BY 'WWW.1.rep';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.100';       # 授予 该用户 replication slave 权限

mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.101' IDENTIFIED BY 'WWW.1.rep';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.101';       # 授予 该用户 replication slave 权限

mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.102' IDENTIFIED BY 'WWW.1.rep';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.102';       # 授予 该用户 replication slave 权限

mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.rep';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.103';       # 授予 该用户 replication slave 权限

     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.


// 在 master 上 做一次 full backup, 后续的操作 会 将其 同步给 slave
[root@master ~]# mysqldump --help | grep -E '^default-character-set'
        default-character-set             utf8mb4

[root@master ~]# mysqldump -u root -p --lock-all-tables --all-databases --master-data=2 > /root/db_full-backup.sql
Enter password:
Warning: A partial dump from a server that has GTIDs will by default include the GTIDs of all transactions, even those that changed suppressed parts of the database. If you don't want to restore GTIDs, pass --set-gtid-purged=OFF. To make a complete dump, pass --all-databases --triggers --routines --events.


// 将 master 的 db_full-backup.sql 拷贝给 slave
[root@master ~]# rsync -av /root/db_full-backup.sql  root@192.168.175.101:/tmp/
[root@master ~]# rsync -av /root/db_full-backup.sql  root@192.168.175.102:/tmp/
[root@master ~]# rsync -av /root/db_full-backup.sql  root@192.168.175.103:/tmp/


// 查看一下 状态信息
mysql> show master status;
      +-------------------+----------+--------------+------------------+------------------------------------------+
      | File              | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
      +-------------------+----------+--------------+------------------+------------------------------------------+
      | master-bin.000001 |     2158 |              |                  | 41141e82-ab81-11e9-9a5f-000c29152d2e:1-8 |
      +-------------------+----------+--------------+------------------+------------------------------------------+





--------------------
slave01 端 replication 设置


[root@slave01 ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

          [mysql]
          default-character-set = utf8mb4

          [mysqlbinlog]
          set_charset=utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 启用 skip-name-resolve 不仅能优化性能(特别是在 DNS 很慢或有许多hosts时),
          # 还能 解决 本示例中 权限的问题, 因为本示例中 用户都是基于 ip 地址创建并授权的,
          # 如 'repluser'@'192.168.175.102', 如果不启用 skip-name-resolve,
          # 则 在某时候 可能会去 检查账号 'repluser'@'slave02' 的授权, 因为本示例未对 'repluser'@'slave02'
          # 授权, 导致 因权限拒绝 而 访问失败, 从而无法正常实现 replication 功能.
          #   --skip-name-resolve:  Don't resolve hostnames. All hostnames are IP's or 'localhost'.
          #   https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_skip-name-resolve
          #   https://dev.mysql.com/doc/refman/5.7/en/host-cache.html
          skip-name-resolve=ON

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=slave01-bin
          server-id=101   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency

          # 此例中 打算 使用 TABLE 记录 master_info 和 relay_log_info
          # 一些 mysql replication 的 最佳实践(best practices) 指南 见 https://www.percona.com/sites/default/files/presentations/Replication-webinar.pdf
          master_info_repository=TABLE
          relay_log_info_repository=TABLE
          relay-log-recovery=1

          # 如下 2 行 是与 半同步复制 相关的设置
          # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
          #     有因为 在 mha 中, mysql server 的角色 会在 master <--> slave 时间相互切换, 即 mysql server
          #     有 扮演 master 和 slave 这两种不同角色的机会, 所以对于 同一 mysql server,
          #     要 同时 安装 和 启用 semi-sync replication 的 semisync_master.so 插件 和 semisync_slave.so 插件
          # 注: 安装插件的方式 如 plugin-load-add 和 INSTALL PLUGIN 仅能 择其一,
          #     即使用了 plugin-load-add 安装 就不要再使用 INSTALL PLUGIN 方式安装, 或
          #     使用过 INSTALL PLUGIN 安装就 不要再 使用 plugin-load-add 方式安装, 否则会报错
          #     关于插件安装方式 见
          #     https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html
          #     https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html
          plugin-load-add='rpl_semi_sync_master=semisync_master.so'  # 加载半同步复制的 semisync_master.so 插件
          plugin-load-add='rpl_semi_sync_slave=semisync_slave.so'    # 加载半同步复制的 semisync_slave.so 插件
          rpl_semi_sync_master_enabled=1                             # 启用半同步复制的 master 插件
          rpl_semi_sync_master_timeout=1000                          # 1 second # 默认为 10 seconds
          rpl_semi_sync_slave_enabled=1                              # 启用半同步复制的 slave 插件

          # 更多 与 半同步复制 相关的 系统变量 或 状态变量 见:
          #    https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html





// 先 通过 命令 mysqld 查看一下 配置
[root@slave01 ~]# mysqld --verbose --help | grep -E '^(log-bin |server-id |gtid-mode|enforce-gtid-consistency)'
        enforce-gtid-consistency                                     true
        gtid-mode                                                    ON
        log-bin                                                      slave01-bin
        server-id                                                    101



// 重启 slave01 的 mysql server 是 如上配置生效
[root@slave01 ~]# systemctl restart mysqld

// 查看验证 插件 semisync_master.so 和 semisync_slave.so 是否被 安装加
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
      +----------------------+---------------+
      | PLUGIN_NAME          | PLUGIN_STATUS |
      +----------------------+---------------+
      | rpl_semi_sync_master | ACTIVE        | <-----
      | rpl_semi_sync_slave  | ACTIVE        | <-----
      +----------------------+---------------+

// 查看验证 相关的 'rpl_semi_sync%' 配置 是否 生效
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
      +-------------------------------------------+------------+
      | Variable_name                             | Value      |
      +-------------------------------------------+------------+
      | rpl_semi_sync_master_enabled              | ON         | <-----
      | rpl_semi_sync_master_timeout              | 1000       |
      | rpl_semi_sync_master_trace_level          | 32         |
      | rpl_semi_sync_master_wait_for_slave_count | 1          |
      | rpl_semi_sync_master_wait_no_slave        | ON         |
      | rpl_semi_sync_master_wait_point           | AFTER_SYNC |
      | rpl_semi_sync_slave_enabled               | ON         | <-----
      | rpl_semi_sync_slave_trace_level           | 32         |
      +-------------------------------------------+------------+

// 查看 此时 相关的 'Rpl_semi_sync%' 状态
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
      +--------------------------------------------+-------+
      | Variable_name                              | Value |
      +--------------------------------------------+-------+
      | Rpl_semi_sync_master_clients               | 0     |
      | Rpl_semi_sync_master_net_avg_wait_time     | 0     |
      | Rpl_semi_sync_master_net_wait_time         | 0     |
      | Rpl_semi_sync_master_net_waits             | 0     |
      | Rpl_semi_sync_master_no_times              | 0     |
      | Rpl_semi_sync_master_no_tx                 | 0     |
      | Rpl_semi_sync_master_status                | ON    | <-----
      | Rpl_semi_sync_master_timefunc_failures     | 0     |
      | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
      | Rpl_semi_sync_master_tx_wait_time          | 0     |
      | Rpl_semi_sync_master_tx_waits              | 0     |
      | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
      | Rpl_semi_sync_master_wait_sessions         | 0     |
      | Rpl_semi_sync_master_yes_tx                | 0     |
      | Rpl_semi_sync_slave_status                 | OFF   |
      +--------------------------------------------+-------+



// 查看一下客户端工具 mysql 默认使用 的 字符集
[root@slave01 ~]# mysql --help | grep  ^default-character-set
      default-character-set             utf8mb4


// 查看一下 slave01 上的 master 的 一份完全备份
[root@slave01 ~]# ls /tmp/db_full-backup.sql
      /tmp/db_full-backup.sql


[root@slave01 ~]# mysql -u root -p < /tmp/db_full-backup.sql  # 以 batch mode 还原 master 的 备份(即保持slave 初始数据与 master 一致)

[root@slave01 ~]# echo $?
0

// 执行一下 help 帮助信息 查看 change master 的 语法帮助
mysql> help change master to

// 在 slave 上设置 master 信息 (即 到 master 的 连接, 认证 和 replication 的坐标信息)
mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.175.100',
    -> MASTER_PORT=3306,
    -> MASTER_USER='repluser',
    -> MASTER_PASSWORD='WWW.1.rep',
    -> MASTER_AUTO_POSITION=1 ; #因为是基于 gtid, 所有启用 MASTER_AUTO_POSITION 功能自动确定 replication 所需的坐标信息

// 启动 slave 的 io_thread 和 sql_thread
mysql> start slave;


mysql> pager less -Fi
mysql> show slave status\G

             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes





----------------------------------------------------------------

slave02 端 replication 设置


[root@slave02 ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

          [mysql]
          default-character-set = utf8mb4

          [mysqlbinlog]
          set_charset=utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 启用 skip-name-resolve 不仅能优化性能(特别是在 DNS 很慢或有许多hosts时),
          # 还能 解决 本示例中 权限的问题, 因为本示例中 用户都是基于 ip 地址创建并授权的,
          # 如 'repluser'@'192.168.175.102', 如果不启用 skip-name-resolve,
          # 则 在某时候 可能会去 检查账号 'repluser'@'slave02' 的授权, 因为本示例未对 'repluser'@'slave02'
          # 授权, 导致 因权限拒绝 而 访问失败, 从而无法正常实现 replication 功能.
          #   --skip-name-resolve:  Don't resolve hostnames. All hostnames are IP's or 'localhost'.
          #   https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_skip-name-resolve
          #   https://dev.mysql.com/doc/refman/5.7/en/host-cache.html
          skip-name-resolve=ON

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=slave02-bin
          server-id=102   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency

          # 此例中 打算 使用 TABLE 记录 master_info 和 relay_log_info
          # 一些 mysql replication 的 最佳实践(best practices) 指南 见 https://www.percona.com/sites/default/files/presentations/Replication-webinar.pdf
          master_info_repository=TABLE
          relay_log_info_repository=TABLE
          relay-log-recovery=1

          # 如下 2 行 是与 半同步复制 相关的设置
          # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
          #     有因为 在 mha 中, mysql server 的角色 会在 master <--> slave 时间相互切换, 即 mysql server
          #     有 扮演 master 和 slave 这两种不同角色的机会, 所以对于 同一 mysql server,
          #     要 同时 安装 和 启用 semi-sync replication 的 semisync_master.so 插件 和 semisync_slave.so 插件
          # 注: 安装插件的方式 如 plugin-load-add 和 INSTALL PLUGIN 仅能 择其一,
          #     即使用了 plugin-load-add 安装 就不要再使用 INSTALL PLUGIN 方式安装, 或
          #     使用过 INSTALL PLUGIN 安装就 不要再 使用 plugin-load-add 方式安装, 否则会报错
          #     关于插件安装方式 见
          #     https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html
          #     https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html
          plugin-load-add='rpl_semi_sync_master=semisync_master.so'  # 加载半同步复制的 semisync_master.so 插件
          plugin-load-add='rpl_semi_sync_slave=semisync_slave.so'    # 加载半同步复制的 semisync_slave.so 插件
          rpl_semi_sync_master_enabled=1                             # 启用半同步复制的 master 插件
          rpl_semi_sync_master_timeout=1000                          # 1 second # 默认为 10 seconds
          rpl_semi_sync_slave_enabled=1                              # 启用半同步复制的 slave 插件



// 先 通过 命令 mysqld 查看一下 配置
[root@slave02 ~]# mysqld --verbose --help | grep -E '^(log-bin |server-id |gtid-mode|enforce-gtid-consistency)'
          enforce-gtid-consistency                                     true
          gtid-mode                                                    ON
          log-bin                                                      slave02-bin
          server-id                                                    102


// 重启 slave02 的 mysql server 是 如上配置生效
[root@slave02 ~]# systemctl restart mysqld


// 查看验证 插件 semisync_master.so 和 semisync_slave.so 是否被 安装加
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
      +----------------------+---------------+
      | PLUGIN_NAME          | PLUGIN_STATUS |
      +----------------------+---------------+
      | rpl_semi_sync_master | ACTIVE        | <-----
      | rpl_semi_sync_slave  | ACTIVE        | <-----
      +----------------------+---------------+

// 查看验证 相关的 'rpl_semi_sync%' 配置 是否 生效
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
      +-------------------------------------------+------------+
      | Variable_name                             | Value      |
      +-------------------------------------------+------------+
      | rpl_semi_sync_master_enabled              | ON         | <-----
      | rpl_semi_sync_master_timeout              | 1000       |
      | rpl_semi_sync_master_trace_level          | 32         |
      | rpl_semi_sync_master_wait_for_slave_count | 1          |
      | rpl_semi_sync_master_wait_no_slave        | ON         |
      | rpl_semi_sync_master_wait_point           | AFTER_SYNC |
      | rpl_semi_sync_slave_enabled               | ON         | <-----
      | rpl_semi_sync_slave_trace_level           | 32         |
      +-------------------------------------------+------------+

// 查看 此时 相关的 'Rpl_semi_sync%' 状态
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
      +--------------------------------------------+-------+
      | Variable_name                              | Value |
      +--------------------------------------------+-------+
      | Rpl_semi_sync_master_clients               | 0     |
      | Rpl_semi_sync_master_net_avg_wait_time     | 0     |
      | Rpl_semi_sync_master_net_wait_time         | 0     |
      | Rpl_semi_sync_master_net_waits             | 0     |
      | Rpl_semi_sync_master_no_times              | 0     |
      | Rpl_semi_sync_master_no_tx                 | 0     |
      | Rpl_semi_sync_master_status                | ON    | <-----
      | Rpl_semi_sync_master_timefunc_failures     | 0     |
      | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
      | Rpl_semi_sync_master_tx_wait_time          | 0     |
      | Rpl_semi_sync_master_tx_waits              | 0     |
      | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
      | Rpl_semi_sync_master_wait_sessions         | 0     |
      | Rpl_semi_sync_master_yes_tx                | 0     |
      | Rpl_semi_sync_slave_status                 | OFF   |
      +--------------------------------------------+-------+



// 查看一下客户端工具 mysql 默认使用 的 字符集
[root@slave02 ~]# mysql --help | grep  ^default-character-set
      default-character-set             utf8mb4


// 查看一下 slave02 上的 master 的 一份完全备份
[root@slave02 ~]# ls /tmp/db_full-backup.sql
      /tmp/db_full-backup.sql


[root@slave02 ~]# mysql -u root -p < /tmp/db_full-backup.sql  # 以 batch mode 还原 master 的 备份(即保持slave 初始数据与 master 一致)

[root@slave02 ~]# echo $?
0

// 执行一下 help 帮助信息 查看 change master 的 语法帮助
mysql> help change master to

// 在 slave 上设置 master 信息 (即 到 master 的 连接, 认证 和 replication 的坐标信息)
mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.175.100',
    -> MASTER_PORT=3306,
    -> MASTER_USER='repluser',
    -> MASTER_PASSWORD='WWW.1.rep',
    -> MASTER_AUTO_POSITION=1 ; #因为是基于 gtid, 所有启用 MASTER_AUTO_POSITION 功能自动确定 replication 所需的坐标信息

// 启动 slave 的 io_thread 和 sql_thread
mysql> start slave;


mysql> pager less -Fi
mysql> show slave status\G

             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes


// 此时 在 master 端 执行 如下 语句 看一下 master 端相关 'Rpl_semi_sync%' 状态 变化
        mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';          #<---- 注: 此语句在 master 端 执行
        +--------------------------------------------+-------+
        | Variable_name                              | Value |
        +--------------------------------------------+-------+
        | Rpl_semi_sync_master_clients               | 2     | <------
        | Rpl_semi_sync_master_net_avg_wait_time     | 0     |
        | Rpl_semi_sync_master_net_wait_time         | 0     |
        | Rpl_semi_sync_master_net_waits             | 0     |
        | Rpl_semi_sync_master_no_times              | 1     |
        | Rpl_semi_sync_master_no_tx                 | 8     |
        | Rpl_semi_sync_master_status                | ON    |
        | Rpl_semi_sync_master_timefunc_failures     | 0     |
        | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
        | Rpl_semi_sync_master_tx_wait_time          | 0     |
        | Rpl_semi_sync_master_tx_waits              | 0     |
        | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
        | Rpl_semi_sync_master_wait_sessions         | 0     |
        | Rpl_semi_sync_master_yes_tx                | 0     |
        | Rpl_semi_sync_slave_status                 | OFF   |
        +--------------------------------------------+-------+





----------------------------------------------------------------

slave03 端 replication 设置


[root@slave03 ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

          [mysql]
          default-character-set = utf8mb4

          [mysqlbinlog]
          set_charset=utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 启用 skip-name-resolve 不仅能优化性能(特别是在 DNS 很慢或有许多hosts时),
          # 还能 解决 本示例中 权限的问题, 因为本示例中 用户都是基于 ip 地址创建并授权的,
          # 如 'repluser'@'192.168.175.102', 如果不启用 skip-name-resolve,
          # 则 在某时候 可能会去 检查账号 'repluser'@'slave02' 的授权, 因为本示例未对 'repluser'@'slave02'
          # 授权, 导致 因权限拒绝 而 访问失败, 从而无法正常实现 replication 功能.
          #   --skip-name-resolve:  Don't resolve hostnames. All hostnames are IP's or 'localhost'.
          #   https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_skip-name-resolve
          #   https://dev.mysql.com/doc/refman/5.7/en/host-cache.html
          skip-name-resolve=ON

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=slave03-bin
          server-id=103   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency

          # 此例中 打算 使用 TABLE 记录 master_info 和 relay_log_info
          # 一些 mysql replication 的 最佳实践(best practices) 指南 见 https://www.percona.com/sites/default/files/presentations/Replication-webinar.pdf
          master_info_repository=TABLE
          relay_log_info_repository=TABLE
          relay-log-recovery=1

          # 如下 2 行 是与 半同步复制 相关的设置
          # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
          #     有因为 在 mha 中, mysql server 的角色 会在 master <--> slave 时间相互切换, 即 mysql server
          #     有 扮演 master 和 slave 这两种不同角色的机会, 所以对于 同一 mysql server,
          #     要 同时 安装 和 启用 semi-sync replication 的 semisync_master.so 插件 和 semisync_slave.so 插件
          # 注: 安装插件的方式 如 plugin-load-add 和 INSTALL PLUGIN 仅能 择其一,
          #     即使用了 plugin-load-add 安装 就不要再使用 INSTALL PLUGIN 方式安装, 或
          #     使用过 INSTALL PLUGIN 安装就 不要再 使用 plugin-load-add 方式安装, 否则会报错
          #     关于插件安装方式 见
          #     https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html
          #     https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html
          plugin-load-add='rpl_semi_sync_master=semisync_master.so'  # 加载半同步复制的 semisync_master.so 插件
          plugin-load-add='rpl_semi_sync_slave=semisync_slave.so'    # 加载半同步复制的 semisync_slave.so 插件
          rpl_semi_sync_master_enabled=1                             # 启用半同步复制的 master 插件
          rpl_semi_sync_master_timeout=1000                          # 1 second # 默认为 10 seconds
          rpl_semi_sync_slave_enabled=1                              # 启用半同步复制的 slave 插件




// 先 通过 命令 mysqld 查看一下 配置
[root@slave03 ~]# mysqld --verbose --help | grep -E '^(log-bin |server-id |gtid-mode|enforce-gtid-consistency)'
          enforce-gtid-consistency                                     true
          gtid-mode                                                    ON
          log-bin                                                      slave03-bin
          server-id                                                    103


// 重启 slave03 的 mysql server 是 如上配置生效
[root@slave03 ~]# systemctl restart mysqld


// 查看验证 插件 semisync_master.so 和 semisync_slave.so 是否被 安装加
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
      +----------------------+---------------+
      | PLUGIN_NAME          | PLUGIN_STATUS |
      +----------------------+---------------+
      | rpl_semi_sync_master | ACTIVE        | <-----
      | rpl_semi_sync_slave  | ACTIVE        | <-----
      +----------------------+---------------+

// 查看验证 相关的 'rpl_semi_sync%' 配置 是否 生效
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
      +-------------------------------------------+------------+
      | Variable_name                             | Value      |
      +-------------------------------------------+------------+
      | rpl_semi_sync_master_enabled              | ON         | <-----
      | rpl_semi_sync_master_timeout              | 1000       |
      | rpl_semi_sync_master_trace_level          | 32         |
      | rpl_semi_sync_master_wait_for_slave_count | 1          |
      | rpl_semi_sync_master_wait_no_slave        | ON         |
      | rpl_semi_sync_master_wait_point           | AFTER_SYNC |
      | rpl_semi_sync_slave_enabled               | ON         | <-----
      | rpl_semi_sync_slave_trace_level           | 32         |
      +-------------------------------------------+------------+

// 查看 此时 相关的 'Rpl_semi_sync%' 状态
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
      +--------------------------------------------+-------+
      | Variable_name                              | Value |
      +--------------------------------------------+-------+
      | Rpl_semi_sync_master_clients               | 0     |
      | Rpl_semi_sync_master_net_avg_wait_time     | 0     |
      | Rpl_semi_sync_master_net_wait_time         | 0     |
      | Rpl_semi_sync_master_net_waits             | 0     |
      | Rpl_semi_sync_master_no_times              | 0     |
      | Rpl_semi_sync_master_no_tx                 | 0     |
      | Rpl_semi_sync_master_status                | ON    | <-----
      | Rpl_semi_sync_master_timefunc_failures     | 0     |
      | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
      | Rpl_semi_sync_master_tx_wait_time          | 0     |
      | Rpl_semi_sync_master_tx_waits              | 0     |
      | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
      | Rpl_semi_sync_master_wait_sessions         | 0     |
      | Rpl_semi_sync_master_yes_tx                | 0     |
      | Rpl_semi_sync_slave_status                 | OFF   |
      +--------------------------------------------+-------+



// 查看一下客户端工具 mysql 默认使用 的 字符集
[root@slave03 ~]# mysql --help | grep  ^default-character-set
      default-character-set             utf8mb4


// 查看一下 slave03 上的 master 的 一份完全备份
[root@slave03 ~]# ls /tmp/db_full-backup.sql
      /tmp/db_full-backup.sql


[root@slave03 ~]# mysql -u root -p < /tmp/db_full-backup.sql  # 以 batch mode 还原 master 的 备份(即保持slave 初始数据与 master 一致)

[root@slave03 ~]# echo $?
0

// 执行一下 help 帮助信息 查看 change master 的 语法帮助
mysql> help change master to

// 在 slave 上设置 master 信息 (即 到 master 的 连接, 认证 和 replication 的坐标信息)
mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.175.100',
    -> MASTER_PORT=3306,
    -> MASTER_USER='repluser',
    -> MASTER_PASSWORD='WWW.1.rep',
    -> MASTER_AUTO_POSITION=1 ; #因为是基于 gtid, 所有启用 MASTER_AUTO_POSITION 功能自动确定 replication 所需的坐标信息

// 启动 slave 的 io_thread 和 sql_thread
mysql> start slave;


mysql> pager less -Fi
mysql> show slave status\G

             Slave_IO_Running: Yes
            Slave_SQL_Running: Yes


// 此时 在 master 端 执行 如下 语句 看一下 master 端相关 'Rpl_semi_sync%' 状态 变化
        mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';          #<---- 注: 此语句在 master 端 执行
        +--------------------------------------------+-------+
        | Variable_name                              | Value |
        +--------------------------------------------+-------+
        | Rpl_semi_sync_master_clients               | 3     | <-------
        | Rpl_semi_sync_master_net_avg_wait_time     | 0     |
        | Rpl_semi_sync_master_net_wait_time         | 0     |
        | Rpl_semi_sync_master_net_waits             | 0     |
        | Rpl_semi_sync_master_no_times              | 1     |
        | Rpl_semi_sync_master_no_tx                 | 8     |
        | Rpl_semi_sync_master_status                | ON    |
        | Rpl_semi_sync_master_timefunc_failures     | 0     |
        | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
        | Rpl_semi_sync_master_tx_wait_time          | 0     |
        | Rpl_semi_sync_master_tx_waits              | 0     |
        | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
        | Rpl_semi_sync_master_wait_sessions         | 0     |
        | Rpl_semi_sync_master_yes_tx                | 0     |
        | Rpl_semi_sync_slave_status                 | OFF   |
        +--------------------------------------------+-------+







---------------------------------------------------------------------------------------------------
2. 正式 部署 mha 集群



// 配置所有主机的ssh免密登录
[root@manager ~]# ssh-keygen -t rsa
      Generating public/private rsa key pair.
      Enter file in which to save the key (/root/.ssh/id_rsa): <======= 直接回车
      Created directory '/root/.ssh'.
      Enter passphrase (empty for no passphrase): <=========== 直接回车
      Enter same passphrase again: <=========== 直接回车
      Your identification has been saved in /root/.ssh/id_rsa.
      Your public key has been saved in /root/.ssh/id_rsa.pub.
      The key fingerprint is:
      SHA256:EtF5HKLYZPrk6pXWuWiTOF5YkGFfMU6juYnhhvBTe6s root@manager
      The key's randomart image is:
      +---[RSA 2048]----+
      |    o +.B+..     |
      |   . X Oo+o      |
      |.   B O ..       |
      | o + O +         |
      |  + = O S        |
      |   o = = .       |
      |    o.*.o        |
      |   .o=+. .       |
      |   .Eo...        |
      +----[SHA256]-----+


[root@manager ~]# tree .ssh
          .ssh
          ├── id_rsa      <-------
          └── id_rsa.pub  <-------


[root@manager ~]# ssh-copy-id root@192.168.175.110

[root@manager ~]# tree .ssh/
          .ssh/
          ├── authorized_keys  <------
          ├── id_rsa
          ├── id_rsa.pub
          └── known_hosts

[root@manager ~]# scp -r /root/.ssh/ root@192.168.175.100:/root/
[root@manager ~]# scp -r /root/.ssh/ root@192.168.175.101:/root/
[root@manager ~]# scp -r /root/.ssh/ root@192.168.175.102:/root/
[root@manager ~]# scp -r /root/.ssh/ root@192.168.175.103:/root/


// 在每台机器上验证
[root@manager ~]# for i in 110 100 101 102 103; do ssh 192.168.175.$i hostname; done
[root@master ~]#  for i in 110 100 101 102 103; do ssh 192.168.175.$i hostname; done
[root@slave01 ~]# for i in 110 100 101 102 103; do ssh 192.168.175.$i hostname; done
[root@slave02 ~]# for i in 110 100 101 102 103; do ssh 192.168.175.$i hostname; done
[root@slave03 ~]# for i in 110 100 101 102 103; do ssh 192.168.175.$i hostname; done


// 所有主机配置主机名解析 (注: 如果不通过 主机名连接, 如下主机名解析 其实是可以不用配置的)
[root@manager ~]# vim /etc/hosts

        127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
        ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6


        192.168.175.110   manager
        192.168.175.100   master
        192.168.175.101   slave01
        192.168.175.102   slave02
        192.168.175.103   slave03

[root@manager ~]# for i in 100 101 102 103;
> do
> scp /etc/hosts  root@192.168.175.$i:/etc/hosts
> done


// 对如上的 scp 拷贝操作 确认一下
[root@master ~]# for i in 110 100 101 102 103;
> do
> ssh root@192.168.175.$i 'echo $(md5sum /etc/hosts) --- $(hostname)'
> done


// 确认 时间 是否 同步(一致)
[root@manager ~]# for i in 110 100 101 102 103;
> do
> ssh root@192.168.175.$i 'echo $(date) --- $(hostname)' &
> done 2> /dev/null; wait 2> /dev/null


// 在mha_manager节点安装mha_manager,mha_node软件
[root@manager ~]# yum clean metadata
[root@manager ~]# yum install -y mha4mysql-manager mha4mysql-node

[root@manager ~]# rpm -q mha4mysql-manager mha4mysql-node
      mha4mysql-manager-0.58-0.el7.centos.noarch
      mha4mysql-node-0.58-0.el7.centos.noarch


// 在所有的数据库服务器上安装mha4mysql_node
[root@master ~]# yum clean metadata
[root@master ~]# yum install -y  mha4mysql-node

[root@slave01 ~]# yum clean metadata
[root@slave01 ~]# yum install -y  mha4mysql-node

[root@slave02 ~]# yum clean metadata
[root@slave02 ~]# yum install -y  mha4mysql-node

[root@slave03 ~]# yum clean metadata
[root@slave03 ~]# yum install -y  mha4mysql-node

// 确认 一下 如上 安装
[root@manager ~]# for i in 100 101 102 103;
> do
> ssh root@192.168.175.$i  'echo $(rpm -q mha4mysql-node) --- $(hostname)'
> done




在数据库服务器上创建MHA的管理用户 (5个)

// 如下语句 在 master 上执行, 让其 自动 同步给 slave01, slave02 和 slave03.
// 注:
//     create user 的步骤有 许多 问题 或 细节要考虑, 所以为了 最大的 灵活性, 最好 按部就班 的 按如下的 步骤 和 语法
//     来 创建用户(尤其是 涉及 replication 的 拓扑结构中), 具体原因见
//     https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/003-gtid-utf8mb4-rpm-multi-source-replication
//     或 参考   http://www.unixfbi.com/155.html   中 “复制账号重复问题”
mysql> USE mysql;
mysql> CREATE USER IF NOT EXISTS 'manager'@'192.168.175.110' IDENTIFIED BY 'WWW.1.manager';
mysql> GRANT ALL ON *.* TO 'manager'@'192.168.175.110';

mysql> CREATE USER IF NOT EXISTS 'manager'@'192.168.175.100' IDENTIFIED BY 'WWW.1.manager';
mysql> GRANT ALL ON *.* TO 'manager'@'192.168.175.100';

mysql> CREATE USER IF NOT EXISTS 'manager'@'192.168.175.101' IDENTIFIED BY 'WWW.1.manager';
mysql> GRANT ALL ON *.* TO 'manager'@'192.168.175.101';

mysql> CREATE USER IF NOT EXISTS 'manager'@'192.168.175.102' IDENTIFIED BY 'WWW.1.manager';
mysql> GRANT ALL ON *.* TO 'manager'@'192.168.175.102';

mysql> CREATE USER IF NOT EXISTS 'manager'@'192.168.175.103' IDENTIFIED BY 'WWW.1.manager';
mysql> GRANT ALL ON *.* TO 'manager'@'192.168.175.103';


     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.


// 配置mha_manager服务器
[root@manager ~]# mkdir -p /masterha/app1     # 创建工作目录，用于保存日志
[root@manager ~]# mkdir /etc/masterha         # 创建保存配置文件的目录


// 创建MHA的配置文件
[root@manager ~]# vim /etc/masterha/app1.cnf

              # https://github.com/yoshinorim/mha4mysql-manager/wiki/Configuration
              # https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Parameters.md

              [server default]
              #指定MHA的工作目录
              manager_workdir=/masterha/app1
              #指定MHA的日志文件
              manager_log=/masterha/app1/manager.log
              #后台数据库存在的管理用户
              user=manager
              password=WWW.1.manager
              #指定ssh免密登录的用户
              ssh_user=root
              #指定主从复制用户
              repl_user=repluser
              repl_password=WWW.1.rep
              #用于指定MHA检测master服务器的周期，单位为秒
              ping_interval=1
              shutdown_script=""

              [server1]
              hostname=192.168.175.100
              port=3306
              #用于指定该服务器保存二进制日志文件的目录
              master_binlog_dir="/var/lib/mysql"
              candidate_master=1

              [server2]
              hostname=192.168.175.101
              port=3306
              master_binlog_dir="/var/lib/mysql"
              candidate_master=1

              [server3]
              hostname=192.168.175.102
              port=3306
              master_binlog_dir="/var/lib/mysql"
              candidate_master=1

              [server4]
              hostname=192.168.175.103
              port=3306
              master_binlog_dir="/var/lib/mysql"
              candidate_master=1




// 检测ssh免密是否正常
[root@manager ~]# masterha_check_ssh --conf=/etc/masterha/app1.cnf

        ......

        Sun Jul 21 16:33:35 2019 - [info] All SSH connection tests passed successfully.


// 检测主从复制是否正常
[root@manager ~]# masterha_check_repl --conf=/etc/masterha/app1.cnf

        ------------ 观察 一下 输出 信息, 看一下 masterha_check_repl 做了 那些 检查
        Sun Jul 21 16:34:39 2019 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
        Sun Jul 21 16:34:39 2019 - [info] Reading application default configuration from /etc/masterha/app1.cnf..
        Sun Jul 21 16:34:39 2019 - [info] Reading server configuration from /etc/masterha/app1.cnf..
        Sun Jul 21 16:34:39 2019 - [info] MHA::MasterMonitor version 0.58.
        Sun Jul 21 16:34:40 2019 - [info] GTID failover mode = 1
        Sun Jul 21 16:34:40 2019 - [info] Dead Servers:
        Sun Jul 21 16:34:40 2019 - [info] Alive Servers:
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.100(192.168.175.100:3306)
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.101(192.168.175.101:3306)
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.102(192.168.175.102:3306)
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.103(192.168.175.103:3306)
        Sun Jul 21 16:34:40 2019 - [info] Alive Slaves:
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.101(192.168.175.101:3306)  Version=5.7.26-log (oldest major version between slaves) log-bin:enabled
        Sun Jul 21 16:34:40 2019 - [info]     GTID ON
        Sun Jul 21 16:34:40 2019 - [info]     Replicating from 192.168.175.100(192.168.175.100:3306)
        Sun Jul 21 16:34:40 2019 - [info]     Primary candidate for the new Master (candidate_master is set)
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.102(192.168.175.102:3306)  Version=5.7.26-log (oldest major version between slaves) log-bin:enabled
        Sun Jul 21 16:34:40 2019 - [info]     GTID ON
        Sun Jul 21 16:34:40 2019 - [info]     Replicating from 192.168.175.100(192.168.175.100:3306)
        Sun Jul 21 16:34:40 2019 - [info]     Primary candidate for the new Master (candidate_master is set)
        Sun Jul 21 16:34:40 2019 - [info]   192.168.175.103(192.168.175.103:3306)  Version=5.7.26-log (oldest major version between slaves) log-bin:enabled
        Sun Jul 21 16:34:40 2019 - [info]     GTID ON
        Sun Jul 21 16:34:40 2019 - [info]     Replicating from 192.168.175.100(192.168.175.100:3306)
        Sun Jul 21 16:34:40 2019 - [info]     Primary candidate for the new Master (candidate_master is set)
        Sun Jul 21 16:34:40 2019 - [info] Current Alive Master: 192.168.175.100(192.168.175.100:3306)
        Sun Jul 21 16:34:40 2019 - [info] Checking slave configurations..
        Sun Jul 21 16:34:40 2019 - [info]  read_only=1 is not set on slave 192.168.175.101(192.168.175.101:3306).
        Sun Jul 21 16:34:40 2019 - [info]  read_only=1 is not set on slave 192.168.175.102(192.168.175.102:3306).
        Sun Jul 21 16:34:40 2019 - [info]  read_only=1 is not set on slave 192.168.175.103(192.168.175.103:3306).
        Sun Jul 21 16:34:40 2019 - [info] Checking replication filtering settings..
        Sun Jul 21 16:34:40 2019 - [info]  binlog_do_db= , binlog_ignore_db=
        Sun Jul 21 16:34:40 2019 - [info]  Replication filtering check ok.
        Sun Jul 21 16:34:40 2019 - [info] GTID (with auto-pos) is supported. Skipping all SSH and Node package checking.
        Sun Jul 21 16:34:40 2019 - [info] Checking SSH publickey authentication settings on the current master..
        Sun Jul 21 16:34:40 2019 - [info] HealthCheck: SSH to 192.168.175.100 is reachable.
        Sun Jul 21 16:34:40 2019 - [info]
        192.168.175.100(192.168.175.100:3306) (current master)
         +--192.168.175.101(192.168.175.101:3306)
         +--192.168.175.102(192.168.175.102:3306)
         +--192.168.175.103(192.168.175.103:3306)

        Sun Jul 21 16:34:40 2019 - [info] Checking replication health on 192.168.175.101..
        Sun Jul 21 16:34:40 2019 - [info]  ok.
        Sun Jul 21 16:34:40 2019 - [info] Checking replication health on 192.168.175.102..
        Sun Jul 21 16:34:40 2019 - [info]  ok.
        Sun Jul 21 16:34:40 2019 - [info] Checking replication health on 192.168.175.103..
        Sun Jul 21 16:34:40 2019 - [info]  ok.
        Sun Jul 21 16:34:40 2019 - [warning] master_ip_failover_script is not defined.
        Sun Jul 21 16:34:40 2019 - [warning] shutdown_script is not defined.
        Sun Jul 21 16:34:40 2019 - [info] Got exit code 0 (Not master dead).

        MySQL Replication Health is OK.

        ------------




// 启动MHA
[root@manager ~]# masterha_manager --conf=/etc/masterha/app1.cnf  &
    [1] 1181
    [root@manager ~]# Sat Jul 20 19:39:31 2019 - [warning] Global configuration file /etc/masterha_default.cnf not found. Skipping.
    Sat Jul 20 19:39:31 2019 - [info] Reading application default configuration from /etc/masterha/app1.cnf..
    Sat Jul 20 19:39:31 2019 - [info] Reading server configuration from /etc/masterha/app1.cnf..


// 如下是 刚启动 MHA 是 与 mha 相关的 网络 状态信息
[root@manager ~]# netstat -anptu | grep 3306
    tcp        0      0 192.168.175.110:41368   192.168.175.101:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:36452   192.168.175.103:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:47650   192.168.175.102:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:33816   192.168.175.100:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:33822   192.168.175.100:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:47642   192.168.175.102:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:33832   192.168.175.100:3306    ESTABLISHED 17480/perl
    tcp        0      0 192.168.175.110:41358   192.168.175.101:3306    TIME_WAIT   -
    tcp        0      0 192.168.175.110:36444   192.168.175.103:3306    TIME_WAIT   -



// 一段时间之后 与 mha 有关的 网络状态信息
[root@manager ~]# netstat -anptu | grep 3306
    tcp        0      0 192.168.175.110:33832   192.168.175.100:3306    ESTABLISHED 17480/perl


// 观察 一下 日志 信息
[root@manager ~]# tail -f /masterha/app1/manager.log
       +--192.168.175.101(192.168.175.101:3306)
       +--192.168.175.102(192.168.175.102:3306)
       +--192.168.175.103(192.168.175.103:3306)

      Sun Jul 21 16:35:37 2019 - [warning] master_ip_failover_script is not defined.
      Sun Jul 21 16:35:37 2019 - [warning] shutdown_script is not defined.
      Sun Jul 21 16:35:37 2019 - [info] Set master ping interval 1 seconds.
      Sun Jul 21 16:35:37 2019 - [warning] secondary_check_script is not defined. It is highly recommended setting it to check master reachability from two or more routes.
      Sun Jul 21 16:35:37 2019 - [info] Starting ping health check on 192.168.175.100(192.168.175.100:3306)..
      Sun Jul 21 16:35:37 2019 - [info] Ping(SELECT) succeeded, waiting until MySQL doesn't respond..



// master 上执行 如下语句 观察
mysql> show slave hosts;
      +-----------+------+------+-----------+--------------------------------------+
      | Server_id | Host | Port | Master_id | Slave_UUID                           |
      +-----------+------+------+-----------+--------------------------------------+
      |       101 |      | 3306 |       100 | 4468f541-ab81-11e9-9102-000c29b95f25 |
      |       102 |      | 3306 |       100 | 4947337c-ab81-11e9-a370-000c29f6f083 |
      |       103 |      | 3306 |       100 | 4be3d091-ab81-11e9-9025-000c2982ac0f |
      +-----------+------+------+-----------+--------------------------------------+



---------------------------------------------------------------------------------------------------
测试 test:


// 关闭 master 上的 mysqld, 观察 故障转移 效果
[root@master ~]# systemctl stop mysqld


// slave01 上: (注: 故障转移不一定每次都 切换到 slave01 上, 所以有时需要在 slave02 或 slave03 才能看到如下信息)
mysql> show slave hosts;
      +-----------+------+------+-----------+--------------------------------------+
      | Server_id | Host | Port | Master_id | Slave_UUID                           |
      +-----------+------+------+-----------+--------------------------------------+
      |       103 |      | 3306 |       101 | 0b310aec-aab1-11e9-9f2a-000c2982ac0f |
      |       102 |      | 3306 |       101 | f9eb741e-aab0-11e9-9ee7-000c29f6f083 |
      +-----------+------+------+-----------+--------------------------------------+



// 恢复故障的主服务器

  主服务器故障修复后，需要人为手工执行change master to连接现有主服务器

      mysql>  CHANGE MASTER TO
          ->  MASTER_HOST='192.168.175.101',
          ->  MASTER_PORT=3306,
          ->  MASTER_USER='repluser',
          ->  MASTER_PASSWORD='WWW.1.rep',
          ->  MASTER_AUTO_POSITION=1 ; #因为是基于 gtid, 所有启用 MASTER_AUTO_POSITION 功能自动确定 replication 所需的坐标信息
      Query OK, 0 rows affected, 2 warnings (0.03 sec)



mysql> start slave;


mysql> show slave hosts;
      +-----------+------+------+-----------+--------------------------------------+
      | Server_id | Host | Port | Master_id | Slave_UUID                           |
      +-----------+------+------+-----------+--------------------------------------+
      |       102 |      | 3306 |       101 | f9eb741e-aab0-11e9-9ee7-000c29f6f083 |
      |       100 |      | 3306 |       101 | e20ebf76-aab0-11e9-b48a-000c29152d2e |
      |       103 |      | 3306 |       101 | 0b310aec-aab1-11e9-9f2a-000c2982ac0f |
      +-----------+------+------+-----------+--------------------------------------+


通过如上的试验, 可以观察到, 使用 gtid, 还可以 简化 恢复过程.

主从复制修复完成后，需要手工启动MHA_manager， 启动时需要将其工作目录下的app1.failover.complete删除






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





















---------------------------------------------------------------------------------------------------
网上资料:


网上各种安装方式:
      http://morecoder.com/article/1051165.html
      https://www.fuwuqizhijia.com/mysql/201705/86753.html
      https://blog.csdn.net/crasheye/article/details/51479121
      http://www.pianshen.com/article/130667257/
      http://www.voidcn.com/article/p-vvodeyhv-bsc.html
      http://www.aichengxu.com/mysql/7979050.htm
      https://codeleading.com/article/1276388701/
      https://blog.engineer.adways.net/entry/22109793
      http://www.qingpingshan.com/shujuku/mysql/264931.html


https://www.jianshu.com/p/5f422e85318d
https://mizzy.org/blog/2013/02/06/1/
https://www.jianshu.com/p/3ef3fc3c9113


How to automatically restart a linux background process if it fails?
    https://superuser.com/questions/507576/how-to-automatically-restart-a-linux-background-process-if-it-fails









