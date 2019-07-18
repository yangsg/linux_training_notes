

半同步复制 Semisynchronous Replication

       该 示例仅 演示 最简单的 semi-sync replication 搭建, 更复杂的场景 还需要做 更多的考虑

准备 实现 环境用的 3 台 主机:
master:  192.168.175.100
slave01: 192.168.175.101
slave02: 192.168.175.102

总体步骤:
    1. 先搭建 基本的 one master to two slaves 的 replication 拓扑环境
    2. 设置 启用 Semisynchronous Replication

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
1. 先搭建 基本的 one master to two slaves 的 replication 拓扑环境

// 开始正式 配置 与 replication 相关的 设置(此时不包含 semi-sync replication 的 设置 )

--------------------
master 端 replication 设置 (此时不包含 semi-sync replication 的 设置)

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

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=master-bin
          server-id=100   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency


// 重启 mysql server, 以 应用 如上的配置
[root@master ~]# systemctl restart mysqld


// 创建 专用于 replication 的 user. 参见 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
// 注:
//     create user 的步骤有 许多 问题 或 细节要考虑, 所以为了 最大的 灵活性, 最好 按部就班 的 按如下的 步骤 和 语法
//     来 创建用户(尤其是 涉及 replication 的 拓扑结构中), 具体原因见
//     https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/003-gtid-utf8mb4-rpm-multi-source-replication
//     或 参考   http://www.unixfbi.com/155.html   中 “复制账号重复问题”
mysql> USE mysql;
mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.101' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.101';       授予 该用户 replication slave 权限

mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.102' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.102';       授予 该用户 replication slave 权限

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

// 查看一下 状态信息
mysql> show master status;
      +-------------------+----------+--------------+------------------+------------------------------------------+
      | File              | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
      +-------------------+----------+--------------+------------------+------------------------------------------+
      | master-bin.000001 |     1156 |              |                  | abeb8ed5-a946-11e9-a9a6-000c29528e39:1-4 |
      +-------------------+----------+--------------+------------------+------------------------------------------+



--------------------
slave01 端 replication 设置 (此时不包含 semi-sync replication 的 设置)


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



// 先 通过 命令 mysqld 查看一下 配置
[root@slave01 ~]# mysqld --verbose --help | grep -E '^(log-bin |server-id |gtid-mode|enforce-gtid-consistency)'
        enforce-gtid-consistency                                     true
        gtid-mode                                                    ON
        log-bin                                                      slave01-bin
        server-id                                                    101


// 重启 slave01 的 mysql server 是 如上配置生效
[root@slave01 ~]# systemctl restart mysqld


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
    -> MASTER_PASSWORD='WWW.1.com',
    -> MASTER_AUTO_POSITION=1 ; #因为是基于 gtid, 所有启用 MASTER_AUTO_POSITION 功能自动确定 replication 所需的坐标信息

// 启动 slave 的 io_thread 和 sql_thread
mysql> start slave;


mysql> pager less -Fi
mysql> show slave status\G


----------------------------------------------------------------

slave02 端 replication 设置 (此时不包含 semi-sync replication 的 设置)


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



// 先 通过 命令 mysqld 查看一下 配置
[root@slave02 ~]# mysqld --verbose --help | grep -E '^(log-bin |server-id |gtid-mode|enforce-gtid-consistency)'
          enforce-gtid-consistency                                     true
          gtid-mode                                                    ON
          log-bin                                                      slave02-bin
          server-id                                                    102


// 重启 slave02 的 mysql server 是 如上配置生效
[root@slave02 ~]# systemctl restart mysqld


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
    -> MASTER_PASSWORD='WWW.1.com',
    -> MASTER_AUTO_POSITION=1 ; #因为是基于 gtid, 所有启用 MASTER_AUTO_POSITION 功能自动确定 replication 所需的坐标信息

// 启动 slave 的 io_thread 和 sql_thread
mysql> start slave;


mysql> pager less -Fi
mysql> show slave status\G









---------------------------------------------------------------------------------------------------
2. 设置 启用 Semisynchronous Replication


--------------------

