
ip信息：
    master: 192.168.175.100/24
    slave:  192.168.175.101/24

---------------------------------------------------------------------------------------------------
前期一些其他准备:

// 设置时区, 同步时间:
      https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/001-one-master-to-one-slave-simplest

// 为熵池 提供一个好的 采集方案:
      https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/01-full/031-rngd.txt

---------------------------------------------------------------------------------------------------
master server 端:

// 安装 mysql 参考  https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_01_install/mysql_install_from_rpm_5.7
[root@master ~]# mkdir download && cd download
[root@master download]# wget --no-check-certificate https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@master download]# yum -y install mysql80-community-release-el7-2.noarch.rpm
[root@master download]# ls /etc/yum.repos.d/ | grep mysql
        mysql-community.repo
        mysql-community-source.repo


[root@master download]# yum repolist all | grep mysql
          mysql-cluster-7.5-community/x86_64 MySQL Cluster 7.5 Community   disabled
          mysql-cluster-7.5-community-source MySQL Cluster 7.5 Community - disabled
          mysql-cluster-7.6-community/x86_64 MySQL Cluster 7.6 Community   disabled
          mysql-cluster-7.6-community-source MySQL Cluster 7.6 Community - disabled
          mysql-connectors-community/x86_64  MySQL Connectors Community    enabled:    108
          mysql-connectors-community-source  MySQL Connectors Community -  disabled
          mysql-tools-community/x86_64       MySQL Tools Community         enabled:     90
          mysql-tools-community-source       MySQL Tools Community - Sourc disabled
          mysql-tools-preview/x86_64         MySQL Tools Preview           disabled
          mysql-tools-preview-source         MySQL Tools Preview - Source  disabled
          mysql55-community/x86_64           MySQL 5.5 Community Server    disabled
          mysql55-community-source           MySQL 5.5 Community Server -  disabled
          mysql56-community/x86_64           MySQL 5.6 Community Server    disabled
          mysql56-community-source           MySQL 5.6 Community Server -  disabled
          mysql57-community/x86_64           MySQL 5.7 Community Server    disabled
          mysql57-community-source           MySQL 5.7 Community Server -  disabled
          mysql80-community/x86_64           MySQL 8.0 Community Server    enabled:    113
          mysql80-community-source           MySQL 8.0 Community Server -  disabled


[root@master download]# vim /etc/yum.repos.d/mysql-community.repo
      # Enable to use MySQL 5.7
      [mysql57-community]
      name=MySQL 5.7 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
      #// enabled=1 表示启用仓库
      enabled=1
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

      [mysql80-community]
      name=MySQL 8.0 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/7/$basearch/
      #// enabled=0 表示禁用仓库
      enabled=0
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql


[root@master ~]# yum repolist enabled | grep mysql
      mysql-connectors-community/x86_64 MySQL Connectors Community                 108
      mysql-tools-community/x86_64      MySQL Tools Community                       90
      mysql57-community/x86_64          MySQL 5.7 Community Server                 347


[root@master ~]# yum -y install mysql-community-server

[root@master ~]# rpm -q mysql-community-server
    mysql-community-server-5.7.26-1.el7.x86_64


[root@master ~]# systemctl start mysqld.service
[root@master ~]# systemctl enable mysqld.service
[root@master ~]# systemctl status mysqld.service

[root@master ~]# grep 'temporary password' /var/log/mysqld.log
        2019-07-15T03:53:34.998263Z 1 [Note] A temporary password is generated for root@localhost: -0py_-q=pPwz

[root@master ~]# mysql -u root -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit


[root@master ~]# netstat -anptu  | grep mysql
tcp6       0      0 :::3306                 :::*                    LISTEN      17897/mysqld

[root@master ~]# ps -elf | grep mysql
1 S mysql     17897      1  0  80   0 - 279982 poll_s 11:53 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


// 开始正式 配置 与 replication 中 与 master 相关的配置

