

https://www.zabbix.com/documentation/4.4/manual/installation/install_from_packages
https://www.zabbix.com/documentation/4.4/manual/installation/install_from_packages/rhel_centos

通过源码安装笔记: https://github.com/yangsg/linux_training_notes/tree/master/zabbix/100-install-from-source


// 配置 zabbix 的国内镜像仓库 (因为有时网络不好, 无法访问下载 zabbix 官网资源)
// 添加 Zabbix repository
//    [root@zabbix_server ~]# rpm -Uvh https://repo.zabbix.com/zabbix/4.4/rhel/7/x86_64/zabbix-release-4.4-1.el7.noarch.rpm
//    [root@zabbix_server ~]# yum -y install yum-utils
//    [root@zabbix_server ~]# yum-config-manager --enable rhel-7-server-optional-rpms


// 参考  https://www.cnblogs.com/caidingyu/p/11423089.html
[root@zabbix_server ~]# vim /etc/yum.repos.d/zabbix.repo

      [zabbix]
      name=Zabbix Official Repository(mirrors.aliyun.com) - $basearch
      baseurl=https://mirrors.aliyun.com/zabbix/zabbix/4.4/rhel/7/x86_64/
      enabled=1
      gpgcheck=0

      [zabbix-non-supported]
      name=Zabbix Official Repository non-supported(mirrors.aliyun.com) - $basearch
      baseurl=https://mirrors.aliyun.com/zabbix/non-supported/rhel/7/x86_64/
      enabled=1
      gpgcheck=0



