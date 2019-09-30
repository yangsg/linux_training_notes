
management interface:

    controller
    192.168.175.11

    compute1
    192.168.175.31


// 在 compute1 所在 虚拟机上 启用 vmware 的 virtual matchine 中的 cpu 的 虚拟化支持功能:
// 右键 该 centos7.4 对应的虚拟主机 -> [设置...] -> [处理器] -> 勾选上[虚拟化 Intel VT-x/EPT 或 AMD-V/RVI(V)]



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
https://docs.openstack.org/install-guide/environment-messaging.html
https://docs.openstack.org/install-guide/environment-messaging-rdo.html


Message queue

在 controller node 上安装 RabbitMQ 消息队列 service

[root@controller ~]# yum -y install rabbitmq-server

[root@controller ~]# systemctl start rabbitmq-server.service
[root@controller ~]# systemctl enable rabbitmq-server.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/rabbitmq-server.service to /usr/lib/systemd/system/rabbitmq-server.service.

[root@controller ~]# systemctl status rabbitmq-server.service
    ● rabbitmq-server.service - RabbitMQ broker
       Loaded: loaded (/usr/lib/systemd/system/rabbitmq-server.service; enabled; vendor preset: disabled)
       Active: active (running) since Sun 2019-09-29 22:01:09 CST; 10min ago
     Main PID: 23612 (beam)
       Status: "Initialized"
       CGroup: /system.slice/rabbitmq-server.service
               ├─23612 /usr/lib64/erlang/erts-8.3.5.3/bin/beam -W w -A 64 -P 1048576 -t 5000000 -stbt db -zdbbl 128000 -K true -- -root /usr/lib64/erlang -progname erl -- -home /var/lib/rab...
               ├─23793 erl_child_setup 1024
               ├─23802 inet_gethost 4
               └─23803 inet_gethost 4

    Sep 29 22:01:07 controller systemd[1]: Starting RabbitMQ broker...
    Sep 29 22:01:07 controller rabbitmq-server[23612]: RabbitMQ 3.6.16. Copyright (C) 2007-2018 Pivotal Software, Inc.
    Sep 29 22:01:07 controller rabbitmq-server[23612]: ##  ##      Licensed under the MPL.  See http://www.rabbitmq.com/
    Sep 29 22:01:07 controller rabbitmq-server[23612]: ##  ##
    Sep 29 22:01:07 controller rabbitmq-server[23612]: ##########  Logs: /var/log/rabbitmq/rabbit@controller.log
    Sep 29 22:01:07 controller rabbitmq-server[23612]: ######  ##        /var/log/rabbitmq/rabbit@controller-sasl.log
    Sep 29 22:01:07 controller rabbitmq-server[23612]: ##########
    Sep 29 22:01:07 controller rabbitmq-server[23612]: Starting broker...
    Sep 29 22:01:09 controller systemd[1]: Started RabbitMQ broker.
    Sep 29 22:01:09 controller rabbitmq-server[23612]: completed with 0 plugins.



// 语法: rabbitmqctl add_user {username} {password}
[root@controller ~]# rabbitmqctl add_user openstack redhat
    Creating user "openstack"

// Permit configuration, write, and read access for the openstack user:
// 语法: rabbitmqctl set_permissions [-p vhost] {user} {conf} {write} {read}
[root@controller ~]# rabbitmqctl set_permissions openstack ".*" ".*" ".*"
    Setting permissions for user "openstack" in vhost "/"



----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-memcached.html
https://docs.openstack.org/install-guide/environment-memcached-rdo.html

        Identity service 认证机制 使用 Memcached  来缓存 tokens

在 controller node 上安装 Memcached


[root@controller ~]# yum -y install memcached python-memcached

// 使 memcached 可以监听在 controller node 的 management IP, 这样可以使 其他 nodes 可以通过 management network 对其访问
[root@controller ~]# vim  /etc/sysconfig/memcached

      #OPTIONS="-l 127.0.0.1,::1"
      OPTIONS="-l 127.0.0.1,::1,controller"


[root@controller ~]# systemctl start memcached.service
[root@controller ~]# systemctl enable memcached.service
      Created symlink from /etc/systemd/system/multi-user.target.wants/memcached.service to /usr/lib/systemd/system/memcached.service.

[root@controller ~]# systemctl status memcached.service
      ● memcached.service - memcached daemon
         Loaded: loaded (/usr/lib/systemd/system/memcached.service; enabled; vendor preset: disabled)
         Active: active (running) since Sun 2019-09-29 22:49:13 CST; 19s ago
       Main PID: 26654 (memcached)
         CGroup: /system.slice/memcached.service
                 └─26654 /usr/bin/memcached -p 11211 -u memcached -m 64 -c 1024 -l 127.0.0.1,::1,controller  <----观察

      Sep 29 22:49:13 controller systemd[1]: Started memcached daemon.
      Sep 29 22:49:13 controller systemd[1]: Starting memcached daemon...

[root@controller ~]# netstat -anput | grep memcached
    tcp        0      0 192.168.175.11:11211    0.0.0.0:*               LISTEN      26654/memcached  <----观察
    tcp        0      0 127.0.0.1:11211         0.0.0.0:*               LISTEN      26654/memcached
    tcp6       0      0 ::1:11211               :::*                    LISTEN      26654/memcached



----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/environment-etcd.html
https://docs.openstack.org/install-guide/environment-etcd-rdo.html
https://blog.csdn.net/bbwangj/article/details/82584988
https://etcd.io/

OpenStack services may use Etcd, a distributed reliable key-value store for distributed key locking,
storing configuration, keeping track of service live-ness and other scenarios.


在 controller node 上安装 etcd

[root@controller ~]# yum -y install etcd


[root@controller ~]# vim /etc/etcd/etcd.conf

      #[Member]
      ETCD_DATA_DIR="/var/lib/etcd/default.etcd"
      ETCD_LISTEN_PEER_URLS="http://192.168.175.11:2380"
      ETCD_LISTEN_CLIENT_URLS="http://192.168.175.11:2379"
      ETCD_NAME="controller"
      #[Clustering]
      ETCD_INITIAL_ADVERTISE_PEER_URLS="http://192.168.175.11:2380"
      ETCD_ADVERTISE_CLIENT_URLS="http://192.168.175.11:2379"
      ETCD_INITIAL_CLUSTER="controller=http://192.168.175.11:2380"
      ETCD_INITIAL_CLUSTER_TOKEN="etcd-cluster-01"
      ETCD_INITIAL_CLUSTER_STATE="new"


[root@controller ~]# systemctl start etcd
[root@controller ~]# systemctl enable etcd
      Created symlink from /etc/systemd/system/multi-user.target.wants/etcd.service to /usr/lib/systemd/system/etcd.service.


