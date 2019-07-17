
多源复制, 可理解为 多主一从

   注: 该示例 只是 一个 简单的 示例, 实际环境中 可能 还 需要考虑 更多的 情况

准备 实现 环境用的 3 台 主机:
master01: 192.168.175.101
master02: 192.168.175.102
slave:    192.168.175.103

小心点: create user 时 一定要小心,多考虑, 最好参考使用如下的 步骤 和 语句形式 来 创建 用户:
      mysql> USE mysql;
      mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
      mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.103';       授予 该用户 replication slave 权限


---------------------------------------------------------------------------------------------------
搭建 本地 yum repo 服务器

因为 外网 网速 太慢, 所有这次 准备自己 搭建 一台 简单的 local yum repo 服务器, 通过该 server 安装 mysql 软件.
具体步骤见:
      https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver

---------------------------------------------------------------------------------------------------
master01 上 安装 mysql

// 配置 本地 yum 源, 参考 https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver
[root@master01 ~]# vim /etc/yum.repos.d/000-local-yum.repo

        [000-local-yum]
        name=000-local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0



[root@master01 ~]# yum repolist | grep local-yum
[root@master01 ~]# yum clean metadata
[root@master01 ~]# yum -y install mysql-community-server

[root@master01 ~]# rpm -q mysql-community-server
[root@master01 ~]# yum list installed  mysql-community-server

[root@master01 ~]# systemctl start mysqld
[root@master01 ~]# systemctl enable mysqld.service
[root@master01 ~]# systemctl status mysqld.service

