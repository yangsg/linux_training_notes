
management interface:

    controller
    192.168.175.11

    compute1
    192.168.175.31


----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-networking-controller.html

在 Controller node 上 设置 网卡信息 并 添加 主机名解析

[root@controller ~]# vim /etc/hosts

      192.168.175.11       controller
      192.168.175.31       compute1

      # 如果没有 部署如下 可选的 services, 则如下 3 条 entries 可以不要
      # This guide includes host entries for optional services in order to reduce complexity should you choose to deploy them.
      192.168.175.41       block1
      192.168.175.51       object1
      192.168.175.52       object2


----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-networking-compute.html

在 Compute node 上 设置 网卡信息 并 添加 主机名解析


[root@compute1 ~]# vim /etc/hosts

      192.168.175.11       controller
      192.168.175.31       compute1

      # 如果没有 部署如下 可选的 services, 则如下 3 条 entries 可以不要
      # This guide includes host entries for optional services in order to reduce complexity should you choose to deploy them.
      192.168.175.41       block1
      192.168.175.51       object1
      192.168.175.52       object2





----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-networking-verify.html

// 验证 网络 连接

[root@controller ~]# ping compute1 -c 1 &> /dev/null && echo success
success

[root@compute1 ~]# ping controller -c 1 &> /dev/null && echo success
success

----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-ntp.html

设置 时间 同步

    chrony 笔记: https://github.com/yangsg/linux_training_notes/tree/master/ntp_chrony_basic

------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-ntp-controller.html

// 在 Controller node 上 设置 时间同步

[root@controller ~]# yum -y install chrony

[root@controller ~]# vim /etc/chrony.conf

    #server 0.centos.pool.ntp.org iburst
    #server 1.centos.pool.ntp.org iburst
    #server 2.centos.pool.ntp.org iburst
    #server 3.centos.pool.ntp.org iburst

    # http://www.ntp.org.cn/pool.php
    # https://help.aliyun.com/document_detail/92704.html
    server ntp1.aliyun.com iburst
    server ntp2.aliyun.com iburst
    server ntp3.aliyun.com iburst
    server ntp4.aliyun.com iburst
    server ntp5.aliyun.com iburst
    server ntp6.aliyun.com iburst
    server ntp7.aliyun.com iburst

    allow 192.168.175.0/24

    local stratum 10


[root@controller ~]# systemctl start chronyd.service
[root@controller ~]# systemctl enable chronyd.service


------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-ntp-other.html

// 在 其他节点 上 设置 时间同步

此处 设置  compute1 找 controller 进行同步

[root@compute1 ~]# yum -y install chrony

[root@compute1 ~]# vim /etc/chrony.conf

      #server 0.centos.pool.ntp.org iburst
      #server 1.centos.pool.ntp.org iburst
      #server 2.centos.pool.ntp.org iburst
      #server 3.centos.pool.ntp.org iburst

      server controller iburst

[root@compute1 ~]# systemctl start chronyd.service
[root@compute1 ~]# systemctl enable chronyd.service


------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-ntp-verify.html

// 验证时间同步


[root@controller ~]# chronyc sources -v

    210 Number of sources = 2

      .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
     / .- Source state '*' = current synced, '+' = combined , '-' = not combined,
    | /   '?' = unreachable, 'x' = time may be in error, '~' = time too variable.
    ||                                                 .- xxxx [ yyyy ] +/- zzzz
    ||      Reachability register (octal) -.           |  xxxx = adjusted offset,
    ||      Log2(Polling interval) --.      |          |  yyyy = measured offset,
    ||                                \     |          |  zzzz = estimated error.
    ||                                 |    |           \
    MS Name/IP address         Stratum Poll Reach LastRx Last sample
    ===============================================================================
    ^+ 120.25.115.20                 2   6   377    28  -1019us[ -855us] +/-   23ms
    ^* 203.107.6.88                  2   6   377    26  +1646us[+1810us] +/-   21ms


