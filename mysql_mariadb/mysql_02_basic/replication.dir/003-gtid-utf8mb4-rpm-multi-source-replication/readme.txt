
多源复制, 可理解为 多主一从


---------------------------------------------------------------------------------------------------
准备 实现 环境用的 3 台 主机:
master01: 192.168.175.101
master02: 192.168.175.102
slave:    192.168.175.103

// 搭建 本地 yum repo 服务器
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
mysql> CREATE USER 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
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
mysql> CREATE USER 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
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



// 启动 slave 线程(io_thread , sql_thread),
// 见 https://dev.mysql.com/doc/mysql-replication-excerpt/5.7/en/replication-multi-source-start-slave.html
mysql> start slave;    # 该命令 会 启动 所有 channel 上 所有 类型的 的 thread





---------------------------------------------------------------------------------------------------

随便测试一下:

mysql> CREATE DATABASE db_m01 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



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
网上资料:

16.1.4.1 MySQL Multi-Source Replication Overview
      https://dev.mysql.com/doc/refman/5.7/en/replication-multi-source-overview.html

16.2.3 Replication Channels
      https://dev.mysql.com/doc/refman/5.7/en/replication-channels.html