master 端 的 semi-sync replication 设置


注: 启用 半同步 复制前 必须 先 安装其 对应的 半同步复制 插件

// 安装 半同步 复制 的 master 端 插件 semisync_master.so
mysql> INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';

// 验证 插件 semisync_master.so 的安装 (还 可以使用 语句 SHOW PLUGINS 查看)
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
      +----------------------+---------------+
      | PLUGIN_NAME          | PLUGIN_STATUS |
      +----------------------+---------------+
      | rpl_semi_sync_master | ACTIVE        |
      +----------------------+---------------+


// 演示一下 在 运行时(at runtime, 即 动态)  如何启用 rpl_semi_sync_master 插件 (注: 此时这些修改 仅在 当前运行的 mysqld 进程中有效)
mysql> SET GLOBAL rpl_semi_sync_master_enabled = 1;
mysql> SET GLOBAL rpl_semi_sync_master_timeout = 1000;

// 查看修改后 相关的 'rpl_semi_sync%' 配置
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
        +-------------------------------------------+------------+
        | Variable_name                             | Value      |
        +-------------------------------------------+------------+
        | rpl_semi_sync_master_enabled              | ON         |  <------
        | rpl_semi_sync_master_timeout              | 1000       |
        | rpl_semi_sync_master_trace_level          | 32         |
        | rpl_semi_sync_master_wait_for_slave_count | 1          |
        | rpl_semi_sync_master_wait_no_slave        | ON         |
        | rpl_semi_sync_master_wait_point           | AFTER_SYNC |
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
        | Rpl_semi_sync_master_status                | ON    |  <------
        | Rpl_semi_sync_master_timefunc_failures     | 0     |
        | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
        | Rpl_semi_sync_master_tx_wait_time          | 0     |
        | Rpl_semi_sync_master_tx_waits              | 0     |
        | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
        | Rpl_semi_sync_master_wait_sessions         | 0     |
        | Rpl_semi_sync_master_yes_tx                | 0     |
        +--------------------------------------------+-------+


// 在 /etc/my.cnf 中 添加 semi-sync replication 的配置
[root@master ~]# vim /etc/my.cnf

          # 如下 2 行 是与 半同步复制 相关的设置
          # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
          rpl_semi_sync_master_enabled=1    # 启用 master 的 semi-sync replication功能 # 默认为 0 即关闭
          rpl_semi_sync_master_timeout=1000 # 1 second # 默认为 10 seconds

          # 更多 与 半同步复制 相关的 系统变量 或 状态变量 见:
          #    https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html


// 重启 master 的 mysql server 使 如上配置生效
[root@master ~]# systemctl restart mysqld

// 观察 重启后 相关 'rpl_semi_sync%' 变量
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
          +-------------------------------------------+------------+
          | Variable_name                             | Value      |
          +-------------------------------------------+------------+
          | rpl_semi_sync_master_enabled              | ON         | <------
          | rpl_semi_sync_master_timeout              | 1000       |
          | rpl_semi_sync_master_trace_level          | 32         |
          | rpl_semi_sync_master_wait_for_slave_count | 1          |
          | rpl_semi_sync_master_wait_no_slave        | ON         |
          | rpl_semi_sync_master_wait_point           | AFTER_SYNC |
          +-------------------------------------------+------------+


// 观察 重启后  相关 'Rpl_semi_sync%' 状态变量 
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
          | Rpl_semi_sync_master_status                | ON    | <------
          | Rpl_semi_sync_master_timefunc_failures     | 0     |
          | Rpl_semi_sync_master_tx_avg_wait_time      | 0     |
          | Rpl_semi_sync_master_tx_wait_time          | 0     |
          | Rpl_semi_sync_master_tx_waits              | 0     |
          | Rpl_semi_sync_master_wait_pos_backtraverse | 0     |
          | Rpl_semi_sync_master_wait_sessions         | 0     |
          | Rpl_semi_sync_master_yes_tx                | 0     |
          +--------------------------------------------+-------+




--------------------

slave01 端 的 semi-sync replication 设置

注: 启用 半同步 复制前 必须 先 安装其 对应的 半同步复制 插件

