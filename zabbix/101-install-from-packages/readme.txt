

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

  zabbix server默认安装后，会自动监控本机；但本机的监控默认是禁用的，若想实现真正本机的监控，需要额外的配置


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


-----------------------------------------------------------------------
示例: 创建一个 区别于 zabbix 用户不同的 用户 zabbix_agent 来 单独运行 zabbix agent 服务
      该 部分仅是官网 考虑到安全因素 而 推荐的做法, 并非必须. 如果嫌 麻烦, 可以直接 跳过(skip)


// 默认 zabbix server 和 agent 服务 都是以 zabbix 用户身份运行, 这有可能导致安全问题, 如 agent 进程 访问 server 的一些敏感信息,
// 可以采用如下方式 让 agent 以不同的用户身份(different user)运行:
//  参考   https://www.zabbix.com/documentation/4.4/manual/installation/requirements/best_practices
//         https://www.zabbix.com/forum/zabbix-help/31161-how-to-change-agent-user-account
//         https://www.zabbix.com/documentation/4.4/manual/appendix/config/zabbix_agentd


[root@zabbix_server ~]# systemctl stop zabbix-agent.service



// 观察一下安装 软件包 zabbix-server-mysql 时生成的文件
[root@zabbix_server ~]# rpm -ql zabbix-server-mysql
    /etc/logrotate.d/zabbix-server
    /etc/zabbix/zabbix_server.conf
    /usr/lib/systemd/system/zabbix-server.service
    /usr/lib/tmpfiles.d/zabbix-server.conf
    /usr/lib/zabbix/alertscripts
    /usr/lib/zabbix/externalscripts
    /usr/sbin/zabbix_server_mysql
    /usr/share/doc/zabbix-server-mysql-4.4.0
    /usr/share/doc/zabbix-server-mysql-4.4.0/AUTHORS
    /usr/share/doc/zabbix-server-mysql-4.4.0/COPYING
    /usr/share/doc/zabbix-server-mysql-4.4.0/ChangeLog
    /usr/share/doc/zabbix-server-mysql-4.4.0/NEWS
    /usr/share/doc/zabbix-server-mysql-4.4.0/README
    /usr/share/doc/zabbix-server-mysql-4.4.0/create.sql.gz
    /usr/share/man/man8/zabbix_server.8.gz
    /var/log/zabbix  <-----------
    /var/run/zabbix  <-----------


// 观察一下安装 软件包 zabbix-agent 时生成的文件
[root@zabbix_server ~]# rpm -ql zabbix-agent
    /etc/logrotate.d/zabbix-agent  <------
    /etc/zabbix/zabbix_agentd.conf
    /etc/zabbix/zabbix_agentd.d
    /etc/zabbix/zabbix_agentd.d/userparameter_mysql.conf
    /usr/lib/systemd/system/zabbix-agent.service
    /usr/lib/tmpfiles.d/zabbix-agent.conf
    /usr/sbin/zabbix_agentd
    /usr/share/doc/zabbix-agent-4.4.0
    /usr/share/doc/zabbix-agent-4.4.0/AUTHORS
    /usr/share/doc/zabbix-agent-4.4.0/COPYING
    /usr/share/doc/zabbix-agent-4.4.0/ChangeLog
    /usr/share/doc/zabbix-agent-4.4.0/NEWS
    /usr/share/doc/zabbix-agent-4.4.0/README
    /usr/share/man/man8/zabbix_agentd.8.gz
    /var/log/zabbix  <---------- 与 zabbix-server-mysql 的 目录 /var/log/zabbix 冲突(本例准备创建新的目录 /var/log/zabbix_agent 来避免此问题)
    /var/run/zabbix  <---------- 与 zabbix-server-mysql 的 目录 /var/run/zabbix 冲突(本例准备创建新的目录 /var/run/zabbix_agent 来避免此问题)





可以发现, 如果 要让 zabbix agent 服务以不同的用户身份(本示例中为用户 'zabbix_agent')运行, 则还要解决 相关目录(权限)冲突的问题.