[root@master01 ~]# grep 'temporary password' /var/log/mysqld.log
        2019-07-16T07:52:45.755184Z 1 [Note] A temporary password is generated for root@localhost: M&ad)((tD0Y2

[root@master01 ~]# mysql -u root -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit

[root@master01 ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2067/mysqld

[root@master01 ~]# ps -elf | grep mysql
    1 S mysql      2067      1  0  80   0 - 279982 poll_s 15:52 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


---------------------------------------------------------------------------------------------------
在 master02, slave 上安装 mysql, 方法 与 如上 master01 安装方法一样 (此处略)




---------------------------------------------------------------------------------------------------
// 开始正式 配置 与 replication 相关的 设置

--------------------
master01 相关配置

[root@master01 ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          default-character-set = utf8mb4

          [mysql]
          default-character-set = utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=master01-bin
          server-id=101   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency



// 重启 mysql server, 以 应用 如上的配置
[root@master01 ~]# systemctl restart mysqld


// 创建 专用于 replication 的 user. 参见 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
// 注:
//     create user 的步骤有 许多 问题 或 细节要考虑, 所以为了 最大的 灵活性, 最好 按部就班 的 按如下的 步骤 和 语法
//     来 创建用户(尤其是 涉及 replication 的 拓扑结构中), 具体原因见 该 文档 最后的 一些 笔记
//     或 参考   http://www.unixfbi.com/155.html   中 “复制账号重复问题”
mysql> USE mysql;
mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.103';       授予 该用户 replication slave 权限

     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.


-----------------------------------------------------------------------------
master02 相关配置:

[root@master02 ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          default-character-set = utf8mb4

          [mysql]
          default-character-set = utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=master02-bin
          server-id=102   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency



// 重启 mysql server, 以 应用 如上的配置
[root@master02 ~]# systemctl restart mysqld

// 创建 专用于 replication 的 user. 参见 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
// 注:
//     create user 的步骤有 许多 问题 或 细节要考虑, 所以为了 最大的 灵活性, 最好 按部就班 的 按如下的 步骤 和 语法
//     来 创建用户(尤其是 涉及 replication 的 拓扑结构中), 具体原因见 该 文档 最后的 一些 笔记
//     或 参考   http://www.unixfbi.com/155.html   中 “复制账号重复问题”
mysql> USE mysql;
mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.103';       授予 该用户 replication slave 权限


     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.


-----------------------------------------------------------------------------
slave 相关配置:

[root@slave ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          default-character-set = utf8mb4

          [mysql]
          default-character-set = utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=slave-bin
          server-id=103   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency

          # slave 必须配置为 基于 TABLE 的 repositories
          # Slaves in a multi-source replication topology require TABLE based repositories.
          # 见  https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-multi-source-configuration.html
          master_info_repository=TABLE
          relay_log_info_repository=TABLE



// 重启 mysql server, 以 应用 如上的配置
[root@slave ~]# systemctl restart mysqld




// 在 slave 上设置 每个 master 的信息 (即 到 master01 和 master02 的 连接, 认证 和 replication 的坐标信息 及 channel)
// 多源复制 必须 使用 FOR CHANNEL channel 子句来指定 使用的 channel. channel 代表 transactions 从 master 流向 slave 的 path.
//  见 https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-multi-source-adding-gtid-master.html
mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.175.101',
    -> MASTER_PORT=3306,
    -> MASTER_USER='repluser',
    -> MASTER_PASSWORD='WWW.1.com',
    -> MASTER_AUTO_POSITION=1 FOR CHANNEL 'master-01';    # 将 master01 加到 名为 'master-01' 的 channel 中

mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.175.102',
    -> MASTER_PORT=3306,
    -> MASTER_USER='repluser',
    -> MASTER_PASSWORD='WWW.1.com',
    -> MASTER_AUTO_POSITION=1 FOR CHANNEL 'master-02';    # 将 master02 加到 名为 'master-02' 的 channel 中


// 看一下 如上的 设置
mysql> pager less -Fi
mysql> show slave status\G

// 看一下 与 slave 相关的表
mysql> show tables from mysql like 'slave%';
      +--------------------------+
      | Tables_in_mysql (slave%) |
      +--------------------------+
      | slave_master_info        |
      | slave_relay_log_info     |
      | slave_worker_info        |
      +--------------------------+


// 启动 slave 线程(io_thread , sql_thread),
// 见 https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-multi-source-start-slave.html
mysql> start slave;    # 该命令 会 启动 所有 channel 上 所有 类型的 的 thread


mysql> show slave status\G

              *************************** 1. row ***************************
                             Slave_IO_State: Waiting for master to send event
                                Master_Host: 192.168.175.101
                                Master_User: repluser
                                Master_Port: 3306
                              Connect_Retry: 60
                            Master_Log_File: master01-bin.000001
                        Read_Master_Log_Pos: 655
                             Relay_Log_File: slave-relay-bin-master@002d01.000002
                              Relay_Log_Pos: 874
                      Relay_Master_Log_File: master01-bin.000001
                           Slave_IO_Running: Yes   <----------
                          Slave_SQL_Running: Yes   <----------
                            Replicate_Do_DB:
                        Replicate_Ignore_DB:
                         Replicate_Do_Table:
                     Replicate_Ignore_Table:
                    Replicate_Wild_Do_Table:
                Replicate_Wild_Ignore_Table:
                                 Last_Errno: 0
                                 Last_Error:
                               Skip_Counter: 0
                        Exec_Master_Log_Pos: 655
                            Relay_Log_Space: 1095
                            Until_Condition: None
                             Until_Log_File:
                              Until_Log_Pos: 0
                         Master_SSL_Allowed: No
                         Master_SSL_CA_File:
                         Master_SSL_CA_Path:
                            Master_SSL_Cert:
                          Master_SSL_Cipher:
                             Master_SSL_Key:
                      Seconds_Behind_Master: 0
              Master_SSL_Verify_Server_Cert: No
                              Last_IO_Errno: 0
                              Last_IO_Error:
                             Last_SQL_Errno: 0
                             Last_SQL_Error:
                Replicate_Ignore_Server_Ids:
                           Master_Server_Id: 101
                                Master_UUID: 8ab7c026-a860-11e9-9c5d-000c29528e39
                           Master_Info_File: mysql.slave_master_info
                                  SQL_Delay: 0
                        SQL_Remaining_Delay: NULL
                    Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
                         Master_Retry_Count: 86400
                                Master_Bind:
                    Last_IO_Error_Timestamp:
                   Last_SQL_Error_Timestamp:
                             Master_SSL_Crl:
                         Master_SSL_Crlpath:
                         Retrieved_Gtid_Set: 8ab7c026-a860-11e9-9c5d-000c29528e39:1-2
                          Executed_Gtid_Set: 8ab7c026-a860-11e9-9c5d-000c29528e39:1-2,
              8e8d2dcd-a860-11e9-95d1-000c294b426a:1-2
                              Auto_Position: 1
                       Replicate_Rewrite_DB:
                               Channel_Name: master-01
                         Master_TLS_Version:
              *************************** 2. row ***************************
                             Slave_IO_State: Waiting for master to send event
                                Master_Host: 192.168.175.102
                                Master_User: repluser
                                Master_Port: 3306
                              Connect_Retry: 60
                            Master_Log_File: master02-bin.000001
                        Read_Master_Log_Pos: 655
                             Relay_Log_File: slave-relay-bin-master@002d02.000002
                              Relay_Log_Pos: 874
                      Relay_Master_Log_File: master02-bin.000001
                           Slave_IO_Running: Yes    <----------
                          Slave_SQL_Running: Yes    <----------
                            Replicate_Do_DB:
                        Replicate_Ignore_DB:
                         Replicate_Do_Table:
                     Replicate_Ignore_Table:
                    Replicate_Wild_Do_Table:
                Replicate_Wild_Ignore_Table:
                                 Last_Errno: 0
                                 Last_Error:
                               Skip_Counter: 0
                        Exec_Master_Log_Pos: 655
                            Relay_Log_Space: 1095
                            Until_Condition: None
                             Until_Log_File:
                              Until_Log_Pos: 0
                         Master_SSL_Allowed: No
                         Master_SSL_CA_File:
                         Master_SSL_CA_Path:
                            Master_SSL_Cert:
                          Master_SSL_Cipher:
                             Master_SSL_Key:
                      Seconds_Behind_Master: 0
              Master_SSL_Verify_Server_Cert: No
                              Last_IO_Errno: 0
                              Last_IO_Error:
                             Last_SQL_Errno: 0
                             Last_SQL_Error:
                Replicate_Ignore_Server_Ids:
                           Master_Server_Id: 102
                                Master_UUID: 8e8d2dcd-a860-11e9-95d1-000c294b426a
                           Master_Info_File: mysql.slave_master_info
                                  SQL_Delay: 0
                        SQL_Remaining_Delay: NULL
                    Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
                         Master_Retry_Count: 86400
                                Master_Bind:
                    Last_IO_Error_Timestamp:
                   Last_SQL_Error_Timestamp:
                             Master_SSL_Crl:
                         Master_SSL_Crlpath:
                         Retrieved_Gtid_Set: 8e8d2dcd-a860-11e9-95d1-000c294b426a:1-2
                          Executed_Gtid_Set: 8ab7c026-a860-11e9-9c5d-000c29528e39:1-2,
              8e8d2dcd-a860-11e9-95d1-000c294b426a:1-2
                              Auto_Position: 1
                       Replicate_Rewrite_DB:
                               Channel_Name: master-02
                         Master_TLS_Version:




---------------------------------------------------------------------------------------------------



---------------------------------------------------------------------------------------------------

随便测试一下:

master01 上创建 db_m01:
    mysql> CREATE DATABASE db_m01 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


master02 上创建 db_m02:
    mysql> CREATE DATABASE db_m02 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


slave 上 查看 如上 创建的 databases 是否 被 replicated 过来:
    mysql> show databases;
          +--------------------+
          | Database           |
          +--------------------+
          | information_schema |
          | db_m01             | <-----
          | db_m02             | <-----
          | mysql              |
          | performance_schema |
          | sys                |
          +--------------------+




---------------------------------------------------------------------------------------------------


https://dinfratechsource.com/2018/11/10/multi-source-replication-in-mysql-5-7/


https://severalnines.com/blog/multi-source-replication-mariadb-galera-cluster
https://dzone.com/articles/high-availability-with-multi-source-replication-in

http://www.unixfbi.com/155.html
https://www.hi-linux.com/posts/61083.html
http://www.yangchengec.cn/setup/527.html
https://yq.aliyun.com/articles/516644


https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-multi-source-tutorials.html
https://juejin.im/entry/5bf7731351882518805ac985










---------------------------------------------------------------------------------------------------

与 create user 和 过滤 复制的 database 有关的问题:

  http://www.unixfbi.com/155.html
  https://yq.aliyun.com/articles/516644

  https://dev.mysql.com/doc/refman/5.7/en/replication-options-slave.html#option_mysqld_replicate-ignore-db

  https://dba.stackexchange.com/questions/28551/mysql-replication-and-ignore-tables
  https://stackoverflow.com/questions/18830964/filter-mysql-replication-ignore-db
  https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
    ---------------------------------------

      binlog-ignore-db
      replicate-ignore-db

          binlog-ignore-db is a master-side setting, it tells the Master not to log changes taking place on the listed DB.

          replicate-ignore-db is a slave-side setting, it tells the Slave to ignore incoming log information related to the listed DB

          The typical use case is when you want to replicate different databases
          from onesingle Master to different Slaves. The Master must log all changes occurring in all databases
          (minus those possibly excluded by binlog-ignore-db, i.e. database that will not be replicated anywhere).

          Each Slave will receive the full binary log, but will only replicate changes related to the selected databases
          (i.e. databases not excluded by replicate-ignore-db -- this list would be different on each Slave).

          (mysql database being a system database, it should be ignored from both ends, unless you really, really really know what you are doing).

    ---------------------------------------

   https://dev.mysql.com/doc/refman/5.7/en/change-replication-filter.html

   https://dev.mysql.com/doc/refman/5.7/en/replication-rules.html
      16.2.5 How Servers Evaluate Replication Filtering Rules
           If a master server does not write a statement to its binary log,
           the statement is not replicated. If the server does log the statement,
           the statement is sent to all slaves and each slave determines whether to execute it or ignore it.

    一些帮助命令:
        [root@slave ~]# mysqld --verbose --help | grep replica
        mysql> help CHANGE REPLICATION FILTER;

   https://dev.mysql.com/doc/refman/5.7/en/replication-rules.html

单个的 'change replication filter' 语句 可以指定 Multiple replication filtering rules.
通过 逗号(commas) 将它们分隔开:
    CHANGE REPLICATION FILTER REPLICATE_DO_DB = (d1), REPLICATE_IGNORE_DB = (d2);
如上语句等价于 在 启动 slave 的 mysqld 时 指定如下选项:
       --replicate-do-db=d1 --replicate-ignore-db=d2

如果相同的 filtering rule 被指定了 multiple times, 则仅 最后的 rule 会被 实际使用.
原文:
      If the same filtering rule is specified multiple times, only the last such rule is actually used.
      For example, the two statements shown here have exactly the same effect,
      because the first REPLICATE_DO_DB rule in the first statement is ignored:

    CHANGE REPLICATION FILTER REPLICATE_DO_DB = (db1, db2), REPLICATE_DO_DB = (db3, db4); # <---- 等价于如下语句
    CHANGE REPLICATION FILTER REPLICATE_DO_DB = (db3,db4);     # <----------------------  等价于如上语句
    如上两条语句 具有 相同的效果, 因为 第 1 条语句中
    过滤规则 REPLICATE_DO_DB = (db1, db2) 与 过滤规则 REPLICATE_DO_DB = (db3, db4) 相同,
    所以 前面的 过滤规则 REPLICATE_DO_DB = (db1, db2) 会被 ignored, 只会 使用 the last 的
    过滤规则 REPLICATE_DO_DB = (db3, db4).

  小心:
      这种 行为 和 specifying the same option multiple times 的 --replicate-* filter options 的行为是不同的,
      因为后者 会导致 the creation of multiple filter rules.

      ------------------ 更多信息 和 细节 见官网: https://dev.mysql.com/doc/refman/5.7/en/change-replication-filter.html
        CHANGE REPLICATION FILTER filter[, filter][, ...]

        filter:
            REPLICATE_DO_DB = (db_list)
          | REPLICATE_IGNORE_DB = (db_list)
          | REPLICATE_DO_TABLE = (tbl_list)
          | REPLICATE_IGNORE_TABLE = (tbl_list)
          | REPLICATE_WILD_DO_TABLE = (wild_tbl_list)
          | REPLICATE_WILD_IGNORE_TABLE = (wild_tbl_list)
          | REPLICATE_REWRITE_DB = (db_pair_list)

      ------------------

(server 计算 复制 过滤规则的方式)   16.2.5 How Servers Evaluate Replication Filtering Rules
https://dev.mysql.com/doc/refman/5.7/en/replication-rules.html
master 可配置的一下选项(但不推荐这么做, 必要时应该 在 slave 上使用 filtering 来控制 那些 events 应该在slave 上被执行):
          --binlog-do-db
          --binlog-ignore-db

16.1.6 Replication and Binary Logging Options and Variables
    https://dev.mysql.com/doc/refman/5.7/en/replication-options.html   (查看 slave上 --replicate-* options)

注意: Note that replication filters cannot be used on a MySQL server instance that is configured for Group Replication,
      because filtering transactions on some servers would make the group unable to reach agreement on a consistent state.

Database-level options (--replicate-do-db, --replicate-ignore-db) are checked first;

[root@slave ~]# mysqld --verbose --help | grep -E --  '--replicate'
      --replicate-do-db=name       <--- Database-level options (数据库级别的 选项)
      --replicate-do-table=name
      --replicate-ignore-db=name   <--- Database-level options
      --replicate-ignore-table=name
      --replicate-rewrite-db=name
      --replicate-same-server-id
      --replicate-wild-do-table=name
      --replicate-wild-ignore-table=name


To make it easier to determine what effect an option set will have,
it is recommended that you avoid mixing “do” and “ignore” options, or wildcard and nonwildcard options.

If any --replicate-rewrite-db options were specified, they are applied before the --replicate-* filtering rules are tested.


16.2.5.1 Evaluation of Database-Level Replication and Binary Logging Options
            https://dev.mysql.com/doc/refman/5.7/en/replication-rules-db-options.html

      ----------------该段文字摘自 http://www.unixfbi.com/155.html
      2.复制账号重复问题
      方法一：

      set  sql_log_bin=0;
      grant all privileges on ....;
      set sql_log_bin=1;
      创建用户时，不管是否使用 use mysql;新创建的用户都不会复制到从库；
      方法二：

      stop slave sql_thread; change replication filter Replicate_ignore_DB=(mysql);
      创建用户时，先执行 use mysql; 然后再 create user XXX; 否则新创建的用户还是会复制到从库；
      ---------------------
        Note (这段文字 可以解释 如上提到的 为什么 create user 时 先执行 use mysql)
          Only DML statements can be logged using the row format. DDL statements are always logged as statements,
          even when binlog_format=ROW. All DDL statements are therefore always filtered according to the rules
          for statement-based replication. This means that you must select the default database explicitly
          with a USE statement in order for a DDL statement to be applied.

      仅 DML statements 能够被 使用 the row format 被 logged.
      而 所有的 DDL 语句 总是被 作为 statements 被 logged. 即使 将 binlog_format 配置为 ROW. 所以 所有的 DDL 语句 总是根据
      statement-based replication 的 规则被过滤. 这意味着 你 必须 使用 use 语句 明确的 select the default database
      以使  a DDL statement 被应用.


      [root@slave ~]# mysqld --verbose --help | grep ^binlog-format
              binlog-format                                                ROW
          ----------
          binlog_format 默认值: https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_binlog_format
              Default Value (>= 5.7.7)  ROW
              Default Value (<= 5.7.6)  STATEMENT
          ----------

--replicate-do-db
https://stackoverflow.com/questions/12086049/mysql-db-in-replication-but-users-created-on-master-are-not-replicating-on-slave

---------------------------------------------------------------------------------------------------
网上资料:

16.1.4.1 MySQL Multi-Source Replication Overview
      https://dev.mysql.com/doc/refman/5.7/en/replication-multi-source-overview.html

16.2.3 Replication Channels
      https://dev.mysql.com/doc/refman/5.7/en/replication-channels.html


13.4.1.2 RESET MASTER Syntax
      https://dev.mysql.com/doc/refman/5.7/en/reset-master.html

13.4.2.4 RESET SLAVE Syntax
      https://dev.mysql.com/doc/refman/5.7/en/reset-slave.html