// 安装 半同步 复制 的 slave 端 插件 semisync_slave.so
mysql> INSTALL PLUGIN rpl_semi_sync_slave SONAME 'semisync_slave.so';

// 验证 插件 semisync_slave.so 的安装 (还 可以使用 语句 SHOW PLUGINS 查看)
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
        +---------------------+---------------+
        | PLUGIN_NAME         | PLUGIN_STATUS |
        +---------------------+---------------+
        | rpl_semi_sync_slave | ACTIVE        |
        +---------------------+---------------+

// 演示一下 在 运行时(at runtime, 即 动态)  如何启用 rpl_semi_sync_slave 插件 (注: 此时这些修改 仅在 当前运行的 mysqld 进程中有效)
mysql> SET GLOBAL rpl_semi_sync_slave_enabled = 1;


// 重新启动 slave 的 I/O 线程, 让 slave 重新连接 master 以使 自己 作为 a semisynchronous slave 被注册
mysql> STOP SLAVE IO_THREAD;
mysql> START SLAVE IO_THREAD;

// 观察 slave01 上 相关的 'rpl_semi_sync%' 变量
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
        +---------------------------------+-------+
        | Variable_name                   | Value |
        +---------------------------------+-------+
        | rpl_semi_sync_slave_enabled     | ON    |  <-----
        | rpl_semi_sync_slave_trace_level | 32    |
        +---------------------------------+-------+

// 观察 slave01 上 相关的 'Rpl_semi_sync%' 状态变量
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
        +----------------------------+-------+
        | Variable_name              | Value |
        +----------------------------+-------+
        | Rpl_semi_sync_slave_status | ON    |  <-----
        +----------------------------+-------+

// 此时 在 master 端 执行 如下 语句 看一下 master 端相关 'Rpl_semi_sync%' 状态 变化
            mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';    #<---- 注: 此语句在 master 端 执行
            +--------------------------------------------+-------+
            | Variable_name                              | Value |
            +--------------------------------------------+-------+
            | Rpl_semi_sync_master_clients               | 1     | <------
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
            +--------------------------------------------+-------+




// 在 /etc/my.cnf 中 添加 semi-sync replication 的配置
[root@slave01 ~]# vim /etc/my.cnf

          [mysqld]
          # 半同步复制 相关的设置
          # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
          rpl_semi_sync_slave_enabled=1    # 启用 slave 的 semi-sync replication功能 # 默认为 0 即关闭

          # 更多 与 半同步复制 相关的 系统变量 或 状态变量 见:
          #    https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html


// 重启 slave01 的 mysql server 是 如上配置生效
[root@slave01 ~]# systemctl restart mysqld


// 观察 重启后 slave01 上 相关的 'rpl_semi_sync%' 变量
mysql> SHOW VARIABLES LIKE 'rpl_semi_sync%';
        +---------------------------------+-------+
        | Variable_name                   | Value |
        +---------------------------------+-------+
        | rpl_semi_sync_slave_enabled     | ON    |   <-----
        | rpl_semi_sync_slave_trace_level | 32    |
        +---------------------------------+-------+

// 观察 重启后 slave01 上 相关的 'Rpl_semi_sync%' 状态变量
mysql> SHOW STATUS LIKE 'Rpl_semi_sync%';
        +----------------------------+-------+
        | Variable_name              | Value |
        +----------------------------+-------+
        | Rpl_semi_sync_slave_status | ON    |  <-----
        +----------------------------+-------+


mysql> pager less -Fi
mysql> start slave;




---------------------------------------------------------------------------------------------------
网上资料:

16.3.9 Semisynchronous Replication
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html

16.3.9.1 Semisynchronous Replication Administrative Interface
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html

16.3.9.2 Semisynchronous Replication Installation and Configuration
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html

      5.5.1 Installing and Uninstalling Plugins
            https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html

16.3.9.3 Semisynchronous Replication Monitoring
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-monitoring.html


MySQL Replication Best Practices (mysql 复制 最佳实践)
https://www.percona.com/sites/default/files/presentations/Replication-webinar.pdf