[root@controller ~]# systemctl status etcd
      ● etcd.service - Etcd Server
         Loaded: loaded (/usr/lib/systemd/system/etcd.service; enabled; vendor preset: disabled)
         Active: active (running) since Mon 2019-09-30 08:46:12 CST; 16s ago
       Main PID: 2015 (etcd)
         CGroup: /system.slice/etcd.service
                 └─2015 /usr/bin/etcd --name=controller --data-dir=/var/lib/etcd/default.etcd --listen-client-urls=http://192.168.175.11:2379

      Sep 30 08:46:12 controller etcd[2015]: 191e268f337653e received MsgVoteResp from 191e268f337653e at term 2
      Sep 30 08:46:12 controller etcd[2015]: 191e268f337653e became leader at term 2
      Sep 30 08:46:12 controller etcd[2015]: raft.node: 191e268f337653e elected leader 191e268f337653e at term 2
      Sep 30 08:46:12 controller etcd[2015]: published {Name:controller ClientURLs:[http://192.168.175.11:2379]} to cluster 5395905c3ad60333
      Sep 30 08:46:12 controller etcd[2015]: setting up the initial cluster version to 3.3
      Sep 30 08:46:12 controller systemd[1]: Started Etcd Server.
      Sep 30 08:46:12 controller etcd[2015]: set the initial cluster version to 3.3
      Sep 30 08:46:12 controller etcd[2015]: enabled capabilities for version 3.3
      Sep 30 08:46:12 controller etcd[2015]: ready to serve client requests
      Sep 30 08:46:12 controller etcd[2015]: serving insecure client requests on 192.168.175.11:2379, this is strongly discouraged!





----------------------------------------------------------------------------------------------------
https://docs.openstack.org/install-guide/openstack-services.html
https://docs.openstack.org/install-guide/openstack-services.html#minimal-deployment-for-stein

Minimal deployment for Stein

Identity service – keystone installation for Stein

--------------------------------------------------------------------------------
https://docs.openstack.org/keystone/stein/install/
https://docs.openstack.org/keystone/stein/install/index-rdo.html


Identity service 概述
Identity service overview:
      https://docs.openstack.org/keystone/stein/install/get-started-rdo.html

        The OpenStack Identity service provides a single point of integration
        for managing authentication, authorization, and a catalog of services.
        // OpenStack Identity service 为管理身份验证，授权和服务目录提供了单点集成。

        Users and services can locate other services by using the service catalog, which is managed by the Identity service.
        // Users 和 services 通过  Identity service 管理的 the service catalog(服务目录) 来 定位查找 other services.

        Each service can have one or many endpoints and each endpoint can be one of three types: admin, internal, or public.
        // 每个 service  可以拥有 one or many endpoints 且 each endpoint 可以是 3 中类型之一: admin, internal, or public

        In a production environment, different endpoint types might reside on
        separate networks exposed to different types of users for security reasons.
        // 在生产环境中, 因为安全的原因 不同的 endpoint types 可能被 安置在 针对不同类型 users 的 独立网络中(separate networks)

              如:
                public API network   -----> Internet 上的 客户, 消费者
                admin API network    -----> 内部组织 用于管理 cloud infrastructure
                internal API network -----> 服务 nodes(hosts) 之间的通信交互

        OpenStack supports multiple regions for scalability. For simplicity,
        this guide uses the management network for all endpoint types and the default RegionOne region.

        Each OpenStack service in your deployment needs a service entry with corresponding endpoints
        stored in the Identity service. This can all be done after the Identity service has been installed and configured.



The Identity service contains these components(Identity service 包含的组件):

      - Server
          A centralized server provides authentication and authorization services using a RESTful interface.

      - Drivers
          Drivers or a service back end are integrated to the centralized server.
          They are used for accessing identity information in repositories external to OpenStack,
          and may already exist in the infrastructure where OpenStack is deployed (for example, SQL databases or LDAP servers).

      - Modules
          Middleware modules run in the address space of the OpenStack component that is using the Identity service.
          These modules intercept service requests, extract user credentials, and send them to the centralized server
          for authorization. The integration between the middleware modules and
          OpenStack components uses the Python Web Server Gateway Interface.




--------------------------------------------------------------------------------
https://docs.openstack.org/keystone/stein/install/keystone-install-rdo.html

在 controller node 上 安装 配置 Identity service(代号 keystone)

    This section describes how to install and configure the OpenStack Identity service, code-named keystone,
    on the controller node. For scalability purposes, this configuration deploys
    Fernet tokens and the Apache HTTP server to handle requests.


      关于 fernet 的一些资料:
          https://cryptography.io/en/latest/fernet/
          https://docs.openstack.org/keystone/pike/admin/identity-fernet-token-faq.html
          https://www.cnblogs.com/dhplxf/p/7966890.html
          https://www.redhat.com/en/blog/introduction-fernet-tokens-red-hat-openstack-platform


// 创建 数据库 keystone 并 授权
[root@controller ~]# mysql -u root -p
  Enter password:

  MariaDB [(none)]> CREATE DATABASE keystone;
  Query OK, 1 row affected (0.000 sec)

  MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'localhost' IDENTIFIED BY 'redhat';
  Query OK, 0 rows affected (0.001 sec)

  MariaDB [(none)]> GRANT ALL PRIVILEGES ON keystone.* TO 'keystone'@'%' IDENTIFIED BY 'redhat';
  Query OK, 0 rows affected (0.000 sec)

  MariaDB [(none)]> show databases;
  +--------------------+
  | Database           |
  +--------------------+
  | information_schema |
  | keystone           | <-----
  | mysql              |
  | performance_schema |
  +--------------------+
  4 rows in set (0.000 sec)


  MariaDB [(none)]> quit
  Bye


安装配置 keystone 相关组件

[root@controller ~]# yum -y install openstack-keystone httpd mod_wsgi

[root@controller ~]# vim /etc/keystone/keystone.conf

    [database]
    connection = mysql+pymysql://keystone:redhat@controller/keystone

    [token]
    provider = fernet


[root@controller ~]# su -s /bin/sh -c "keystone-manage db_sync" keystone

// 查看数据库 keystone 中的 tables
[root@controller ~]# mysql -u root -predhat -e 'show tables from keystone' -t | less

// Initialize Fernet key repositories:
[root@controller ~]# keystone-manage fernet_setup --keystone-user keystone --keystone-group keystone
[root@controller ~]# keystone-manage credential_setup --keystone-user keystone --keystone-group keystone


// Bootstrap the Identity service:
[root@controller ~]# keystone-manage bootstrap --bootstrap-password redhat \
                            --bootstrap-admin-url http://controller:5000/v3/ \
                            --bootstrap-internal-url http://controller:5000/v3/ \
                            --bootstrap-public-url http://controller:5000/v3/ \
                            --bootstrap-region-id RegionOne


[root@controller ~]# vim /etc/httpd/conf/httpd.conf

      ServerName controller


[root@controller ~]# ln -s /usr/share/keystone/wsgi-keystone.conf /etc/httpd/conf.d/

[root@controller ~]# systemctl start httpd.service
[root@controller ~]# systemctl enable httpd.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.

[root@controller ~]# systemctl status httpd.service
      ● httpd.service - The Apache HTTP Server
         Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
         Active: active (running) since Mon 2019-09-30 11:27:05 CST; 43s ago
           Docs: man:httpd(8)
                 man:apachectl(8)
       Main PID: 8330 (httpd)
         Status: "Total requests: 0; Current requests/sec: 0; Current traffic:   0 B/sec"
         CGroup: /system.slice/httpd.service
                 ├─8330 /usr/sbin/httpd -DFOREGROUND
                 ├─8331 (wsgi:keystone- -DFOREGROUND
                 ├─8332 (wsgi:keystone- -DFOREGROUND
                 ├─8333 (wsgi:keystone- -DFOREGROUND
                 ├─8343 (wsgi:keystone- -DFOREGROUND
                 ├─8346 (wsgi:keystone- -DFOREGROUND
                 ├─8350 /usr/sbin/httpd -DFOREGROUND
                 ├─8352 /usr/sbin/httpd -DFOREGROUND
                 ├─8353 /usr/sbin/httpd -DFOREGROUND
                 ├─8354 /usr/sbin/httpd -DFOREGROUND
                 └─8355 /usr/sbin/httpd -DFOREGROUND

      Sep 30 11:27:05 controller systemd[1]: Starting The Apache HTTP Server...
      Sep 30 11:27:05 controller systemd[1]: Started The Apache HTTP Server.



[root@controller ~]# export OS_USERNAME=admin
[root@controller ~]# export OS_PASSWORD=redhat
[root@controller ~]# export OS_PROJECT_NAME=admin
[root@controller ~]# export OS_USER_DOMAIN_NAME=Default
[root@controller ~]# export OS_PROJECT_DOMAIN_NAME=Default
[root@controller ~]# export OS_AUTH_URL=http://controller:5000/v3
[root@controller ~]# export OS_IDENTITY_API_VERSION=3




--------------------------------------------------------------------------------
https://docs.openstack.org/keystone/stein/install/keystone-users-rdo.html


    Create a domain, projects, users, and roles

    The Identity service provides authentication services for each OpenStack service.
    The authentication service uses a combination of domains, projects, users, and roles.

[root@controller ~]# openstack domain create --description "An Example Domain" example
      +-------------+----------------------------------+
      | Field       | Value                            |
      +-------------+----------------------------------+
      | description | An Example Domain                |
      | enabled     | True                             |
      | id          | 0bf31430c395426abe673516af4085dd |
      | name        | example                          |
      | tags        | []                               |
      +-------------+----------------------------------+

[root@controller ~]# openstack project create --domain default --description "Service Project" service
      +-------------+----------------------------------+
      | Field       | Value                            |
      +-------------+----------------------------------+
      | description | Service Project                  |
      | domain_id   | default                          |
      | enabled     | True                             |
      | id          | b5e6588417934a63ac4571154c0cba17 |
      | is_domain   | False                            |
      | name        | service                          |
      | parent_id   | default                          |
      | tags        | []                               |
      +-------------+----------------------------------+


[root@controller ~]# openstack project create --domain default --description "Demo Project" myproject
      +-------------+----------------------------------+
      | Field       | Value                            |
      +-------------+----------------------------------+
      | description | Demo Project                     |
      | domain_id   | default                          |
      | enabled     | True                             |
      | id          | d7f87854502c4d888c859a7a419c8c99 |
      | is_domain   | False                            |
      | name        | myproject                        |
      | parent_id   | default                          |
      | tags        | []                               |
      +-------------+----------------------------------+


[root@controller ~]# openstack user create --domain default --password-prompt myuser
      User Password:
      Repeat User Password:
      +---------------------+----------------------------------+
      | Field               | Value                            |
      +---------------------+----------------------------------+
      | domain_id           | default                          |
      | enabled             | True                             |
      | id                  | f72508de72fa43d2a77248b572378a8e |
      | name                | myuser                           |
      | options             | {}                               |
      | password_expires_at | None                             |
      +---------------------+----------------------------------+


[root@controller ~]# openstack role create myrole
      +-------------+----------------------------------+
      | Field       | Value                            |
      +-------------+----------------------------------+
      | description | None                             |
      | domain_id   | None                             |
      | id          | 0878d04a971a48688d59e4eca3482dbd |
      | name        | myrole                           |
      +-------------+----------------------------------+


// Add the myrole role to the myproject project and myuser user:
[root@controller ~]# openstack role add --project myproject --user myuser myrole



----------------------------------------------------------------------------------------------------
https://docs.openstack.org/keystone/stein/install/keystone-verify-rdo.html

Verify operation

[root@controller ~]# unset OS_AUTH_URL OS_PASSWORD


// As the admin user, request an authentication token:
[root@controller ~]# openstack --os-auth-url http://controller:5000/v3 \
                              --os-project-domain-name Default --os-user-domain-name Default \
                              --os-project-name admin --os-username admin token issue

    Password: <===输入密码: redhat
    +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Field      | Value                                                                                                                                                                                   |
    +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | expires    | 2019-09-30T05:01:55+0000                                                                                                                                                                |
    | id         | gAAAAABdkX4z02Mp0DeD0Go6ir4X6ChBW9a18FxzrFaCDSfAKJR646i1QUK4GV5gnWShIMUi11PHSsFxstX8ah12pZ1TcJNe8BBIlbzHYICEL-44-sJChZMprp1Tfrg8HIEN6Uo3qupAUyXJv22GQw8vt7oELGOs308nUbw78vo-7jt8XpmRmL8 |
    | project_id | c60fbd97d1da495cbaf6dce16ef22a73                                                                                                                                                        |
    | user_id    | 3b01e6ac80c444c2bb921b36a14353dd                                                                                                                                                        |
    +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+



// As the myuser user created in the previous section, request an authentication token:
[root@controller ~]# openstack --os-auth-url http://controller:5000/v3 \
                              --os-project-domain-name Default --os-user-domain-name Default \
                              --os-project-name myproject --os-username myuser token issue

    Password:
    +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Field      | Value                                                                                                                                                                                   |
    +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | expires    | 2019-09-30T05:05:07+0000                                                                                                                                                                |
    | id         | gAAAAABdkX7zlf5F56ODN2N_SZHXQWGHcROWfRJSNok0Q-vSKsYQcJ55K352QI_MFcTEsMLXRp9DdVqff2KbfnPmeHcvhYLI7FaNUNdzcIBBzrAcurKI_Yc2Wv6q7JBSaYPzOE7C9wi9D5hyAqQaMBxBIwu9cKVBojAqt9ctjlur9JXHjWlqRV4 |
    | project_id | d7f87854502c4d888c859a7a419c8c99                                                                                                                                                        |
    | user_id    | f72508de72fa43d2a77248b572378a8e                                                                                                                                                        |
    +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+








----------------------------------------------------------------------------------------------------
https://docs.openstack.org/keystone/stein/install/keystone-openrc-rdo.html

Create OpenStack client environment scripts

  客户端环境脚本: OpenRC 文件

[root@controller ~]# vim admin-openrc

      export OS_PROJECT_DOMAIN_NAME=Default
      export OS_USER_DOMAIN_NAME=Default
      export OS_PROJECT_NAME=admin
      export OS_USERNAME=admin
      export OS_PASSWORD=redhat
      export OS_AUTH_URL=http://controller:5000/v3
      export OS_IDENTITY_API_VERSION=3
      export OS_IMAGE_API_VERSION=2




[root@controller ~]# vim demo-openrc

      export OS_PROJECT_DOMAIN_NAME=Default
      export OS_USER_DOMAIN_NAME=Default
      export OS_PROJECT_NAME=myproject
      export OS_USERNAME=myuser
      export OS_PASSWORD=redhat
      export OS_AUTH_URL=http://controller:5000/v3
      export OS_IDENTITY_API_VERSION=3
      export OS_IMAGE_API_VERSION=2



[root@controller ~]# source admin-openrc
[root@controller ~]# openstack token issue
        +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | Field      | Value                                                                                                                                                                                   |
        +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
        | expires    | 2019-09-30T07:33:50+0000                                                                                                                                                                |
        | id         | gAAAAABdkaHOwLDkR-Tm5Ne73tHHKr-p3Siwc_xK11Ke1EpwN7Mihny8xOIljuHLVlVGZfb3N8DIjXTezqkftcrn7qTTTvlKWaWS5_w-2gLqOojqucIqRGE7dBCCWwq5CAo7iC9xV6OtIyx4ZelZzaBl4AH7yewy4Aav8joX_OGPsmzp2GqCqPk |
        | project_id | c60fbd97d1da495cbaf6dce16ef22a73                                                                                                                                                        |
        | user_id    | 3b01e6ac80c444c2bb921b36a14353dd                                                                                                                                                        |
        +------------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+





----------------------------------------------------------------------------------------------------
https://docs.openstack.org/glance/stein/install/

Glance Installation


--------------------------------------------------------------------------------
https://docs.openstack.org/glance/stein/install/get-started.html

        https://docs.openstack.org/glance/stein/configuration/index.html


Image service overview (Image service 概览)

    The Image service (glance) enables users to discover, register, and retrieve virtual machine images.
    It offers a REST API that enables you to query virtual machine image metadata and retrieve an actual image.
    You can store virtual machine images made available through the Image service in a variety of locations,
    from simple file systems to object-storage systems like OpenStack Object Storage.



The OpenStack Image service includes the following components(OpenStack Image service 包含的组件):

    - glance-api
        Accepts Image API calls for image discovery, retrieval, and storage.

    - glance-registry
        Stores, processes, and retrieves metadata about images. Metadata includes items such as size and type.

           Warning:
              The registry is a private internal service meant for use by OpenStack Image service. Do not expose this service to users.

    - Database
        Stores image metadata and you can choose your database depending on your preference. Most deployments use MySQL or SQLite.

    - Storage repository for image files
        Various repository types are supported including normal file systems (or
        any filesystem mounted on the glance-api controller node), Object Storage,
        RADOS block devices, VMware datastore, and HTTP. Note that
        some repositories will only support read-only usage.

    - Metadata definition service
        A common API for vendors, admins, services, and users to meaningfully define their own custom metadata.
        This metadata can be used on different types of resources like images, artifacts, volumes,
        flavors, and aggregates. A definition includes the new property’s key, description,
        constraints, and the resource types which it can be associated with.


--------------------------------------------------------------------------------
https://docs.openstack.org/glance/stein/install/install-rdo.html

在 controller node 上 安装配置 Image service (代号: glance)


[root@controller ~]# mysql -u root -p
    Enter password:

    MariaDB [(none)]> CREATE DATABASE glance;
    Query OK, 1 row affected (0.000 sec)

    MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'localhost' IDENTIFIED BY 'redhat';
    Query OK, 0 rows affected (0.000 sec)

    MariaDB [(none)]> GRANT ALL PRIVILEGES ON glance.* TO 'glance'@'%' IDENTIFIED BY 'redhat';
    Query OK, 0 rows affected (0.001 sec)

    MariaDB [(none)]> show databases;
    +--------------------+
    | Database           |
    +--------------------+
    | glance             | <------
    | information_schema |
    | keystone           |
    | mysql              |
    | performance_schema |
    +--------------------+
    5 rows in set (0.000 sec)

    MariaDB [(none)]> quit
    Bye


[root@controller ~]# source admin-openrc

// Create the glance user:
[root@controller ~]# openstack user create --domain default --password-prompt glance
    User Password:
    Repeat User Password:
    +---------------------+----------------------------------+
    | Field               | Value                            |
    +---------------------+----------------------------------+
    | domain_id           | default                          |
    | enabled             | True                             |
    | id                  | 4a94bfba2c9e4d7c970572053171faa7 |
    | name                | glance                           |
    | options             | {}                               |
    | password_expires_at | None                             |
    +---------------------+----------------------------------+



// Add the admin role to the glance user and service project:
[root@controller ~]# openstack role add --project service --user glance admin


// Create the glance service entity:
[root@controller ~]# openstack service create --name glance --description "OpenStack Image" image
      +-------------+----------------------------------+
      | Field       | Value                            |
      +-------------+----------------------------------+
      | description | OpenStack Image                  |
      | enabled     | True                             |
      | id          | 0fd89a1387e6429e9dffc700d0735642 |
      | name        | glance                           |
      | type        | image                            |
      +-------------+----------------------------------+



[root@controller ~]# openstack endpoint create --region RegionOne image public http://controller:9292
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | 9f040b59ae0c48b89cf011d36e6e83f2 |
      | interface    | public                           |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 0fd89a1387e6429e9dffc700d0735642 |
      | service_name | glance                           |
      | service_type | image                            |
      | url          | http://controller:9292           |
      +--------------+----------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne image internal http://controller:9292
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | 4607a208239e45799bb59d7a9e9a8bd3 |
      | interface    | internal                         |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 0fd89a1387e6429e9dffc700d0735642 |
      | service_name | glance                           |
      | service_type | image                            |
      | url          | http://controller:9292           |
      +--------------+----------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne image admin http://controller:9292
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | f72c740534a14a3d837173fadb835f21 |
      | interface    | admin                            |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 0fd89a1387e6429e9dffc700d0735642 |
      | service_name | glance                           |
      | service_type | image                            |
      | url          | http://controller:9292           |
      +--------------+----------------------------------+


Install and configure components(安装 和 配置 组件)
[root@controller ~]# yum -y install openstack-glance

[root@controller ~]# vim /etc/glance/glance-api.conf

      [database]
      connection = mysql+pymysql://glance:redhat@controller/glance

      [keystone_authtoken]
      www_authenticate_uri  = http://controller:5000
      auth_url = http://controller:5000
      memcached_servers = controller:11211
      auth_type = password
      project_domain_name = Default
      user_domain_name = Default
      project_name = service
      username = glance
      password = redhat

      [paste_deploy]
      flavor = keystone

      [glance_store]
      stores = file,http
      default_store = file
      filesystem_store_datadir = /var/lib/glance/images/



[root@controller ~]# vim /etc/glance/glance-registry.conf

      [database]
      connection = mysql+pymysql://glance:redhat@controller/glance

      [keystone_authtoken]
      www_authenticate_uri = http://controller:5000
      auth_url = http://controller:5000
      memcached_servers = controller:11211
      auth_type = password
      project_domain_name = Default
      user_domain_name = Default
      project_name = service
      username = glance
      password = redhat

      [paste_deploy]
      flavor = keystone

[root@controller ~]# su -s /bin/sh -c "glance-manage db_sync" glance


[root@controller ~]# systemctl start openstack-glance-api.service   openstack-glance-registry.service
[root@controller ~]# systemctl enable openstack-glance-api.service  openstack-glance-registry.service
      Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-glance-api.service to /usr/lib/systemd/system/openstack-glance-api.service.
      Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-glance-registry.service to /usr/lib/systemd/system/openstack-glance-registry.service.

[root@controller ~]# systemctl status openstack-glance-api.service
      ● openstack-glance-api.service - OpenStack Image Service (code-named Glance) API server
         Loaded: loaded (/usr/lib/systemd/system/openstack-glance-api.service; enabled; vendor preset: disabled)
         Active: active (running) since Mon 2019-09-30 15:33:42 CST; 46s ago
       Main PID: 17009 (glance-api)
         CGroup: /system.slice/openstack-glance-api.service
                 ├─17009 /usr/bin/python2 /usr/bin/glance-api
                 └─17033 /usr/bin/python2 /usr/bin/glance-api

      Sep 30 15:33:44 controller glance-api[17009]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprecated... separately.
      Sep 30 15:33:44 controller glance-api[17009]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:44 controller glance-api[17009]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprecated... separately.
      Sep 30 15:33:44 controller glance-api[17009]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:45 controller glance-api[17009]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprecated... separately.
      Sep 30 15:33:45 controller glance-api[17009]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:45 controller glance-api[17009]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprecated... separately.
      Sep 30 15:33:45 controller glance-api[17009]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:45 controller glance-api[17009]: /usr/lib/python2.7/site-packages/paste/deploy/util.py:55: DeprecationWarning: Using function/method 'Healthcheck.factory()' is ... as a filter
      Sep 30 15:33:45 controller glance-api[17009]: val = callable(*args, **kw)
      Hint: Some lines were ellipsized, use -l to show in full.


[root@controller ~]# systemctl status openstack-glance-registry.service
      ● openstack-glance-registry.service - OpenStack Image Service (code-named Glance) Registry server
         Loaded: loaded (/usr/lib/systemd/system/openstack-glance-registry.service; enabled; vendor preset: disabled)
         Active: active (running) since Mon 2019-09-30 15:33:42 CST; 1min 18s ago
       Main PID: 17010 (glance-registry)
         CGroup: /system.slice/openstack-glance-registry.service
                 ├─17010 /usr/bin/python2 /usr/bin/glance-registry
                 └─17031 /usr/bin/python2 /usr/bin/glance-registry

      Sep 30 15:33:44 controller glance-registry[17010]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprec...separately.
      Sep 30 15:33:44 controller glance-registry[17010]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:44 controller glance-registry[17010]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprec...separately.
      Sep 30 15:33:44 controller glance-registry[17010]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:44 controller glance-registry[17010]: /usr/lib/python2.7/site-packages/paste/deploy/loadwsgi.py:22: PkgResourcesDeprecationWarning: Parameters to load are deprec...separately.
      Sep 30 15:33:44 controller glance-registry[17010]: return pkg_resources.EntryPoint.parse("x=" + s).load(False)
      Sep 30 15:33:45 controller glance-registry[17010]: /usr/lib/python2.7/site-packages/glance/registry/api/__init__.py:36: DeprecationWarning: Glance Registry service has been d...or removal.
      Sep 30 15:33:45 controller glance-registry[17010]: debtcollector.deprecate("Glance Registry service has been "
      Sep 30 15:33:45 controller glance-registry[17010]: /usr/lib/python2.7/site-packages/paste/deploy/util.py:55: DeprecationWarning: Using function/method 'Healthcheck.factory()'...as a filter
      Sep 30 15:33:45 controller glance-registry[17010]: val = callable(*args, **kw)
      Hint: Some lines were ellipsized, use -l to show in full.


----------------------------------------------------------------------------------------------------
https://docs.openstack.org/placement/stein/install/
https://docs.openstack.org/placement/stein/install/install-rdo.html

Placement Service


[root@controller ~]# mysql -u root -p
      Enter password:

      MariaDB [(none)]> CREATE DATABASE placement;
      Query OK, 1 row affected (0.001 sec)

      MariaDB [(none)]> GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'localhost' IDENTIFIED BY 'redhat';
      Query OK, 0 rows affected (0.001 sec)

      MariaDB [(none)]> GRANT ALL PRIVILEGES ON placement.* TO 'placement'@'%' IDENTIFIED BY 'redhat';
      Query OK, 0 rows affected (0.001 sec)

      MariaDB [(none)]> show databases;
      +--------------------+
      | Database           |
      +--------------------+
      | glance             |
      | information_schema |
      | keystone           |
      | mysql              |
      | performance_schema |
      | placement          |
      +--------------------+
      6 rows in set (0.001 sec)

      MariaDB [(none)]> quit
      Bye


[root@controller ~]# source admin-openrc
[root@controller ~]# openstack user create --domain default --password-prompt placement
      User Password:
      Repeat User Password:
      +---------------------+----------------------------------+
      | Field               | Value                            |
      +---------------------+----------------------------------+
      | domain_id           | default                          |
      | enabled             | True                             |
      | id                  | 6a8b5438b01c4528be876568657a5373 |
      | name                | placement                        |
      | options             | {}                               |
      | password_expires_at | None                             |
      +---------------------+----------------------------------+


[root@controller ~]# openstack role add --project service --user placement admin

// Create the Placement API entry in the service catalog:
[root@controller ~]# openstack service create --name placement --description "Placement API" placement
      +-------------+----------------------------------+
      | Field       | Value                            |
      +-------------+----------------------------------+
      | description | Placement API                    |
      | enabled     | True                             |
      | id          | 32da6a9dad3047959c03efb9301c68ab |
      | name        | placement                        |
      | type        | placement                        |
      +-------------+----------------------------------+


// Create the Placement API service endpoints:
[root@controller ~]# openstack endpoint create --region RegionOne placement public http://controller:8778
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | ac4d6591f2f74b2394b3d9eaad1e01ca |
      | interface    | public                           |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 32da6a9dad3047959c03efb9301c68ab |
      | service_name | placement                        |
      | service_type | placement                        |
      | url          | http://controller:8778           |
      +--------------+----------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne placement internal http://controller:8778
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | f1db9f90203f477fb23dff0824a75f72 |
      | interface    | internal                         |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 32da6a9dad3047959c03efb9301c68ab |
      | service_name | placement                        |
      | service_type | placement                        |
      | url          | http://controller:8778           |
      +--------------+----------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne placement admin http://controller:8778
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | 1645b7c9908845979d29d3c79d40b1a7 |
      | interface    | admin                            |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 32da6a9dad3047959c03efb9301c68ab |
      | service_name | placement                        |
      | service_type | placement                        |
      | url          | http://controller:8778           |
      +--------------+----------------------------------+


Install and configure components (安装配置组件)

[root@controller ~]# yum -y install openstack-placement-api


[root@controller ~]# vim  /etc/placement/placement.conf
    [placement_database]
    connection = mysql+pymysql://placement:redhat@controller/placement

    [api]
    auth_strategy = keystone

    [keystone_authtoken]
    auth_url = http://controller:5000/v3
    memcached_servers = controller:11211
    auth_type = password
    project_domain_name = default
    user_domain_name = default
    project_name = service
    username = placement
    password = redhat



[root@controller ~]# su -s /bin/sh -c "placement-manage db sync" placement


[root@controller ~]# systemctl restart httpd




----------------------------------------------------------------------------------------------------
https://docs.openstack.org/nova/stein/install/
https://docs.openstack.org/nova/stein/install/overview.html
https://docs.openstack.org/nova/stein/install/get-started-compute.html


Compute service

--------------------------------------------------------------------------------
https://docs.openstack.org/nova/stein/install/get-started-compute.html

Compute service overview(Compute service 概览)

OpenStack Compute consists of the following areas and their components(OpenStack Compute 的组件):

    - nova-api service
        Accepts and responds to end user compute API calls. The service supports the OpenStack Compute API.
        It enforces some policies and initiates most orchestration activities, such as running an instance.

    - nova-api-metadata service
        Accepts metadata requests from instances. The nova-api-metadata service is generally used when you run
        in multi-host mode with nova-network installations. For details, see Metadata service in the Compute Administrator Guide.

            https://docs.openstack.org/nova/stein/admin/networking-nova.html#metadata-service-deploy

    - nova-compute service
        A worker daemon that creates and terminates virtual machine instances through hypervisor APIs. For example:

            - XenAPI for XenServer/XCP
            - libvirt for KVM or QEMU
            - VMwareAPI for VMware

        Processing is fairly complex. Basically, the daemon accepts actions from the queue and performs
        a series of system commands such as launching a KVM instance and updating its state in the database.

    - nova-scheduler service
        Takes a virtual machine instance request from the queue and determines on which compute server host it runs.

    - nova-conductor module
        Mediates interactions between the nova-compute service and the database. It eliminates
        direct accesses to the cloud database made by the nova-compute service.
        The nova-conductor module scales horizontally. However, do not deploy it
        on nodes where the nova-compute service runs. For more information, see the conductor section in the Configuration Options.

    - nova-consoleauth daemon
        Authorizes tokens for users that console proxies provide. See nova-novncproxy and nova-xvpvncproxy.
        This service must be running for console proxies to work. You can run proxies of either
        type against a single nova-consoleauth service in a cluster configuration. For information, see About nova-consoleauth.

            https://docs.openstack.org/nova/stein/admin/remote-console-access.html#about-nova-consoleauth

        Deprecated since version 18.0.0: nova-consoleauth is deprecated since 18.0.0 (Rocky)
        and will be removed in an upcoming release. See workarounds.enable_consoleauth for details.

    - nova-novncproxy daemon
        Provides a proxy for accessing running instances through a VNC connection. Supports browser-based novnc clients.
    - nova-spicehtml5proxy daemon
        Provides a proxy for accessing running instances through a SPICE connection. Supports browser-based HTML5 client.
    - nova-xvpvncproxy daemon
        Provides a proxy for accessing running instances through a VNC connection. Supports an OpenStack-specific Java client.

           Deprecated since version 19.0.0: nova-xvpvnxproxy is deprecated since 19.0.0 (Stein) and will be removed in an upcoming release.

    - The queue
        A central hub for passing messages between daemons. Usually implemented with RabbitMQ, also can be implemented with another AMQP message queue, such as ZeroMQ.

    - SQL database
        Stores most build-time and run-time states for a cloud infrastructure, including:

            - Available instance types
            - Instances in use
            - Available networks
            - Projects

        Theoretically, OpenStack Compute can support any database that SQLAlchemy supports.
        Common databases are SQLite3 for test and development work, MySQL, MariaDB, and PostgreSQL.




----------------------------------------------------------------------------------------------------
https://docs.openstack.org/nova/stein/install/controller-install.html


在 controller node 上安装配置 Compute service(代号: nova)

[root@controller ~]# mysql -u root -p
    Enter password:

    MariaDB [(none)]> CREATE DATABASE nova_api;
    Query OK, 1 row affected (0.000 sec)

    MariaDB [(none)]> CREATE DATABASE nova;
    Query OK, 1 row affected (0.001 sec)

    MariaDB [(none)]> CREATE DATABASE nova_cell0;
    Query OK, 1 row affected (0.001 sec)

    MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'localhost' IDENTIFIED BY 'redhat';
    MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_api.* TO 'nova'@'%' IDENTIFIED BY 'redhat';

    MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'localhost' IDENTIFIED BY 'redhat';
    MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova.* TO 'nova'@'%' IDENTIFIED BY 'redhat';

    MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'localhost' IDENTIFIED BY 'redhat';
    MariaDB [(none)]> GRANT ALL PRIVILEGES ON nova_cell0.* TO 'nova'@'%' IDENTIFIED BY 'redhat';

    MariaDB [(none)]> show databases;
        +--------------------+
        | Database           |
        +--------------------+
        | glance             |
        | information_schema |
        | keystone           |
        | mysql              |
        | nova               | <----
        | nova_api           | <----
        | nova_cell0         | <----
        | performance_schema |
        | placement          |
        +--------------------+
        9 rows in set (0.001 sec)

    MariaDB [(none)]> quit
    Bye



[root@controller ~]# source admin-openrc


// Create the Compute service credentials:
[root@controller ~]# openstack user create --domain default --password-prompt nova
    User Password:
    Repeat User Password:
    +---------------------+----------------------------------+
    | Field               | Value                            |
    +---------------------+----------------------------------+
    | domain_id           | default                          |
    | enabled             | True                             |
    | id                  | a4152a02462d41ebb6d058405f39a1e2 |
    | name                | nova                             |
    | options             | {}                               |
    | password_expires_at | None                             |
    +---------------------+----------------------------------+

[root@controller ~]# openstack role add --project service --user nova admin

[root@controller ~]# openstack service create --name nova --description "OpenStack Compute" compute
    +-------------+----------------------------------+
    | Field       | Value                            |
    +-------------+----------------------------------+
    | description | OpenStack Compute                |
    | enabled     | True                             |
    | id          | 9e7759cb008b4d2384d94fb415c28871 |
    | name        | nova                             |
    | type        | compute                          |
    +-------------+----------------------------------+


// Create the Compute API service endpoints:
[root@controller ~]# openstack endpoint create --region RegionOne compute public http://controller:8774/v2.1
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | 8af9d318185b48a18c821650cc1700fa |
      | interface    | public                           |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 9e7759cb008b4d2384d94fb415c28871 |
      | service_name | nova                             |
      | service_type | compute                          |
      | url          | http://controller:8774/v2.1      |
      +--------------+----------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne compute internal http://controller:8774/v2.1
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | d23e327b4a73450c86c1ce83869e1ebb |
      | interface    | internal                         |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 9e7759cb008b4d2384d94fb415c28871 |
      | service_name | nova                             |
      | service_type | compute                          |
      | url          | http://controller:8774/v2.1      |
      +--------------+----------------------------------+
[root@controller ~]# openstack endpoint create --region RegionOne compute admin http://controller:8774/v2.1
      +--------------+----------------------------------+
      | Field        | Value                            |
      +--------------+----------------------------------+
      | enabled      | True                             |
      | id           | cca14f6a187042b0850937a90fa91197 |
      | interface    | admin                            |
      | region       | RegionOne                        |
      | region_id    | RegionOne                        |
      | service_id   | 9e7759cb008b4d2384d94fb415c28871 |
      | service_name | nova                             |
      | service_type | compute                          |
      | url          | http://controller:8774/v2.1      |
      +--------------+----------------------------------+



Install and configure components(安装配置组件)

[root@controller ~]# yum -y install openstack-nova-api openstack-nova-conductor \
                                    openstack-nova-novncproxy openstack-nova-scheduler


[root@controller ~]# vim /etc/nova/nova.conf

      [DEFAULT]
      enabled_apis = osapi_compute,metadata

      [api_database]
      connection = mysql+pymysql://nova:redhat@controller/nova_api

      [database]
      connection = mysql+pymysql://nova:redhat@controller/nova


[root@controller ~]# vim /etc/nova/nova.conf

      [DEFAULT]
      transport_url = rabbit://openstack:redhat@controller

      [api]
      auth_strategy = keystone

      [keystone_authtoken]
      auth_url = http://controller:5000/v3
      memcached_servers = controller:11211
      auth_type = password
      project_domain_name = Default
      user_domain_name = Default
      project_name = service
      username = nova
      password = redhat



[root@controller ~]# vim /etc/nova/nova.conf

      [DEFAULT]
      my_ip = 192.168.175.11

[root@controller ~]# vim /etc/nova/nova.conf

      [DEFAULT]
      use_neutron = true
      firewall_driver = nova.virt.firewall.NoopFirewallDriver



    Note(注):
        By default, Compute uses an internal firewall driver. Since the Networking service includes a firewall driver,
        you must disable the Compute firewall driver by using the nova.virt.firewall.NoopFirewallDriver firewall driver.


// Configure the [neutron] section of /etc/nova/nova.conf. Refer to the Networking service install guide for more details.
// https://docs.openstack.org/neutron/stein/install/compute-install-rdo.html
[root@controller ~]# vim /etc/nova/nova.conf

      [neutron]
      url = http://controller:9696
      auth_url = http://controller:5000
      auth_type = password
      project_domain_name = default
      user_domain_name = default
      region_name = RegionOne
      project_name = service
      username = neutron
      password = redhat


[root@controller ~]# vim /etc/nova/nova.conf

    [vnc]
    enabled = true

    server_listen = $my_ip
    server_proxyclient_address = $my_ip


    [glance]
    api_servers = http://controller:9292

    [oslo_concurrency]
    lock_path = /var/lib/nova/tmp

    [placement]
    region_name = RegionOne
    project_domain_name = Default
    project_name = service
    auth_type = password
    user_domain_name = Default
    auth_url = http://controller:5000/v3
    username = placement
    password = redhat


// Populate the nova-api database:
[root@controller ~]# su -s /bin/sh -c "nova-manage api_db sync" nova


// Register the cell0 database:
[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 map_cell0" nova


// Create the cell1 cell:
[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 create_cell --name=cell1 --verbose" nova
      148f1573-7ae8-4b57-b566-e7e907f786e7

// Populate the nova database:
[root@controller ~]# su -s /bin/sh -c "nova-manage db sync" nova

[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 list_cells" nova
    +-------+--------------------------------------+------------------------------------+-------------------------------------------------+----------+
    |  Name |                 UUID                 |           Transport URL            |               Database Connection               | Disabled |
    +-------+--------------------------------------+------------------------------------+-------------------------------------------------+----------+
    | cell0 | 00000000-0000-0000-0000-000000000000 |               none:/               | mysql+pymysql://nova:****@controller/nova_cell0 |  False   |
    | cell1 | 148f1573-7ae8-4b57-b566-e7e907f786e7 | rabbit://openstack:****@controller |    mysql+pymysql://nova:****@controller/nova    |  False   |
    +-------+--------------------------------------+------------------------------------+-------------------------------------------------+----------+


[root@controller ~]# systemctl start openstack-nova-api.service \
                                openstack-nova-scheduler.service \
                                openstack-nova-conductor.service openstack-nova-novncproxy.service

[root@controller ~]# systemctl enable openstack-nova-api.service \
                                openstack-nova-scheduler.service \
                                openstack-nova-conductor.service openstack-nova-novncproxy.service

  Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-nova-api.service to /usr/lib/systemd/system/openstack-nova-api.service.
  Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-nova-scheduler.service to /usr/lib/systemd/system/openstack-nova-scheduler.service.
  Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-nova-conductor.service to /usr/lib/systemd/system/openstack-nova-conductor.service.
  Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-nova-novncproxy.service to /usr/lib/systemd/system/openstack-nova-novncproxy.service.


注:
    nova-consoleauth is deprecated since 18.0.0 (Rocky) and will be removed in an upcoming release.
    Console proxies should be deployed per cell. If performing a fresh install (not an upgrade),
    then you likely do not need to install the nova-consoleauth service. See workarounds.enable_consoleauth for details.
          https://docs.openstack.org/nova/stein/configuration/config.html#workarounds.enable_consoleauth


[root@controller ~]# systemctl is-active openstack-nova-api.service \
                                  openstack-nova-scheduler.service \
                                  openstack-nova-conductor.service openstack-nova-novncproxy.service

    active
    active
    active
    active





----------------------------------------------------------------------------------------------------
https://docs.openstack.org/nova/stein/install/compute-install.html
https://docs.openstack.org/nova/stein/install/compute-install-rdo.html

在 compute node 上 安装 配置 Compute service(代号: nova)

[root@compute1 ~]# yum -y install openstack-nova-compute


[root@compute1 ~]# vim /etc/nova/nova.conf

      [DEFAULT]
      enabled_apis = osapi_compute,metadata

      transport_url = rabbit://openstack:redhat@controller


      [api]
      auth_strategy = keystone

      [keystone_authtoken]
      auth_url = http://controller:5000/v3
      memcached_servers = controller:11211
      auth_type = password
      project_domain_name = Default
      user_domain_name = Default
      project_name = service
      username = nova
      password = redhat


[root@compute1 ~]# vim /etc/nova/nova.conf

        [DEFAULT]

        my_ip = 192.168.175.31

        use_neutron = true
        firewall_driver = nova.virt.firewall.NoopFirewallDriver


  Note(注):
      By default, Compute uses an internal firewall service. Since Networking includes a firewall service,
      you must disable the Compute firewall service by using the nova.virt.firewall.NoopFirewallDriver firewall driver.


// Configure the [neutron] section of /etc/nova/nova.conf. Refer to the Networking service install guide for more details.
// https://docs.openstack.org/neutron/stein/install/compute-install-rdo.html#configure-the-compute-service-to-use-the-networking-service
[root@compute1 ~]# vim /etc/nova/nova.conf

        [neutron]
        url = http://controller:9696
        auth_url = http://controller:5000
        auth_type = password
        project_domain_name = default
        user_domain_name = default
        region_name = RegionOne
        project_name = service
        username = neutron
        password = redhat


[root@compute1 ~]# vim /etc/nova/nova.conf

    [vnc]
    enabled = true
    server_listen = 0.0.0.0
    server_proxyclient_address = $my_ip
    novncproxy_base_url = http://controller:6080/vnc_auto.html


  Note(注):
    If the web browser to access remote consoles resides on a host that cannot resolve the controller hostname,
    you must replace controller with the management interface IP address of the controller node.
    // 按本示例中的配置, 访问远程 consoles 的 web browser 的 主机 必须能够 解析主机名 'controller',  否则应该把
    // url 中的主机名 controller 替换为其 对应的 ip 地址



[root@compute1 ~]# vim /etc/nova/nova.conf

      [glance]
      api_servers = http://controller:9292

      [oslo_concurrency]
      lock_path = /var/lib/nova/tmp

      [placement]
      region_name = RegionOne
      project_domain_name = Default
      project_name = service
      auth_type = password
      user_domain_name = Default
      auth_url = http://controller:5000/v3
      username = placement
      password = redhat




// Determine whether your compute node supports hardware acceleration for virtual machines:
[root@compute1 ~]# grep -E -o '(vmx|svm)' /proc/cpuinfo
      vmx

[root@compute1 ~]# grep -E -c '(vmx|svm)' /proc/cpuinfo
      1


[root@compute1 ~]# vim /etc/nova/nova.conf

      [libvirt]
      # 因为我的 vmware 虚拟机实例 设置为了 支持硬件加速, 所以这里配置为使用kvm,
      # 如果不支持硬件加速, 则可以设置 virt_type=qemu, 但是这样的话 性能要慢一些
      virt_type=kvm


[root@compute1 ~]# systemctl start libvirtd.service openstack-nova-compute.service
[root@compute1 ~]# systemctl enable libvirtd.service openstack-nova-compute.service
      Created symlink from /etc/systemd/system/multi-user.target.wants/openstack-nova-compute.service to /usr/lib/systemd/system/openstack-nova-compute.service.


[root@compute1 ~]# systemctl status libvirtd.service
      ● libvirtd.service - Virtualization daemon
         Loaded: loaded (/usr/lib/systemd/system/libvirtd.service; enabled; vendor preset: enabled)
         Active: active (running) since Mon 2019-09-30 20:54:01 CST; 43s ago
           Docs: man:libvirtd(8)
                 https://libvirt.org
       Main PID: 2253 (libvirtd)
         CGroup: /system.slice/libvirtd.service
                 └─2253 /usr/sbin/libvirtd

      Sep 30 20:54:00 compute1 systemd[1]: Starting Virtualization daemon...
      Sep 30 20:54:01 compute1 systemd[1]: Started Virtualization daemon.


[root@compute1 ~]# systemctl status  openstack-nova-compute.service
      ● openstack-nova-compute.service - OpenStack Nova Compute Server
         Loaded: loaded (/usr/lib/systemd/system/openstack-nova-compute.service; enabled; vendor preset: disabled)
         Active: active (running) since Mon 2019-09-30 20:54:10 CST; 1min 6s ago
       Main PID: 2270 (nova-compute)
         CGroup: /system.slice/openstack-nova-compute.service
                 └─2270 /usr/bin/python2 /usr/bin/nova-compute

      Sep 30 20:54:01 compute1 systemd[1]: Starting OpenStack Nova Compute Server...
      Sep 30 20:54:10 compute1 systemd[1]: Started OpenStack Nova Compute Server.



Add the compute node to the cell database(注: 在 controller node 上执行如下操作)

[root@controller ~]# source admin-openrc
[root@controller ~]# openstack compute service list --service nova-compute
      +----+--------------+----------+------+---------+-------+----------------------------+
      | ID | Binary       | Host     | Zone | Status  | State | Updated At                 |
      +----+--------------+----------+------+---------+-------+----------------------------+
      |  5 | nova-compute | compute1 | nova | enabled | up    | 2019-09-30T13:00:38.000000 |
      +----+--------------+----------+------+---------+-------+----------------------------+

// Discover compute hosts:
[root@controller ~]# su -s /bin/sh -c "nova-manage cell_v2 discover_hosts --verbose" nova
      Found 2 cell mappings.
      Skipping cell0 since it does not contain hosts.
      Getting computes from cell 'cell1': 148f1573-7ae8-4b57-b566-e7e907f786e7
      Checking host mapping for compute host 'compute1': 8e4eaafe-bdbc-4d89-a3ba-ffc089d581bc
      Creating host mapping for compute host 'compute1': 8e4eaafe-bdbc-4d89-a3ba-ffc089d581bc
      Found 1 unmapped computes in cell: 148f1573-7ae8-4b57-b566-e7e907f786e7



    Note(注):
        When you add new compute nodes, you must run nova-manage cell_v2 discover_hosts
        on the controller node to register those new compute nodes.
        Alternatively, you can set an appropriate interval in /etc/nova/nova.conf:

            [scheduler]
            discover_hosts_in_cells_interval = 300









----------------------------------------------------------------------------------------------------
https://docs.openstack.org/neutron/stein/install/
https://docs.openstack.org/neutron/stein/install/overview.html
https://docs.openstack.org/neutron/stein/install/common/get-started-networking.html



Networking service

      OpenStack Networking Guide:
            https://docs.openstack.org/neutron/stein/admin/index.html



--------------------------------------------------------------------------------
https://docs.openstack.org/neutron/stein/install/common/get-started-networking.html

Networking service overview(Networking service概览)

    OpenStack Networking (neutron) allows you to create and attach interface devices managed
    by other OpenStack services to networks. Plug-ins can be implemented to accommodate
    different networking equipment and software, providing flexibility to OpenStack architecture and deployment.


It includes the following components:

    - neutron-server
        Accepts and routes API requests to the appropriate OpenStack Networking plug-in for action.

    - OpenStack Networking plug-ins and agents
        Plug and unplug ports, create networks or subnets, and provide IP addressing.
        These plug-ins and agents differ depending on the vendor and technologies used
        in the particular cloud. OpenStack Networking ships with plug-ins and agents
        for Cisco virtual and physical switches, NEC OpenFlow products, Open vSwitch, Linux bridging, and the VMware NSX product.

        The common agents are L3 (layer 3), DHCP (dynamic host IP addressing), and a plug-in agent.


    - Messaging queue
        Used by most OpenStack Networking installations to route information between
        the neutron-server and various agents. Also acts as a database to store networking state for particular plug-ins.

    OpenStack Networking mainly interacts with OpenStack Compute to provide networks and connectivity for its instances.


--------------------------------------------------------------------------------
https://docs.openstack.org/neutron/stein/install/concepts.html

Networking (neutron) concepts

    OpenStack Networking (neutron) manages all networking facets for the Virtual Networking Infrastructure (VNI)
    and the access layer aspects of the Physical Networking Infrastructure (PNI) in your OpenStack environment.
    OpenStack Networking enables projects to create advanced virtual network topologies which
    may include services such as a firewall, a load balancer, and a virtual private network (VPN).

    Networking provides networks, subnets, and routers as object abstractions. Each
    abstraction has functionality that mimics its physical counterpart: networks
    contain subnets, and routers route traffic between different subnets and networks.

    Any given Networking set up has at least one external network. Unlike the other networks,
    the external network is not merely a virtually defined network. Instead, it represents
    a view into a slice of the physical, external network accessible outside the
    OpenStack installation. IP addresses on the external network are accessible by anybody physically on the outside network.

    In addition to external networks, any Networking set up has one or more internal networks.
    These software-defined networks connect directly to the VMs. Only the VMs on
    any given internal network, or those on subnets connected through
    interfaces to a similar router, can access VMs connected to that network directly.

    For the outside network to access VMs, and vice versa, routers between
    the networks are needed. Each router has one gateway that is connected
    to an external network and one or more interfaces connected to internal networks.
    Like a physical router, subnets can access machines on other subnets that are
    connected to the same router, and machines can access the outside network through the gateway for the router.

    Additionally, you can allocate IP addresses on external networks to ports
    on the internal network. Whenever something is connected to a subnet,
    that connection is called a port. You can associate external network
    IP addresses with ports to VMs. This way, entities on the outside network can access VMs.

    Networking also supports security groups. Security groups enable administrators to define
    firewall rules in groups. A VM can belong to one or more security groups, and Networking
    applies the rules in those security groups to block or unblock ports, port ranges, or traffic types for that VM.

    Each plug-in that Networking uses has its own concepts. While not vital to operating
    the VNI and OpenStack environment, understanding these concepts can help you
    set up Networking. All Networking installations use a core plug-in and a security
    group plug-in (or just the No-Op security group plug-in). Additionally,
    Firewall-as-a-Service (FWaaS) and Load-Balancer-as-a-Service (LBaaS) plug-ins are available.




--------------------------------------------------------------------------------
https://docs.openstack.org/neutron/stein/install/install-rdo.html

TODO 继续完成该示例




