// 创建一个 不同的用户 'zabbix_agent' 来 运行 zabbix agent 服务
[root@zabbix_server ~]# useradd -M -s /sbin/nologin zabbix_agent
[root@zabbix_server ~]# vim /etc/zabbix/zabbix_agentd.conf

    PidFile=/var/run/zabbix_agent/zabbix_agentd.pid
    User=zabbix_agent
    LogFile=/var/log/zabbix_agent/zabbix_agentd.log



[root@zabbix_server ~]# mkdir /var/log/zabbix_agent
[root@zabbix_server ~]# chown zabbix_agent:zabbix_agent /var/log/zabbix_agent
[root@zabbix_server ~]# ls -ld /var/log/zabbix_agent
      drwxr-xr-x 2 zabbix_agent zabbix_agent 6 Oct 16 18:06 /var/log/zabbix_agent




// 确保 logrotate 以 zabbix_agent 身份来创建 新日志文件
[root@zabbix_server ~]# vim /etc/logrotate.d/zabbix-agent

    /var/log/zabbix_agent/zabbix_agentd.log {
      weekly
      rotate 12
      compress
      delaycompress
      missingok
      notifempty
      create 0664 zabbix_agent zabbix_agent
    }


[root@zabbix_server ~]# cp -a /usr/lib/systemd/system/zabbix-agent.service  /etc/systemd/system/zabbix-agent.service
[root@zabbix_server ~]# vim /etc/systemd/system/zabbix-agent.service

    [Unit]
    Description=Zabbix Agent
    After=syslog.target
    After=network.target

    [Service]
    Environment="CONFFILE=/etc/zabbix/zabbix_agentd.conf"
    EnvironmentFile=-/etc/sysconfig/zabbix-agent
    Type=forking
    Restart=on-failure
    #PIDFile=/run/zabbix/zabbix_agentd.pid
    PIDFile=/var/run/zabbix_agent/zabbix_agentd.pid
    KillMode=control-group
    ExecStart=/usr/sbin/zabbix_agentd -c $CONFFILE

    # 如下 加一行 配置 'ExecStartPost=/bin/sleep 0.1' 是为了解决 如下在该配置未加时 start 的时候报
    # 警告信息: Oct 16 19:30:46 zabbix_server systemd[1]: PID file /var/run/zabbix_agent/zabbix_agentd.pid not readable (yet?) after start.
    # 其实该警告信息直接忽略也是可以的
    # 相关参考:
    # https://blog.csdn.net/yuanfangPOET/article/details/90646154
    # https://access.redhat.com/solutions/1598173
    # https://support.zabbix.com/browse/ZBX-10867
    #    This looks to be similar but there is no issue after stopping and restarting, but rather the
    #    perky warning message due to systemd reading the PID before the service is fully up.
    #                           原因: systemd 在 the service 完全启动之前 读取了 the PID
    ExecStartPost=/bin/sleep 0.1
    ExecStop=/bin/kill -SIGTERM $MAINPID
    RestartSec=10s
    User=zabbix_agent
    Group=zabbix_agent
    # 参考笔记 https://github.com/yangsg/linux_training_notes/blob/master/cluster-storage/125-redis/111-high-availability-redis-sentinel/101-redis-sentinel-demo02/readme.txt
    RuntimeDirectory=zabbix_agent
    RuntimeDirectoryMode=0755

    [Install]
    WantedBy=multi-user.target



[root@zabbix_server ~]# systemctl daemon-reload
[root@zabbix_server ~]# systemctl start zabbix-agent.service

// 重新 enable  zabbix-agent (更新链接)
[root@zabbix_server ~]# systemctl disable zabbix-agent.service
      Removed symlink /etc/systemd/system/multi-user.target.wants/zabbix-agent.service.

[root@zabbix_server ~]# systemctl enable zabbix-agent.service
      Created symlink from /etc/systemd/system/multi-user.target.wants/zabbix-agent.service to /etc/systemd/system/zabbix-agent.service.