[root@compute1 ~]# chronyc sources -v
    210 Number of sources = 1

      .-- Source mode  '^' = server, '=' = peer, '#' = local clock.
     / .- Source state '*' = current synced, '+' = combined , '-' = not combined,
    | /   '?' = unreachable, 'x' = time may be in error, '~' = time too variable.
    ||                                                 .- xxxx [ yyyy ] +/- zzzz
    ||      Reachability register (octal) -.           |  xxxx = adjusted offset,
    ||      Log2(Polling interval) --.      |          |  yyyy = measured offset,
    ||                                \     |          |  zzzz = estimated error.
    ||                                 |    |           \
    MS Name/IP address         Stratum Poll Reach LastRx Last sample
    ===============================================================================
    ^* controller                    3   6    17    25  +5905ns[ +100us] +/-   20ms


----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-packages.html
https://docs.openstack.org/install-guide/environment-packages-rdo.html


安装 OpenStack packages

此处描述的 openstack packages 需要在 所有 nodes 上安装

    The set up of OpenStack packages described here needs to be done on all nodes: controller, compute, and Block Storage nodes.


// 在 controller node 上安装
[root@controller ~]# yum -y install centos-release-openstack-stein
[root@controller ~]# yum -y install python-openstackclient


// 在 compute1 node 上安装
[root@compute1 ~]# yum -y install centos-release-openstack-stein
[root@compute1 ~]# yum -y install python-openstackclient



----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-sql-database.html
https://docs.openstack.org/install-guide/environment-sql-database-rdo.html


在 controller node 上安装 MariaDB 数据库

[root@controller ~]# yum -y install mariadb mariadb-server python2-PyMySQL

[root@controller ~]# vim /etc/my.cnf.d/openstack.cnf

      [mysqld]
      bind-address = 192.168.175.11

      default-storage-engine = innodb
      innodb_file_per_table = on
      max_connections = 4096
      collation-server = utf8_general_ci
      character-set-server = utf8



// 注: 如果现在直接启动, 会出现 'max_open_files to more than 1024' 的 Warning 信息,
//     解决方法见后面
[root@controller ~]# systemctl start mariadb.service
[root@controller ~]# systemctl enable mariadb.service
    Created symlink from /etc/systemd/system/mysql.service to /usr/lib/systemd/system/mariadb.service.
    Created symlink from /etc/systemd/system/mysqld.service to /usr/lib/systemd/system/mariadb.service.
    Created symlink from /etc/systemd/system/multi-user.target.wants/mariadb.service to /usr/lib/systemd/system/mariadb.service.



[root@controller ~]# systemctl status mariadb.service
      ● mariadb.service - MariaDB 10.3 database server
         Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
         Active: active (running) since Sun 2019-09-29 19:57:46 CST; 5min ago
           Docs: man:mysqld(8)
                 https://mariadb.com/kb/en/library/systemd/
       Main PID: 23058 (mysqld)
         Status: "Taking your SQL requests now..."
         CGroup: /system.slice/mariadb.service
                 └─23058 /usr/libexec/mysqld --basedir=/usr

      Sep 29 19:57:46 controller mysql-prepare-db-dir[22955]: Please report any problems at http://mariadb.org/jira
      Sep 29 19:57:46 controller mysql-prepare-db-dir[22955]: The latest information about MariaDB is available at http://mariadb.org/.
      Sep 29 19:57:46 controller mysql-prepare-db-dir[22955]: You can find additional information about the MySQL part at:
      Sep 29 19:57:46 controller mysql-prepare-db-dir[22955]: http://dev.mysql.com
      Sep 29 19:57:46 controller mysql-prepare-db-dir[22955]: Consider joining MariaDB's strong and vibrant community:
      Sep 29 19:57:46 controller mysql-prepare-db-dir[22955]: https://mariadb.org/get-involved/
      Sep 29 19:57:46 controller mysqld[23058]: 2019-09-29 19:57:46 0 [Note] /usr/libexec/mysqld (mysqld 10.3.10-MariaDB) starting as process 23058 ...
      Sep 29 19:57:46 controller mysqld[23058]: 2019-09-29 19:57:46 0 [Warning] Could not increase number of max_open_files to more than 1024 (request: 8127) <----观察
      Sep 29 19:57:46 controller mysqld[23058]: 2019-09-29 19:57:46 0 [Warning] Changed limits: max_open_files: 1024  max_connections: 594 (was 4096)  table_cache: 200 (was 2000)
      Sep 29 19:57:46 controller systemd[1]: Started MariaDB 10.3 database server.


