
ip信息：
    master: 192.168.175.100/24
    slave:  192.168.175.101/24

---------------------------------------------------------------------------------------------------
master server 端:

// 前期准备：设置时区 和 同步时间,  参考  https://github.com/yangsg/linux_training_notes/tree/master/ntp_chrony_basic

// master设置时区和同步时间
[root@master ~]# timedatectl set-timezone Asia/Shanghai
[root@master ~]# timedatectl status | grep 'Time zone'
       Time zone: Asia/Shanghai (CST, +0800)

[root@master ~]# yum -y install chrony
[root@master ~]# vim /etc/chrony.conf   #// 生产环境应该是同步到自己内部搭建的ntp服务器

      #server 0.centos.pool.ntp.org iburst
      #server 1.centos.pool.ntp.org iburst
      #server 2.centos.pool.ntp.org iburst
      #server 3.centos.pool.ntp.org iburst

      server ntp1.aliyun.com iburst
      server ntp2.aliyun.com iburst
      server ntp3.aliyun.com iburst
      server ntp4.aliyun.com iburst
      server ntp5.aliyun.com iburst
      server ntp6.aliyun.com iburst
      server ntp7.aliyun.com iburst

[root@master ~]# systemctl start chronyd
[root@master ~]# systemctl enable chronyd

[root@master ~]# chronyc sources -v
[root@master ~]# timedatectl | grep 'NTP enabled'
     NTP enabled: yes




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
      mysql-connectors-community/x86_64  MySQL Connectors Community    enabled:     95
      mysql-connectors-community-source  MySQL Connectors Community -  disabled
      mysql-tools-community/x86_64       MySQL Tools Community         enabled:     84
      mysql-tools-community-source       MySQL Tools Community - Sourc disabled
      mysql-tools-preview/x86_64         MySQL Tools Preview           disabled
      mysql-tools-preview-source         MySQL Tools Preview - Source  disabled
      mysql55-community/x86_64           MySQL 5.5 Community Server    disabled
      mysql55-community-source           MySQL 5.5 Community Server -  disabled
      mysql56-community/x86_64           MySQL 5.6 Community Server    disabled
      mysql56-community-source           MySQL 5.6 Community Server -  disabled
      mysql57-community/x86_64           MySQL 5.7 Community Server    disabled
      mysql57-community-source           MySQL 5.7 Community Server -  disabled
      mysql80-community/x86_64           MySQL 8.0 Community Server    enabled:     82
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

[root@master download]# yum repolist enabled | grep mysql
      mysql-connectors-community/x86_64 MySQL Connectors Community                  95
      mysql-tools-community/x86_64      MySQL Tools Community                       84
      mysql57-community/x86_64          MySQL 5.7 Community Server                 327

[root@master download]# yum -y install mysql-community-server

[root@master download]# rpm -q mysql-community-server
      mysql-community-server-5.7.25-1.el7.x86_64

[root@master ~]# systemctl start mysqld.service
[root@master ~]# systemctl enable mysqld.service
[root@master ~]# systemctl status mysqld.service

[root@master ~]# grep 'temporary password' /var/log/mysqld.log
2019-04-04T13:05:09.097245Z 1 [Note] A temporary password is generated for root@localhost: h5GulK<>uN#s

[root@master ~]# mysql -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
mysql> quit

