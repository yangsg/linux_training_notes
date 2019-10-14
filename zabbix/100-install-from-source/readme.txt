
安装手册: https://www.zabbix.com/documentation/4.4/manual/installation/install

zabbix 的 tarball 包下载页面: https://www.zabbix.com/download_sources

// 构建基础的编译环境
[root@zabbix_server ~]# yum -y install gcc gcc-c++ autoconf automake


// 下载 zabbix 源码包
[root@zabbix_server ~]# ls download/
    zabbix-4.4.0.tar.gz

// 创建 zabbix 用户
[root@zabbix_server ~]# useradd -r -d /usr/lib/zabbix -s /sbin/nologin zabbix


----------------------------------------------------------------------------------------------------
// 创建 zabbix 数据库 (注: zabbix 的 server 和 proxy 需要数据库, 但是 agent 不需要)
// 参考:    https://www.zabbix.com/documentation/4.4/manual/appendix/install/db_scripts
// zabbix 仅支持 UTF-8, 其没有安全缺陷. 所以这里没有特殊需求, 就没必要使用 utf8mb4 了

// 安装 mysql 数据库(此处安装 mariadb)
[root@zabbix_server ~]# yum -y install mariadb-server
[root@zabbix_server ~]# rpm -q mariadb-server
    mariadb-server-5.5.64-1.el7.x86_64


[root@zabbix_server ~]# systemctl start mariadb.service
[root@zabbix_server ~]# systemctl enable mariadb.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/mariadb.service to /usr/lib/systemd/system/mariadb.service.

[root@zabbix_server ~]# systemctl status mariadb.service
    ● mariadb.service - MariaDB database server
       Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
       Active: active (running) since Sun 2019-10-13 21:05:26 CST; 22s ago
     Main PID: 1583 (mysqld_safe)
       CGroup: /system.slice/mariadb.service
               ├─1583 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
               └─1745 /usr/libexec/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib64/mysql/plugin --log-error=/var/log/mariadb/mariadb.log --pid-file=/var/run/mariadb/m...

    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: MySQL manual for more instructions.
    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: Please report any problems at http://mariadb.org/jira
    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: The latest information about MariaDB is available at http://mariadb.org/.
    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: You can find additional information about the MySQL part at:
    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: http://dev.mysql.com
    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: Consider joining MariaDB's strong and vibrant community:
    Oct 13 21:05:24 zabbix_server mariadb-prepare-db-dir[1497]: https://mariadb.org/get-involved/
    Oct 13 21:05:24 zabbix_server mysqld_safe[1583]: 191013 21:05:24 mysqld_safe Logging to '/var/log/mariadb/mariadb.log'.
    Oct 13 21:05:24 zabbix_server mysqld_safe[1583]: 191013 21:05:24 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql
    Oct 13 21:05:26 zabbix_server systemd[1]: Started MariaDB database server.


// 初始化 mysql 数据库的安全设置
[root@zabbix_server ~]# mysql_secure_installation

      Enter current password for root (enter for none):  <====直接按 enter 键回车

      Set root password? [Y/n] y   <======键入 y
      New password:   <======键入新的root密码, 本示例只用 'redhat'
      Re-enter new password: <======重新键入新root密码
      Password updated successfully!
      Reloading privilege tables..
       ... Success!


[root@zabbix_server ~]# mysql -uroot -p
Enter password:

// 注: zabbix 必须使用 字符集 utf8 和 比较规则 utf8_bin
MariaDB [(none)]> create database zabbix character set utf8 collate utf8_bin;
MariaDB [(none)]> grant all privileges on zabbix.* to zabbix@localhost identified by 'redhat';
MariaDB [(none)]> quit






----------------------------------------------------------------------------------------------------
编译安装 zabbix-server 程序

[root@zabbix_server ~]# cd download/
[root@zabbix_server download]# tar -xvf zabbix-4.4.0.tar.gz
[root@zabbix_server download]# cd zabbix-4.4.0/

// 观察一下 zabbix 源码目录下 的  data.sql images.sql schema.sql 文件
// 注:  对于 proxy, 其仅需导入 schema.sql, 而无需 images.sql 和 data.sql
[root@zabbix_server zabbix-4.4.0]# ls -1 database/mysql/
    data.sql      <------
    images.sql    <------
    Makefile.am
    Makefile.in
    schema.sql    <------



// 安装 zabbix 的 server 需要的依赖
[root@zabbix_server zabbix-4.4.0]# yum -y install mariadb-devel libxml2-devel net-snmp-devel libevent-devel libcurl-devel pcre-devel openssl-devel