[root@zabbix_server ~]# systemctl status zabbix-agent.service
      ● zabbix-agent.service - Zabbix Agent
         Loaded: loaded (/etc/systemd/system/zabbix-agent.service; enabled; vendor preset: disabled)
         Active: active (running) since Wed 2019-10-16 19:42:30 CST; 4s ago
        Process: 25290 ExecStop=/bin/kill -SIGTERM $MAINPID (code=exited, status=0/SUCCESS)
        Process: 25304 ExecStartPost=/bin/sleep 0.1 (code=exited, status=0/SUCCESS)
        Process: 25302 ExecStart=/usr/sbin/zabbix_agentd -c $CONFFILE (code=exited, status=0/SUCCESS)
       Main PID: 25305 (zabbix_agentd)
         CGroup: /system.slice/zabbix-agent.service
                 ├─25305 /usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf
                 ├─25306 /usr/sbin/zabbix_agentd: collector [idle 1 sec]
                 ├─25307 /usr/sbin/zabbix_agentd: listener #1 [waiting for connection]
                 ├─25308 /usr/sbin/zabbix_agentd: listener #2 [waiting for connection]
                 ├─25309 /usr/sbin/zabbix_agentd: listener #3 [waiting for connection]
                 └─25310 /usr/sbin/zabbix_agentd: active checks #1 [idle 1 sec]

      Oct 16 19:42:29 zabbix_server systemd[1]: Starting Zabbix Agent...
      Oct 16 19:42:30 zabbix_server systemd[1]: Started Zabbix Agent.


// 观察一下 运行 zabbix_agentd 的用户
[root@zabbix_server ~]# ps aux | grep zabbix_agent
    zabbix_+  25305  0.0  0.1  78636  1256 ?        S    19:42   0:00 /usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf
    zabbix_+  25306  0.0  0.1  78636  1356 ?        S    19:42   0:00 /usr/sbin/zabbix_agentd: collector [idle 1 sec]
    zabbix_+  25307  0.0  0.2  78752  2460 ?        S    19:42   0:00 /usr/sbin/zabbix_agentd: listener #1 [waiting for connection]
    zabbix_+  25308  0.0  0.2  78752  2564 ?        S    19:42   0:00 /usr/sbin/zabbix_agentd: listener #2 [waiting for connection]
    zabbix_+  25309  0.0  0.2  78752  2472 ?        S    19:42   0:00 /usr/sbin/zabbix_agentd: listener #3 [waiting for connection]
    zabbix_+  25310  0.0  0.2  78636  2092 ?        S    19:42   0:00 /usr/sbin/zabbix_agentd: active checks #1 [idle 1 sec]
    root      25941  0.0  0.0 112660   664 pts/1    R+   20:08   0:00 grep --color=auto zabbix_agent



//注: 因为 用户名 'zabbix_agent' 的名字太长, 显示效果中将 zabbix_agent 截断了 并使用 加号 '+' 来代替,
//      为了解决此问题, 可以采用如下方式:
//      参考  https://askubuntu.com/questions/523673/ps-aux-for-long-charactered-usernames-shows-a-plus-sign
[root@zabbix_server ~]# ps axo user:20,pid,pcpu,pmem,vsz,rss,tty,stat,start,time,comm  | grep zabbix_agent
    zabbix_agent          25305  0.0  0.1  78636  1256 ?        S    19:42:29 00:00:00 zabbix_agentd
    zabbix_agent          25306  0.0  0.1  78636  1356 ?        S    19:42:29 00:00:00 zabbix_agentd
    zabbix_agent          25307  0.0  0.2  78752  2460 ?        S    19:42:29 00:00:00 zabbix_agentd
    zabbix_agent          25308  0.0  0.2  78752  2564 ?        S    19:42:29 00:00:00 zabbix_agentd
    zabbix_agent          25309  0.0  0.2  78752  2472 ?        S    19:42:29 00:00:00 zabbix_agentd
    zabbix_agent          25310  0.0  0.2  78636  2092 ?        S    19:42:29 00:00:00 zabbix_agentd




-----------------------------------------------------------------------


----------------------------------------------------------------------------------------------------

------------------------------
Login and configuring user:

  https://www.zabbix.com/documentation/4.4/manual/quickstart/login

  路线： Administration → Users

    In Zabbix, access rights to hosts are assigned to user groups, not individual users.


    a Zabbix superuser: 'Admin'
    a special default user: 'Guest'