问题 issue: 观察上面的 警告信息:
      [Warning] Could not increase number of max_open_files to more than 1024 (request: 8127)
      [Warning] Changed limits: max_open_files: 1024  max_connections: 594 (was 4096)  table_cache: 200 (was 2000)


现在开始来解决该问题
    参考:
        https://mariadb.com/kb/en/library/server-system-variables/#open_files_limit
        https://mariadb.com/kb/en/library/systemd/#configuring-the-open-files-limit
        https://github.com/yangsg/linux_training_notes/blob/master/linux_basic/centos7.4/02-other/015-systemd-unit-files.txt

[root@controller ~]# mkdir -p /etc/systemd/system/mariadb.service.d
[root@controller ~]# vim /etc/systemd/system/mariadb.service.d/limitnofile.conf

      [Service]
      LimitNOFILE=infinity


[root@controller ~]# systemctl daemon-reload
[root@controller ~]# systemctl restart mariadb.service

[root@controller ~]# systemctl daemon-reload
[root@controller ~]# systemctl restart mariadb.service
[root@controller ~]# systemctl status mariadb.service
        ● mariadb.service - MariaDB 10.3 database server
           Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
          Drop-In: /etc/systemd/system/mariadb.service.d
                   └─limitnofile.conf  <-----观察
           Active: active (running) since Sun 2019-09-29 20:24:33 CST; 23s ago
             Docs: man:mysqld(8)
                   https://mariadb.com/kb/en/library/systemd/
          Process: 23318 ExecStartPost=/usr/libexec/mysql-check-upgrade (code=exited, status=0/SUCCESS)
          Process: 23246 ExecStartPre=/usr/libexec/mysql-prepare-db-dir %n (code=exited, status=0/SUCCESS)
          Process: 23222 ExecStartPre=/usr/libexec/mysql-check-socket (code=exited, status=0/SUCCESS)
         Main PID: 23285 (mysqld)
           Status: "Taking your SQL requests now..."
           CGroup: /system.slice/mariadb.service
                   └─23285 /usr/libexec/mysqld --basedir=/usr

        Sep 29 20:24:33 controller systemd[1]: Starting MariaDB 10.3 database server...
        Sep 29 20:24:33 controller mysql-prepare-db-dir[23246]: Database MariaDB is probably initialized in /var/lib/mysql already, nothing is done.
        Sep 29 20:24:33 controller mysqld[23285]: 2019-09-29 20:24:33 0 [Note] /usr/libexec/mysqld (mysqld 10.3.10-MariaDB) starting as process 23285 ...
        Sep 29 20:24:33 controller systemd[1]: Started MariaDB 10.3 database server.

[root@controller ~]# netstat -anptu | grep mysql
      tcp        0      0 192.168.175.11:3306     0.0.0.0:*               LISTEN      23285/mysqld

[root@controller ~]# ps aux |grep mysqld
      mysql     23285  0.1  2.4 1311948 98100 ?       Ssl  20:24   0:00 /usr/libexec/mysqld --basedir=/usr



[root@controller ~]# mysql_secure_installation

    Set root password? [Y/n] y
    New password:   <======设置密码, 本示例使用的密码为 'redhat'
    Re-enter new password:  <=====重新键入设置的密码
    Password updated successfully!


[root@controller ~]# mysql -u root -p
    Enter password:  <=====输入密码
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 20
    Server version: 10.3.10-MariaDB MariaDB Server

    Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> show databases;  <=====显示所有 databases
    +--------------------+
    | Database           |
    +--------------------+
    | information_schema |
    | mysql              |
    | performance_schema |
    +--------------------+
    3 rows in set (0.000 sec)

    MariaDB [(none)]> quit  <======退出
    Bye




----------------------------------------------------------------------------------------------------

