// 查看一下 configure 可用选项
[root@zabbix_server zabbix-4.4.0]# ./configure --help
[root@zabbix_server zabbix-4.4.0]# ./configure --enable-server --enable-agent --with-mysql --enable-ipv6 --with-net-snmp --with-libcurl --with-libxml2 --with-openssl


    注:
        对于监视 virtual machine monitoring 而言 --with-libcurl and --with-libxml2 是 必须的
        对于 SMTP 认证 和 web.page.* Zabbix agent items 而言 --with-libcurl 也是必须的

        Since version 3.4.0, Zabbix will always compile with the PCRE library; installing it is not optional.

        更多关于 加密支持信息, 见 https://www.zabbix.com/documentation/4.4/manual/encryption#compiling_zabbix_with_encryption_support

        此处指定选项 --enable-agent 是为了同时编译安装 命令行工具 zabbix_get 和 zabbix_sender


[root@zabbix_server zabbix-4.4.0]# make
[root@zabbix_server zabbix-4.4.0]# make install

[root@zabbix_server ~]# which zabbix_server
    /usr/local/sbin/zabbix_server

[root@zabbix_server ~]# zabbix_server -V


// 导入数据到数据库 (针对 server)
[root@zabbix_server ~]# mysql -u root -p

    MariaDB [(none)]> use zabbix
    MariaDB [zabbix]> source  /root/download/zabbix-4.4.0/database/mysql/schema.sql
    MariaDB [zabbix]> source /root/download/zabbix-4.4.0/database/mysql/images.sql
    MariaDB [zabbix]> source /root/download/zabbix-4.4.0/database/mysql/data.sql
    MariaDB [zabbix]> quit


// 修改  zabbix_server.conf 配置文件
[root@zabbix_server ~]# vim /usr/local/etc/zabbix_server.conf
[root@zabbix_server ~]# grep -E -v '^#|^[[:space:]]*$' /usr/local/etc/zabbix_server.conf    # 查看修改后的结果
    LogFile=/tmp/zabbix_server.log
    DBHost=localhost
    DBName=zabbix
    DBUser=zabbix
    DBPassword=redhat
    DBPort=3306
    Timeout=4
    LogSlowQueries=3000
    StatsAllowedIP=127.0.0.1


// 其中 zabbix_server 服务进程
[root@zabbix_server ~]# zabbix_server



// 安装 Zabbix web interface
[root@zabbix_server ~]# yum install -y httpd php gd php-gd php-mysql

[root@zabbix_server ~]# systemctl start httpd.service
[root@zabbix_server ~]# systemctl enable httpd.service
    Created symlink from /etc/systemd/system/multi-user.target.wants/httpd.service to /usr/lib/systemd/system/httpd.service.


// 创建 php 解析的测试页面
[root@zabbix_server ~]# vim /var/www/html/a.php

    <?php
      phpinfo();
    ?>

// 创建 php 连接 mysql 的测试页面
[root@zabbix_server ~]# vim /var/www/html/b.php

    <?php
    // 参考: https://www.runoob.com/php/php-mysql-connect.html
    $servername = "localhost";
    $username = "zabbix";
    $password = "redhat";

    // 创建连接
    $conn = new mysqli($servername, $username, $password);

    // 检测连接
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }
    echo "连接成功";
    ?>

浏览器访问页面:
    http://192.168.175.100/a.php       (php 是否能正常解析)
    http://192.168.175.100/b.php       (php 是否能正常连接mysql数据库)


[root@zabbix_server ~]# mkdir /var/www/html/zabbix

[root@zabbix_server ~]# ls /root/download/zabbix-4.4.0/frontends/
    php

[root@zabbix_server ~]# cp -a /root/download/zabbix-4.4.0/frontends/php/*  /var/www/html/zabbix/

浏览器访问  http://192.168.175.100/zabbix
则会被重定向到页面  http://192.168.175.100/zabbix/setup.php


点击页面 http://192.168.175.100/zabbix/setup.php 上的按钮 [Next Step],
发现有一些参数和模块没满足要求, 则需要解决
[root@zabbix_server ~]# yum -y install php-bcmath php-mbstring php-xml

[root@zabbix_server ~]# vim /etc/php.ini

    post_max_size = 16M
    max_execution_time = 300
    max_input_time = 300
    date.timezone = Asia/Shanghai


[root@zabbix_server ~]# systemctl reload httpd







[root@zabbix_server ~]# vim ./download/zabbix-4.4.0/misc/init.d/fedora/core5/zabbix_server



/usr/local/etc/zabbix_server.conf
/usr/local/etc/zabbix_proxy.conf
/usr/local/etc/zabbix_agentd.conf
