------------------------------
New host

  https://www.zabbix.com/documentation/4.4/manual/quickstart/host

  路线： Configuration → Hosts

host:  (广义)网络实体

    A host in Zabbix is a networked entity (physical, virtual) that you wish to monitor.
    The definition of what can be a “host” in Zabbix is quite flexible.
    It can be a physical server, a network switch, a virtual machine or some application.


一个 pre-defined host: 'Zabbix server'


Host name 的合法字符: Alphanumerics, spaces, dots, dashes and underscores

  注: All access permissions are assigned to host groups, not individual hosts. That is why a host must belong to at least one group.

  注: 如果 Zabbix server 和 Zabbix agent 在同一主机, 则 此处 ip 必须与  zabbix_agentd.conf 中 'Server' 指令 指定的 ip 一致

  关于 'Availability' 列:
     If the ZBX icon in the Availability column is red, there is some error with communication -
     move your mouse cursor over it to see the error message. If that icon is gray,
     no status update has happened so far. Check that Zabbix server is running, and try refreshing the page later as well.

----------
添加远程(remote) 监控主机示例:
//查看 ip 地址
[root@node01 ~]# ip addr show ens33  | awk '/inet / {print $2}'  # 查看 ip 地址
    192.168.175.111/24


// 配置 阿里的 zabbix 镜像 yum 源
[root@node01 ~]# vim /etc/yum.repos.d/zabbix.repo

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


[root@node01 ~]# yum -y install zabbix-agent
[root@node01 ~]# rpm -q zabbix-agent
    zabbix-agent-4.4.0-1.el7.x86_64


[root@node01 ~]# vim /etc/zabbix/zabbix_agentd.conf

    Server=192.168.175.100
    ServerActive=192.168.175.100
    Hostname=node01

[root@node01 ~]# systemctl start zabbix-agent.service
[root@node01 ~]# systemctl enable zabbix-agent.service

[root@node01 ~]# systemctl status zabbix-agent.service
    ● zabbix-agent.service - Zabbix Agent
       Loaded: loaded (/usr/lib/systemd/system/zabbix-agent.service; enabled; vendor preset: disabled)
       Active: active (running) since Thu 2019-10-17 13:07:43 CST; 42s ago
     Main PID: 1347 (zabbix_agentd)
       CGroup: /system.slice/zabbix-agent.service
               ├─1347 /usr/sbin/zabbix_agentd -c /etc/zabbix/zabbix_agentd.conf
               ├─1348 /usr/sbin/zabbix_agentd: collector [idle 1 sec]
               ├─1349 /usr/sbin/zabbix_agentd: listener #1 [waiting for connection]
               ├─1350 /usr/sbin/zabbix_agentd: listener #2 [waiting for connection]
               ├─1351 /usr/sbin/zabbix_agentd: listener #3 [waiting for connection]
               └─1352 /usr/sbin/zabbix_agentd: active checks #1 [idle 1 sec]

    Oct 17 13:07:43 node01 systemd[1]: Starting Zabbix Agent...
    Oct 17 13:07:43 node01 systemd[1]: PID file /run/zabbix/zabbix_agentd.pid not readable (yet?) after start. <---- 这里直接忽略该警告了
    Oct 17 13:07:43 node01 systemd[1]: Started Zabbix Agent.

[root@node01 ~]# netstat -anptu | grep zabbix
    tcp        0      0 0.0.0.0:10050           0.0.0.0:*               LISTEN      1347/zabbix_agentd
    tcp6       0      0 :::10050                :::*                    LISTEN      1347/zabbix_agentd



接下来在页面上执行如下操作:
    1)  创建 host group (路线: Configuration → Host groups)(因为 所有 权限都是被 赋予  host groups, 所以 host 必须至少 属于 one group)
          注: 练习时 可以创建 类似名为 "a_test_host_group" 主机组, 这里加前缀 'a_' 使其 显示在 host groups 列表的第一行, 方便查看和操作
    2)  添加 host


----------------------------------------------------------------------------------------------------
New item

路线: Configuration → Hosts  (因所有 item 按 host 进行分组)

  https://www.zabbix.com/documentation/4.4/manual/quickstart/item



----------------------------------------------------------------------------------------------------