[root@master ~]# vim /etc/my.cnf

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
mysql> CREATE USER 'repluser'@'192.168.175.101' IDENTIFIED BY 'WWW.1.com';  # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.101';      # 授予 该用户 replication slave 全向

     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.

// 在 master 上 做一次 full backup, 后续的操作 会 将其 同步给 slave
[root@master ~]# mysqldump --help | grep -E '^default-character-set'   # 先 看一下 本机 默认情况下 mysqldump 连接 mysql server时的字符集
    default-character-set             utf8mb4   <---- 观察

[root@master ~]# mysqldump -u root -p --lock-all-tables --all-databases --master-data=2 > /root/db_full-backup.sql
        Enter password:
        Warning: A partial dump from a server that has GTIDs will by default include the GTIDs of all transactions, even those that changed suppressed parts of the database. If you don't want to restore GTIDs, pass --set-gtid-purged=OFF. To make a complete dump, pass --all-databases --triggers --routines --events.


// 将 master 的 db_full-backup.sql 拷贝给 slave
[root@master ~]# rsync -av /root/db_full-backup.sql  root@192.168.175.101:/tmp/

// 查看一下 状态信息
mysql> show master status;
      +-------------------+----------+--------------+------------------+------------------------------------------+
      | File              | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set                        |
      +-------------------+----------+--------------+------------------+------------------------------------------+
      | master-bin.000001 |      631 |              |                  | 1ea51141-a6b4-11e9-b38f-000c29f6f083:1-2 |
      +-------------------+----------+--------------+------------------+------------------------------------------+










---------------------------------------------------------------------------------------------------
slave server 端:


// slave端安装mysql
[root@slave ~]# mkdir download && cd download
[root@slave download]# wget --no-check-certificate https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@slave download]# yum -y install mysql80-community-release-el7-2.noarch.rpm
[root@slave download]# ls /etc/yum.repos.d/ | grep mysql
        mysql-community.repo
        mysql-community-source.repo

[root@slave download]# yum repolist all | grep mysql
        mysql-cluster-7.5-community/x86_64 MySQL Cluster 7.5 Community   disabled
        mysql-cluster-7.5-community-source MySQL Cluster 7.5 Community - disabled
        mysql-cluster-7.6-community/x86_64 MySQL Cluster 7.6 Community   disabled
        mysql-cluster-7.6-community-source MySQL Cluster 7.6 Community - disabled
        mysql-connectors-community/x86_64  MySQL Connectors Community    enabled:    108
        mysql-connectors-community-source  MySQL Connectors Community -  disabled
        mysql-tools-community/x86_64       MySQL Tools Community         enabled:     90
        mysql-tools-community-source       MySQL Tools Community - Sourc disabled
        mysql-tools-preview/x86_64         MySQL Tools Preview           disabled
        mysql-tools-preview-source         MySQL Tools Preview - Source  disabled
        mysql55-community/x86_64           MySQL 5.5 Community Server    disabled
        mysql55-community-source           MySQL 5.5 Community Server -  disabled
        mysql56-community/x86_64           MySQL 5.6 Community Server    disabled
        mysql56-community-source           MySQL 5.6 Community Server -  disabled
        mysql57-community/x86_64           MySQL 5.7 Community Server    disabled
        mysql57-community-source           MySQL 5.7 Community Server -  disabled
        mysql80-community/x86_64           MySQL 8.0 Community Server    enabled:    113
        mysql80-community-source           MySQL 8.0 Community Server -  disabled


[root@slave download]# vim /etc/yum.repos.d/mysql-community.repo

      # Enable to use MySQL 5.7
      [mysql57-community]
      name=MySQL 5.7 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
      #// enabled=1 表示启用仓库
      enabled=1
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

      [mysql80-community]
      name=MySQL 8.0 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/7/$basearch/
      #// enabled=0 表示禁用仓库
      enabled=0
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql


[root@slave download]# yum repolist enabled | grep mysql
      mysql-connectors-community/x86_64 MySQL Connectors Community                 108
      mysql-tools-community/x86_64      MySQL Tools Community                       90
      mysql57-community/x86_64          MySQL 5.7 Community Server                 347