[root@zabbix_server ~]# yum repolist | grep zabbix
      zabbix               Zabbix Official Repository(mirrors.aliyun.com) - x86     15
      zabbix-non-supported Zabbix Official Repository non-supported(mirrors.ali      4





// 安装 Zabbix server
[root@localhost ~]# yum -y install zabbix-server-mysql zabbix-get  #这里同时将 命令 zabbix_get 所在的包也装上

// 安装 支持 mysql/apache 的 Zabbix frontend
[root@localhost ~]# yum -y install zabbix-web-mysql

    注:
      centos8 上 安装支持 mysql/apache 的 Zabbix frontend 使用命令: `yum install zabbix-web-mysql zabbix-apache-conf`

      如果是想要安装 支持 mysql/nginx 的 Zabbix frontend, 则 centos7/8 上都使用如下命令:

              yum install epel-release
              yum install zabbix-web-mysql zabbix-nginx-conf


--------------------------------------------------
// 安装 mysql 数据库(此处安装 mariadb)
// 参考 https://github.com/yangsg/linux_training_notes/tree/master/zabbix/100-install-from-source
//      https://www.zabbix.com/documentation/4.4/manual/appendix/install/db_scripts#mysql
[root@zabbix_server ~]# yum -y install mariadb-server
[root@zabbix_server ~]# rpm -q mariadb-server
    mariadb-server-5.5.64-1.el7.x86_64

[root@zabbix_server ~]# systemctl start mariadb.service
[root@zabbix_server ~]# systemctl enable mariadb.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/mariadb.service to /usr/lib/systemd/system/mariadb.service.


[root@zabbix_server ~]# systemctl status mariadb.service
    ● mariadb.service - MariaDB database server
       Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
       Active: active (running) since Mon 2019-10-14 17:34:42 CST; 31s ago
     Main PID: 1470 (mysqld_safe)
       CGroup: /system.slice/mariadb.service
               ├─1470 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
               └─1632 /usr/libexec/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib64/mysql/plugin --log-error=/var/log/mariadb/mariadb.log --pid-file=/var/run/mariadb/m...

    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: MySQL manual for more instructions.
    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: Please report any problems at http://mariadb.org/jira
    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: The latest information about MariaDB is available at http://mariadb.org/.
    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: You can find additional information about the MySQL part at:
    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: http://dev.mysql.com
    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: Consider joining MariaDB's strong and vibrant community:
    Oct 14 17:34:40 zabbix_server mariadb-prepare-db-dir[1384]: https://mariadb.org/get-involved/
    Oct 14 17:34:40 zabbix_server mysqld_safe[1470]: 191014 17:34:40 mysqld_safe Logging to '/var/log/mariadb/mariadb.log'.
    Oct 14 17:34:40 zabbix_server mysqld_safe[1470]: 191014 17:34:40 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql
    Oct 14 17:34:42 zabbix_server systemd[1]: Started MariaDB database server.


// 初始化 mysql 数据库的安全设置
[root@zabbix_server ~]# mysql_secure_installation

      Enter current password for root (enter for none):  <====直接按 enter 键回车

      Set root password? [Y/n] y   <======键入 y
      New password:   <======键入新的root密码, 本示例只用 'redhat'
      Re-enter new password: <======重新键入新root密码
      Password updated successfully!
      Reloading privilege tables..
       ... Success!


// 创建 zabbix 数据库 及 相关用户 并 授权
// 参考:  https://www.zabbix.com/documentation/4.4/manual/appendix/install/db_scripts#mysql
[root@zabbix_server ~]# mysql -uroot -p
    Enter password:

    // 注: zabbix 必须使用 字符集 utf8 和 比较规则 utf8_bin
    MariaDB [(none)]> create database zabbix character set utf8 collate utf8_bin;
    MariaDB [(none)]> grant all privileges on zabbix.* to zabbix@localhost identified by 'redhat';
    MariaDB [(none)]> quit



// 为 zabbix-server 导入 mysql 的 initial schema 和 data
// 导入之前可以观察一下  create.sql.gz 包含的 sql 脚本干了什么事情 (果然是创建表 和 插入数据)
[root@zabbix_server ~]# zcat /usr/share/doc/zabbix-server-mysql-4.4.0/create.sql.gz | less

      CREATE TABLE `users` (
              `userid`                 bigint unsigned                           NOT NULL,
              `alias`                  varchar(100)    DEFAULT ''                NOT NULL,
              `name`                   varchar(100)    DEFAULT ''                NOT NULL,

                  略 略 略 略 略 略 略

// 执行导入数据操作
[root@zabbix_server ~]# zcat /usr/share/doc/zabbix-server-mysql-4.4.0/create.sql.gz | mysql -uzabbix -p zabbix

// 可以观察一下 数据库 zabbix 中新创建的一些表
[root@zabbix_server ~]# mysql -u root -p -t -e 'show tables from zabbix' | less


// 修改  zabbix_server.conf 配置文件, 为 Zabbix server 配置数据库信息
[root@zabbix_server ~]# vim /etc/zabbix/zabbix_server.conf

      DBHost=localhost
      DBName=zabbix
      DBUser=zabbix
      DBPassword=redhat


// 观察一下当前 zabbix_server.conf 中所有的配置情况
[root@zabbix_server ~]# grep -E -v '^#|^[[:space:]]*$' /etc/zabbix/zabbix_server.conf
      LogFile=/var/log/zabbix/zabbix_server.log
      LogFileSize=0
      PidFile=/var/run/zabbix/zabbix_server.pid
      SocketDir=/var/run/zabbix
      DBHost=localhost
      DBName=zabbix
      DBUser=zabbix
      DBPassword=redhat
      SNMPTrapperFile=/var/log/snmptrap/snmptrap.log
      Timeout=4
      AlertScriptsPath=/usr/lib/zabbix/alertscripts
      ExternalScripts=/usr/lib/zabbix/externalscripts
      LogSlowQueries=3000
      StatsAllowedIP=127.0.0.1


// 启动 Zabbix server 服务相关的进程
[root@zabbix_server ~]# systemctl start zabbix-server httpd
[root@zabbix_server ~]# systemctl enable zabbix-server httpd
    Created symlink from /etc/systemd/system/multi-user.target.wants/zabbix-server.service to /usr/lib/systemd/system/zabbix-server.service.
    Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.


// 观察一下 zabbix 的端口信息(注: 实际还应该观察一下 httpd 的端口信息)
[root@zabbix_server ~]# netstat -anptu | grep zabbix
      tcp        0      0 0.0.0.0:10051           0.0.0.0:*               LISTEN      1840/zabbix_server
      tcp6       0      0 :::10051                :::*                    LISTEN      1840/zabbix_server



// 配置 Zabbix frontend
到这里, 依然可以像 通过源码 安装 zabbix 的时候一样, 可以用浏览器访问一下 http://192.168.175.100/zabbix/setup.php
在 "Check of pre-requisites" 步骤的页面中 观察一下 所有模块 和 参数设置 是否都符合要求了。
可以看到, date.timezone 现在还没有设置

    注: Note that in RHEL 7 (but not in RHEL 8) it's necessary to uncomment and set the right date.timezone setting for you.

[root@zabbix_server ~]# vim /etc/httpd/conf.d/zabbix.conf

    php_value max_execution_time 300
    php_value memory_limit 128M
    php_value post_max_size 16M
    php_value upload_max_filesize 2M
    php_value max_input_time 300
    php_value max_input_vars 10000
    php_value always_populate_raw_post_data -1
    # 注: 如上的参数都已经默认配置好了, 这里仅需配置一下 时区 即可
    php_value date.timezone Asia/Shanghai


// 重新加载 httpd, 使如上的配置修改生效
[root@zabbix_server ~]# systemctl reload httpd

参考 https://www.zabbix.com/documentation/4.4/manual/installation/install#installing_frontend
在页面
   http://192.168.175.100/zabbix/setup.php
上完成 zabbix frontend 的配置



// 最后查看 通过在页面 setup.php 上操作生成的 zabbix.conf.php 配置文件:
[root@zabbix_server ~]# cat /etc/zabbix/web/zabbix.conf.php

      <?php
      // Zabbix GUI configuration file.
      global $DB;

      $DB['TYPE']     = 'MYSQL';
      $DB['SERVER']   = 'localhost';
      $DB['PORT']     = '3306';
      $DB['DATABASE'] = 'zabbix';
      $DB['USER']     = 'zabbix';
      $DB['PASSWORD'] = 'redhat';

      // Schema name. Used for IBM DB2 and PostgreSQL.
      $DB['SCHEMA'] = '';

      $ZBX_SERVER      = 'localhost';
      $ZBX_SERVER_PORT = '10051';
      $ZBX_SERVER_NAME = 'zabbix_server';

      $IMAGE_FORMAT_DEFAULT = IMAGE_FORMAT_PNG;



此时浏览器 访问   http://192.168.175.100/zabbix/
则 显示的是 zabbix 的登录表单，键入默认的用户信息登录即可, 如下:

      default username: Admin
      default password: zabbix

成功则跳转到 Dashboard 页面



----------------------------------------------------------------------------------------------------
在 zabbix_server 安装 agent, 实现 自监控


// 安装 zabbix-agent
[root@zabbix_server ~]# yum -y install zabbix-agent


// 在 zabbix_agentd.conf 中配置 zabbix server 地址信息 及 agent 所在被监控主机的名称作为唯一标志
[root@zabbix_server ~]# vim /etc/zabbix/zabbix_agentd.conf

      # agent 被动模式下zabbix server的地址
      Server=192.168.175.100
      # agent 主动模式下zabbix server的地址
      ServerActive=192.168.175.100
      # 被监控机的显示名称
      Hostname=zabbix_server


// 启动 zabbix-agent 服务并设为开机自启
[root@zabbix_server ~]# systemctl start zabbix-agent.service
[root@zabbix_server ~]# systemctl enable zabbix-agent.service
      Created symlink from /etc/systemd/system/multi-user.target.wants/zabbix-agent.service to /usr/lib/systemd/system/zabbix-agent.service.

[root@zabbix_server ~]# systemctl status zabbix-agent.service
    ● zabbix-agent.service - Zabbix Agent
       Loaded: loaded (/usr/lib/systemd/system/zabbix-agent.service; enabled; vendor preset: disabled)
       Active: active (running) since Wed 2019-10-16 15:44:05 CST; 26s ago
     Main PID: 18451 (zabbix_agentd)
       CGroup: /system.slice/zabbix-agent.service
               ├─18451 /usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf
               ├─18452 /usr/sbin/zabbix_agentd: collector [idle 1 sec]
               ├─18453 /usr/sbin/zabbix_agentd: listener #1 [waiting for connection]
               ├─18454 /usr/sbin/zabbix_agentd: listener #2 [waiting for connection]
               ├─18455 /usr/sbin/zabbix_agentd: listener #3 [waiting for connection]
               └─18456 /usr/sbin/zabbix_agentd: active checks #1 [idle 1 sec]

    Oct 16 15:44:05 zabbix_server systemd[1]: Starting Zabbix Agent...
    Oct 16 15:44:05 zabbix_server systemd[1]: PID file /run/zabbix/zabbix_agentd.pid not readable (yet?) after start.
    Oct 16 15:44:05 zabbix_server systemd[1]: Started Zabbix Agent.


// 观察 一下 端口信息
[root@zabbix_server ~]# netstat -anptu | grep zabbix
    tcp        0      0 0.0.0.0:10050           0.0.0.0:*               LISTEN      18451/zabbix_agentd
    tcp        0      0 0.0.0.0:10051           0.0.0.0:*               LISTEN      1763/zabbix_server
    tcp6       0      0 :::10050                :::*                    LISTEN      18451/zabbix_agentd
    tcp6       0      0 :::10051                :::*                    LISTEN      1763/zabbix_server


    web操作: 在页面 [Configuration\Hosts] 上操作将 agent 的 Interface 字段对应的 ip(即127.0.0.1) 修改为 192.168.175.100,
    同时将其 Hostname 改为 zabbix_server (因为本示例在 zabbix_agentd.conf 中修改了 Hostname, 最好保持一致以便区分)
    等待一段时间后,  "Availability" 字段下的  "ZBX"  图标会 变为 绿色(green), 表示 可以正常收集 agent 主机信息



----------------------------------------------------------------------------------------------------



