[root@master ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2268/mysqld

[root@master ~]# ps -elf | grep mysql
    1 S mysql      2268      1  0  80   0 - 279981 poll_s 21:05 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid

// 开始正式 配置 与 replication 中 与 master 相关的配置

// 启用 master 的 bin log 和 设置 server id. 参考 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-masterbaseconfig.html
[root@master ~]# vim /etc/my.cnf
          [mysqld]
          log-bin=master-bin
          server-id=100   # server-id 范围: 1 and (232)−1

// 重启 mysql server, 以 应用 如上的配置
[root@master ~]# systemctl restart mysqld


// 创建 专用于 replication 的 user. 参见 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
mysql> CREATE USER 'repluser'@'192.168.175.101' IDENTIFIED BY 'WWW.1.com';  # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.101';      # 授予 该用户 replication slave 全向

     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.

// 在 master 上 做一次 full backup, 后续的操作 会 将其 同步给 slave
[root@master ~]# mysqldump -u root -p --lock-all-tables --all-databases --master-data=2 > /root/db_full-backup.sql

// 查看 一下 后续 slave 用到的 replication 的 起始坐标
[root@master ~]# grep -in 'change master' /root/db_full-backup.sql  | head -n 1
      22:-- CHANGE MASTER TO MASTER_LOG_FILE='master-bin.000001', MASTER_LOG_POS=631;


// 将 master 的 db_full-backup.sql 拷贝给 slave
[root@master ~]# rsync -av /root/db_full-backup.sql  root@192.168.175.101:/tmp/











---------------------------------------------------------------------------------------------------
slave server 端:

// slave 上按照与master相同的方式设置时区和同步时间
[root@slave ~]# timedatectl set-timezone Asia/Shanghai
[root@slave ~]# timedatectl status | grep 'Time zone'
       Time zone: Asia/Shanghai (CST, +0800)

[root@slave ~]# yum -y install chrony
[root@slave ~]# vim /etc/chrony.conf   #// 生产环境应该是同步到自己内部搭建的ntp服务器

      #server 0.centos.pool.ntp.org iburst
      #server 1.centos.pool.ntp.org iburst
      #server 2.centos.pool.ntp.org iburst
      #server 3.centos.pool.ntp.org iburst

      server ntp1.aliyun.com iburst
      server ntp2.aliyun.com iburst
      server ntp3.aliyun.com iburst
      server ntp4.aliyun.com iburst
      server ntp5.aliyun.com iburst
      server ntp6.aliyun.com iburst
      server ntp7.aliyun.com iburst

[root@slave ~]# systemctl start chronyd
[root@slave ~]# systemctl enable chronyd

[root@slave ~]# chronyc sources -v
[root@slave ~]# timedatectl | grep 'NTP enabled'
     NTP enabled: yes


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
      mysql-connectors-community/x86_64  MySQL Connectors Community    enabled:     95
      mysql-connectors-community-source  MySQL Connectors Community -  disabled
      mysql-tools-community/x86_64       MySQL Tools Community         enabled:     84
      mysql-tools-community-source       MySQL Tools Community - Sourc disabled
      mysql-tools-preview/x86_64         MySQL Tools Preview           disabled
      mysql-tools-preview-source         MySQL Tools Preview - Source  disabled
      mysql55-community/x86_64           MySQL 5.5 Community Server    disabled
      mysql55-community-source           MySQL 5.5 Community Server -  disabled
      mysql56-community/x86_64           MySQL 5.6 Community Server    disabled
      mysql56-community-source           MySQL 5.6 Community Server -  disabled
      mysql57-community/x86_64           MySQL 5.7 Community Server    disabled
      mysql57-community-source           MySQL 5.7 Community Server -  disabled
      mysql80-community/x86_64           MySQL 8.0 Community Server    enabled:     82
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
      mysql-connectors-community/x86_64 MySQL Connectors Community                  95
      mysql-tools-community/x86_64      MySQL Tools Community                       84
      mysql57-community/x86_64          MySQL 5.7 Community Server                 327


[root@slave download]# yum -y install mysql-community-server
[root@slave download]# rpm -q mysql-community-server
      mysql-community-server-5.7.25-1.el7.x86_64

[root@slave ~]# systemctl start mysqld.service
[root@slave ~]# systemctl enable mysqld.service
[root@slave ~]# systemctl status mysqld.service

[root@slave ~]# grep 'temporary password' /var/log/mysqld.log
2019-04-04T13:57:52.760328Z 1 [Note] A temporary password is generated for root@localhost: v4kUOWnvig!1

mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
mysql> quit


[root@slave ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      17766/mysqld
[root@slave ~]# ps -elf | grep mysql
    1 S mysql     17766      1  0  80   0 - 279981 poll_s 21:57 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


// 开始正式 设置 slave 中 与 replication 相关的 设置. 参考 https://dev.mysql.com/doc/refman/5.7/en/replication-setup-slaves.html

[root@slave ~]# mysql -u root -p < /tmp/db_full-backup.sql  # 以 batch mode 还原 master 的 备份(即保持slave 初始数据与 master 一致)

[root@slave ~]# echo $?
0

// 配 slave 设置一个 server-id
[root@slave ~]# vim /etc/my.cnf

      [mysqld]
      log-bin=slave-bin  #启用 slave 的 bin log, 该行配置非必须, 但对于 data backups 和 crash recovery 等 处理很有用,很方便
      server-id=101


// 重启 slave 的 mysql server 是 如上配置生效
[root@slave ~]# systemctl restart mysqld

// 查看 slave 的 replication 需要的 起始坐标
[root@slave ~]# grep -in 'change master to' /tmp/db_full-backup.sql  | head -n 1
        22:-- CHANGE MASTER TO MASTER_LOG_FILE='master-bin.000001', MASTER_LOG_POS=631;



// 执行一下 help 帮助信息 查看 change master 的 语法帮助
mysql> help change master to

// 在 slave 上设置 master 信息 (即 到 master 的 连接, 认证 和 replication 的坐标信息)
mysql> CHANGE MASTER TO
    -> MASTER_HOST='192.168.175.100',
    -> MASTER_PORT=3306,
    -> MASTER_USER='repluser',
    -> MASTER_PASSWORD='WWW.1.com',
    -> MASTER_LOG_FILE='master-bin.000001',
    -> MASTER_LOG_POS=631;



// 查看 一些 先关的文件
[root@slave ~]# ls -1 /var/lib/mysql | grep -E 'master.info|slave|relay'
            master.info
            relay-log.info
            slave-bin.000001
            slave-bin.index
            slave-relay-bin.000001
            slave-relay-bin.index



// 查看 一下  master.info 文件 内容
[root@slave ~]# cat /var/lib/mysql/master.info
                              25
                              master-bin.000001
                              631
                              192.168.175.100
                              repluser
                              WWW.1.com
                              3306
                              60
                              0





                              0
                              30.000

                              0

                              86400


                              0


// 查看 一下  relay-log.info 文件 内容
[root@slave ~]# cat /var/lib/mysql/relay-log.info
                              7
                              ./slave-relay-bin.000001
                              4
                              master-bin.000001
                              631
                              0
                              0
                              1




// 其中 slave 线程(io thread 和 sql thead)
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
                              Relay_Log_Pos: 321
                      Relay_Master_Log_File: master-bin.000001
                           Slave_IO_Running: Yes   <----------- 查看 io thread 状态
                          Slave_SQL_Running: Yes   <----------- 查看 sql thread 状态
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
                            Relay_Log_Space: 528
                            Until_Condition: None
                             Until_Log_File:
                              Until_Log_Pos: 0
                         Master_SSL_Allowed: No
                         Master_SSL_CA_File:
                         Master_SSL_CA_Path:
                            Master_SSL_Cert:
                          Master_SSL_Cipher:
                             Master_SSL_Key:
                      Seconds_Behind_Master: 0   <------------- 延迟
              Master_SSL_Verify_Server_Cert: No
                              Last_IO_Errno: 0
                              Last_IO_Error:      <---------------- 当发生错误时可以查看一下这里
                             Last_SQL_Errno: 0
                             Last_SQL_Error:      <---------------- 当发生错误时可以查看一下这里 
                Replicate_Ignore_Server_Ids:
                           Master_Server_Id: 100
                                Master_UUID: dc0c664f-a20f-11e9-b9d0-000c2982ac0f
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
                          Executed_Gtid_Set:
                              Auto_Position: 0
                       Replicate_Rewrite_DB:
                               Channel_Name:
                         Master_TLS_Version:



---------------------------------------------------------------------------------------------------
测试 test:
   在 master 上 执行一些 修改操作 (如 创建数据库 等), 看起是否自动 同步到 slave 端.

---------------------------------------------------------------------------------------------------

其他相关命令:

      mysql> stop slave;   # 暂停 slave threads


默认 启动 mysqld 时, 会 自动 start slave threads.  如果启动时指定了 --skip-slave-start , 则 slave 启动后 不会自动 start slave threads.


语句: flush tables with read lock     # 常用于 backup, 与语句 lock tables 是有区别的. 见  https://dev.mysql.com/doc/refman/5.7/en/flush.html
作用: Closes all open tables and locks all tables for all databases with a global read lock.

语句:  UNLOCK TABLES
作用:  release the lock


reset 命令 见  https://dev.mysql.com/doc/refman/5.7/en/reset.html

---------------------------------------------------------------------------------------------------
网上资料:

    16.1 Configuring Replication
        https://dev.mysql.com/doc/refman/5.7/en/replication-configuration.html

    16.1.1 Binary Log File Position Based Replication Configuration Overview
        https://dev.mysql.com/doc/refman/5.7/en/binlog-replication-configuration-overview.html