[root@slave download]# yum -y install mysql-community-server

[root@slave download]# rpm -q mysql-community-server
      mysql-community-server-5.7.26-1.el7.x86_64



[root@slave ~]# systemctl start mysqld.service
[root@slave ~]# systemctl enable mysqld.service
[root@slave ~]# systemctl status mysqld.service


[root@slave ~]# grep 'temporary password' /var/log/mysqld.log
      2019-07-15T05:37:41.165239Z 1 [Note] A temporary password is generated for root@localhost: -n;>ad/(f27J



mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
mysql> quit

[root@slave ~]# netstat -anptu  | grep mysql
      tcp6       0      0 :::3306                 :::*                    LISTEN      17755/mysqld

[root@slave ~]# ps -elf | grep mysql
      1 S mysql     17755      1  0  80   0 - 279982 poll_s 13:37 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid



// 开始正式 设置 slave 中 与 replication 相关的 设置. 参考 https://dev.mysql.com/doc/refman/5.7/en/replication-setup-slaves.html

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
          server-id=101   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency



// 先 通过 命令 mysqld 查看一下 配置
[root@slave ~]# mysqld --verbose --help | grep -E '^(log-bin |server-id |gtid-mode|enforce-gtid-consistency)'
        enforce-gtid-consistency                                     true
        gtid-mode                                                    ON
        log-bin                                                      slave-bin
        server-id                                                    101

// 重启 slave 的 mysql server 是 如上配置生效
[root@slave ~]# systemctl restart mysqld


// 查看一下客户端工具 mysql 默认使用 的 字符集
[root@slave ~]# mysql --help | grep  ^default-character-set
        default-character-set             utf8mb4

// 查看一下 slave 上的 master 的 一份完全备份
[root@slave ~]# ls /tmp/db_full-backup.sql
      /tmp/db_full-backup.sql


[root@slave ~]# mysql -u root -p < /tmp/db_full-backup.sql  # 以 batch mode 还原 master 的 备份(即保持slave 初始数据与 master 一致)

[root@slave ~]# echo $?
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


// 启动 slave 线程(io thread 和 sql thead)
mysql> start slave;


mysql> pager less -Fi

// 查看 slave 状态信息
mysql> show slave status\G
                        *************************** 1. row ***************************
                                       Slave_IO_State: Waiting for master to send event
                                          Master_Host: 192.168.175.100
                                          Master_User: repluser
                                          Master_Port: 3306
                                        Connect_Retry: 60
                                      Master_Log_File: master-bin.000001
                                  Read_Master_Log_Pos: 631
                                       Relay_Log_File: slave-relay-bin.000002
                                        Relay_Log_Pos: 417
                                Relay_Master_Log_File: master-bin.000001
                                     Slave_IO_Running: Yes    <----------- 查看 io thread 状态
                                    Slave_SQL_Running: Yes    <----------- 查看 sql thread 状态
                                      Replicate_Do_DB:
                                  Replicate_Ignore_DB:
                                   Replicate_Do_Table:
                               Replicate_Ignore_Table:
                              Replicate_Wild_Do_Table:
                          Replicate_Wild_Ignore_Table:
                                           Last_Errno: 0
                                           Last_Error:
                                         Skip_Counter: 0
                                  Exec_Master_Log_Pos: 631
                                      Relay_Log_Space: 624
                                      Until_Condition: None
                                       Until_Log_File:
                                        Until_Log_Pos: 0
                                   Master_SSL_Allowed: No
                                   Master_SSL_CA_File:
                                   Master_SSL_CA_Path:
                                      Master_SSL_Cert:
                                    Master_SSL_Cipher:
                                       Master_SSL_Key:
                                Seconds_Behind_Master: 0    <------------- 延迟
                        Master_SSL_Verify_Server_Cert: No
                                        Last_IO_Errno: 0
                                        Last_IO_Error:     <---------------- 当发生错误时可以查看一下这里
                                       Last_SQL_Errno: 0
                                       Last_SQL_Error:     <---------------- 当发生错误时可以查看一下这里
                          Replicate_Ignore_Server_Ids:
                                     Master_Server_Id: 100
                                          Master_UUID: 1ea51141-a6b4-11e9-b38f-000c29f6f083
                                     Master_Info_File: /var/lib/mysql/master.info
                                            SQL_Delay: 0
                                  SQL_Remaining_Delay: NULL
                              Slave_SQL_Running_State: Slave has read all relay log; waiting for more updates
                                   Master_Retry_Count: 86400
                                          Master_Bind:
                              Last_IO_Error_Timestamp:
                             Last_SQL_Error_Timestamp:
                                       Master_SSL_Crl:
                                   Master_SSL_Crlpath:
                                   Retrieved_Gtid_Set:
                                    Executed_Gtid_Set: 1ea51141-a6b4-11e9-b38f-000c29f6f083:1-2
                                        Auto_Position: 1    <--------------- 观察到 已经 启用了 auto_position 功能.
                                 Replicate_Rewrite_DB:
                                         Channel_Name:
                                   Master_TLS_Version:






---------------------------------------------------------------------------------------------------
测试 test:

// master 上 执行一些 修改语句, 如创建 jiaowu 数据库:
mysql> CREATE DATABASE jiaowu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

// slave 上 观察 一下 master 上的 changes 是否 被 replicated 过来了, 如 查看 当前 slave 上是否存在 jiaowu 数据库:
mysql> show databases;
        +--------------------+
        | Database           |
        +--------------------+
        | information_schema |
        | jiaowu             | <-----
        | mysql              |
        | performance_schema |
        | sys                |
        +--------------------+


---------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------

其他相关命令:

      mysql> stop slave;   # 暂停 slave threads


默认 启动 mysqld 时, 会 自动 start slave threads.  如果启动时指定了 --skip-slave-start , 则 slave 启动后 不会自动 start slave threads.


语句: flush tables with read lock     # 常用于 backup, 与语句 lock tables 是有区别的. 见  https://dev.mysql.com/doc/refman/5.7/en/flush.html
作用: Closes all open tables and locks all tables for all databases with a global read lock.

语句:  UNLOCK TABLES
作用:  release the lock


reset 命令 见  https://dev.mysql.com/doc/refman/5.7/en/reset.html

------------------
其他一些 可能感兴趣的 变量:
        gtid_next
        gtid_executed
        gtid_purged

        gtid_owned

        binlog_gtid_simple_recovery
        gtid_executed_compression_period

        sync_binlog=1
        innodb_flush_log_at_trx_commit=1

其他一些 可能感兴趣的 表:
        mysql.gtid_executed

   更多信息 见 mysql 官网 和 其他笔记 或 google, baidu
---------------------------------------------------------------------------------------------------
网上资料:

https://dev.mysql.com/doc/refman/5.7/en/replication.html

16.1.1 Binary Log File Position Based Replication Configuration Overview
      https://dev.mysql.com/doc/refman/5.7/en/binlog-replication-configuration-overview.html

16.1.3 Replication with Global Transaction Identifiers
      https://dev.mysql.com/doc/refman/5.7/en/replication-gtids.html



16.1.3.4 Setting Up Replication Using GTIDs
    https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-howto.html

16.1.3.6 Restrictions on Replication with GTIDs  (基于 GTIDs 的 复制的 限制)
    https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-restrictions.html


谨记一点:
      未启用 GTIDs 的 transactions 的 binary log 是 不能 用在 启用了  GTIDs 的 server 上的

      It is important to understand that logs containing transactions
      without GTIDs cannot be used on servers where GTIDs are enabled.
      Before proceeding, you must be sure that transactions without
      GTIDs do not exist anywhere in the topology.

注: 在 启用 GTIDs 之前做的 已经存在的 backups 不能 再 用于 启用了 GTIDs 的 server
    此时做 一个 新的 backup, 你将 不会没有 可用的 backup.

