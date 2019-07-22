

关于 cgi 和 fastcgi 见 笔记:   https://github.com/yangsg/linux_training_notes/tree/master/httpd

// apr apr-util相关的网址:
// http://apr.apache.org/
// http://apr.apache.org/download.cgi
// apr: Apache Portable Runtime library,一个免费的C语言库，包含一些数据结构和例程，形成一个在不同操作系统之间的可移植层。
// apr-util和apr类似，也是一个包含了数据结构和例程的C语言库，它为apr提供了额外的实用程序接口,
// 包含了对XML, LDAP, database interfaces, URI parsing等的支持


---------------------------------------------------------------------------------------------------

// 构建基础编译环境
[root@web_server ~]# yum -y install gcc gcc-c++ autoconf automake

[root@httpd7server ~]# mkdir download
[root@httpd7server ~]# cd download/

[root@web_server ~]# mkdir download
[root@web_server ~]# cd download/

//  下载 或 准备 软件包  httpd,  apr 和 apr-util 到 download 目录下
[root@web_server download]# tree
      .
      ├── apr-1.7.0.tar.gz
      ├── apr-util-1.6.1.tar.gz
      └── httpd-2.4.39.tar.gz

        httpd 下载页面: https://httpd.apache.org/download.cgi
        apr 和 apr-util 最新推荐版本的 下载页面: http://apr.apache.org/download.cgi
        apr 和 apr-util 就版本下载列表 页面: https://archive.apache.org/dist/apr/



// 新建独立的程序安装目录
[root@web_server ~]# mkdir /app


// 安装httpd其他依赖库
//  pcre: Perl-compatible regular expression library 兼容于perl正则表达式的库
[root@web_server ~]# yum -y install pcre-devel openssl-devel


// 安装apr-util的依赖库
[root@web_server ~]# yum -y install expat-devel   #如果不安装,make apr-util时会报错"fatal error: expat.h: No such file or directory"


// 解压并将apr和apr-util放置于httpd下的srclib目录
[root@web_server download]# tar -xvf httpd-2.4.39.tar.gz
[root@web_server download]# tar -xvf apr-1.7.0.tar.gz
[root@web_server download]# tar -xvf apr-util-1.6.1.tar.gz
[root@web_server download]# cp -r apr-1.7.0 httpd-2.4.39/srclib/apr
[root@web_server download]# cp -r apr-util-1.6.1 httpd-2.4.39/srclib/apr-util


[root@web_server download]# cd httpd-2.4.39/
[root@httpd7server httpd-2.4.38]# ./configure \
  --prefix=/app/httpd \
  --with-included-apr \
  --enable-so \
  --enable-rewrite \
  --enable-ssl \
  --enable-cgi \
  --enable-cgid \
  --enable-modules=most \
  --enable-mods-shared=most \
  --enable-mpm-shared=all \
  --with-mpm=event


[root@web_server httpd-2.4.39]# make
[root@web_server httpd-2.4.39]# make install

// 查看一些 编译 设置
[root@web_server ~]# /app/httpd/bin/httpd -V
        Server version: Apache/2.4.39 (Unix)
        Server built:   Jul 22 2019 16:31:17
        Server's Module Magic Number: 20120211:84
        Server loaded:  APR 1.7.0, APR-UTIL 1.6.1
        Compiled using: APR 1.7.0, APR-UTIL 1.6.1
        Architecture:   64-bit
        Server MPM:     event
          threaded:     yes (fixed thread count)
            forked:     yes (variable process count)
        Server compiled with....
         -D APR_HAS_SENDFILE
         -D APR_HAS_MMAP
         -D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)
         -D APR_USE_PROC_PTHREAD_SERIALIZE
         -D APR_USE_PTHREAD_SERIALIZE
         -D SINGLE_LISTEN_UNSERIALIZED_ACCEPT
         -D APR_HAS_OTHER_CHILD
         -D AP_HAVE_RELIABLE_PIPED_LOGS
         -D DYNAMIC_MODULE_LIMIT=256
         -D HTTPD_ROOT="/app/httpd"
         -D SUEXEC_BIN="/app/httpd/bin/suexec"
         -D DEFAULT_PIDLOG="logs/httpd.pid"
         -D DEFAULT_SCOREBOARD="logs/apache_runtime_status"
         -D DEFAULT_ERRORLOG="logs/error_log"
         -D AP_TYPES_CONFIG_FILE="conf/mime.types"
         -D SERVER_CONFIG_FILE="conf/httpd.conf"


// 查看 一些 目录结构
[root@web_server ~]# tree -L 1 /app/httpd/
          /app/httpd/
          ├── bin
          ├── build
          ├── cgi-bin
          ├── conf
          ├── error
          ├── htdocs
          ├── icons
          ├── include
          ├── lib
          ├── logs
          ├── man
          ├── manual
          └── modules


// 设置 PATH 环境变量
[root@web_server ~]# vim /etc/profile
      export PATH=/app/httpd/bin:$PATH

[root@web_server ~]# source /etc/profile


// 查看httpd命令的简要帮助
[root@web_server ~]# httpd -h
      Usage: httpd [-D name] [-d directory] [-f file]
                   [-C "directive"] [-c "directive"]
                   [-k start|restart|graceful|graceful-stop|stop]
                   [-v] [-V] [-h] [-l] [-L] [-t] [-T] [-S] [-X]
      Options:
        -D name            : define a name for use in <IfDefine name> directives
        -d directory       : specify an alternate initial ServerRoot
        -f file            : specify an alternate ServerConfigFile
        -C "directive"     : process directive before reading config files
        -c "directive"     : process directive after reading config files
        -e level           : show startup errors of level (see LogLevel)
        -E file            : log startup errors to file
        -v                 : show version number
        -V                 : show compile settings
        -h                 : list available command line options (this page)
        -l                 : list compiled in modules
        -L                 : list available configuration directives
        -t -D DUMP_VHOSTS  : show parsed vhost settings
        -t -D DUMP_RUN_CFG : show parsed run settings
        -S                 : a synonym for -t -D DUMP_VHOSTS -D DUMP_RUN_CFG
        -t -D DUMP_MODULES : show all loaded modules
        -M                 : a synonym for -t -D DUMP_MODULES
        -t -D DUMP_INCLUDES: show all included configuration files
        -t                 : run syntax check for config files
        -T                 : start without DocumentRoot(s) check
        -X                 : debug mode (only one worker, do not detach)

// 启用 httpd 服务
[root@web_server ~]# /app/httpd/bin/httpd -k start
AH00558: httpd: Could not reliably determine the server's fully qualified domain name, using fe80::20c:29ff:fe15:2d2e%ens33. Set the 'ServerName' directive globally to suppress this message
httpd (pid 34374) already running


[root@web_server ~]# netstat -anptu | grep httpd
    tcp6       0      0 :::80                   :::*                    LISTEN      34374/httpd

// 查看 httpd 的 pid 文件
[root@web_server ~]# find /app/httpd/  | grep pid
    /app/httpd/logs/httpd.pid

// 设置开机自启
[root@web_server ~]# vim /etc/rc.d/rc.local
        /app/httpd/bin/httpd -k start

[root@web_server ~]# chmod +x /etc/rc.d/rc.local

      ---------
      相关参考：
          https://my.oschina.net/yuanhaohao/blog/1933528
          http://httpd.apache.org/docs/2.4/install.html      //APR and APR-Util
          [root@httpd7server httpd-2.4.38]# less INSTALL
      ---------


---------------------------------------------------------------------------------------------------
安装通用二进制格式的 mysql
    参考  https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_01_install/mysql_install_from_generic_binary

// 下载 或 准备 通用二进制格式的 mysql 安装包


// 卸载系统自带的mariadb

[root@web_server ~]# rpm -qa | grep mariadb
      mariadb-libs-5.5.56-2.el7.x86_64
[root@web_server ~]# rpm -e --nodeps mariadb-libs


// 确认 或 安装 通用二进制格式的 mysql 需要的依赖
[root@web_server ~]# rpm -qa | grep -i libaio
    libaio-0.3.109-13.el7.x86_64   <---- 已经安装

// For MySQL 5.7.19 and later, 通用二进制的 mysql 会依赖 libnuma 库
[root@web_server ~]# yum search libnuma
[root@web_server ~]# yum -y install numactl-libs

[root@web_server ~]# rpm -q numactl-libs
    numactl-libs-2.0.9-7.el7.x86_64

[root@web_server ~]# useradd -M -s /sbin/nologin mysql
[root@web_server ~]# mkdir -p /mydata/data
[root@web_server ~]# chown -R mysql:mysql /mydata/data/


[root@web_server ~]# ls download/ | grep mysql
    mysql-5.7.27-linux-glibc2.12-x86_64.tar.gz

[root@web_server ~]# cd download/
[root@web_server download]# tar -xvf mysql-5.7.27-linux-glibc2.12-x86_64.tar.gz  -C /app/

[root@web_server download]# cd /app/
[root@web_server app]# ls
httpd  mysql-5.7.27-linux-glibc2.12-x86_64

[root@web_server app]# mv mysql-5.7.27-linux-glibc2.12-x86_64/ mysql
[root@web_server app]# ls
      httpd  mysql

[root@web_server app]# cd
[root@web_server ~]# chown -R root:mysql /app/mysql/


[root@web_server ~]# vim /etc/profile.d/mysql.sh
      export PATH=$PATH:/app/mysql/bin

[root@web_server ~]# source /etc/profile.d/mysql.sh


// 初始化数据库
// https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html
[root@web_server ~]# mysqld --initialize --user=mysql --basedir=/app/mysql/  --datadir=/mydata/data     #注意记录下该命令生成的临时密码
      2019-07-22T10:41:08.274512Z 1 [Note] A temporary password is generated for root@localhost: .8-G(;L<m.s:    #<<<<<<<记下临时密码

[root@web_server ~]# vim /etc/my.cnf
    [mysqld]
    basedir=/app/mysql
    datadir=/mydata/data
    port=3306
    server_id=20
    socket=/tmp/mysql.sock


// 启动mysqld服务
[root@web_server ~]# cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld
[root@web_server ~]# chmod a+x /etc/init.d/mysqld
[root@web_server ~]# chkconfig --add mysqld
[root@web_server ~]# chkconfig mysqld on
[root@web_server ~]# chkconfig --list mysqld


[root@web_server ~]# /etc/init.d/mysqld start
      Starting MySQL.Logging to '/mydata/data/web_server.err'.
       SUCCESS!


[root@web_server ~]# netstat -antp | grep :3306
      tcp6       0      0 :::3306                 :::*                    LISTEN      54091/mysqld


// 数据库初始化安全设置 https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html
[root@web_server ~]# mysql_secure_installation


[root@web_server ~]# mysql -h localhost -u root -p
mysql> pager less -Fi
mysql> show global variables like '%log%';




        ---------
        https://dev.mysql.com/doc/refman/5.7/en/binary-installation.html
        https://dev.mysql.com/doc/refman/5.7/en/replace-third-party-yum.html

        #其他一些小技巧：
        https://www.psce.com/en/blog/2012/06/02/how-to-find-mysql-binary-logs-error-logs-temporary-files/
          lsof -nc mysqld | grep -vE '(.so(..*)?$|.frm|.MY?|.ibd|ib_logfile|ibdata|TCP)'

        ---------


// 导出MySQL库文件 (该 操作时 正对 lamp 才有的)
[root@web_server ~]# ls -1 /app/mysql/lib/
      libmysqlclient.a
      libmysqlclient.so
      libmysqlclient.so.20
      libmysqlclient.so.20.3.14
      libmysqld.a
      libmysqld-debug.a
      libmysqlservices.a
      mecab
      pkgconfig
      plugin


[root@web_server ~]# vim /etc/ld.so.conf.d/mysql.conf
      /app/mysql/lib


[root@web_server ~]# ldconfig
[root@web_server ~]# ldconfig -v | grep mysql

// 导出head文件
[root@web_server ~]# ln -s /app/mysql/include/  /usr/include/mysql
[root@web_server ~]# ls  /usr/include/mysql





---------------------------------------------------------------------------------------------------
安装PHP


// 下载 或 准备 php 软件 的 源码安装包
[root@web_server download]# ls | grep php
      php-5.6.40.tar.gz

安装mcrypt,mhash加密认证组件
[root@web_server ~]# yum -y install libmcrypt libmcrypt-devel mcrypt mhash-devel mhash

[root@web_server ~]# yum install -y libxml2-devel bzip2-devel openssl-devel

[root@web_server ~]# cd /app/mysql/lib/
[root@web_server lib]# ln -s libmysqlclient.so.20.3.14 libmysqlclient_r.so


[root@web_server download]# tar -xvf php-5.6.40.tar.gz
[root@web_server download]# cd php-5.6.40/

[root@web_server php-5.6.40]# ./configure \
--prefix=/app/php \
--with-mysql=/app/mysql \
--with-mysqli=/app/mysql/bin/mysql_config \
--with-openssl \
--enable-mbstring \
--with-freetype-dir \
--with-jpeg-dir \
--with-png-dir \
--with-zlib \
--with-libxml-dir=/usr \
--enable-xml \
--enable-sockets \
--with-apxs2=/app/httpd/bin/apxs \
--with-mcrypt \
--with-config-file-path=/etc \
--with-config-file-scan-dir=/etc/php.d \
--with-bz2 \
--enable-maintainer-zts


          ------------------------- configure 成功的效果大概如下面的样子

          Generating files
          configure: creating ./config.status
          creating main/internal_functions.c
          creating main/internal_functions_cli.c
          +--------------------------------------------------------------------+
          | License:                                                           |
          | This software is subject to the PHP License, available in this     |
          | distribution in the file LICENSE.  By continuing this installation |
          | process, you are bound by the terms of this license agreement.     |
          | If you do not agree with the terms of this license, you must abort |
          | the installation process at this point.                            |
          +--------------------------------------------------------------------+

          Thank you for using PHP.

          config.status: creating php5.spec
          config.status: creating main/build-defs.h
          config.status: creating scripts/phpize
          config.status: creating scripts/man1/phpize.1
          config.status: creating scripts/php-config
          config.status: creating scripts/man1/php-config.1
          config.status: creating sapi/cli/php.1
          config.status: creating sapi/cgi/php-cgi.1
          config.status: creating ext/phar/phar.1
          config.status: creating ext/phar/phar.phar.1
          config.status: creating main/php_config.h
          config.status: executing default commands

          -------------------------


[root@web_server php-5.6.40]# make
[root@web_server php-5.6.40]# make install

// 复制PHP配置文件
[root@web_server php-5.6.40]# cp php.ini-production /etc/php.ini


// 编辑httpd配置文件，整合httpd和PHP
[root@web_server ~]# vim /app/httpd/conf/httpd.conf

    AddType application/x-httpd-php .php
    AddType application/x-httpd-php-source .phps

    DirectoryIndex index.php index.html

[root@web_server ~]# httpd -t

[root@web_server ~]# httpd -k restart





---------------------------------------------------------------------------------------------------
测试lamp平台工作是否正常

1、测试HTTPD/PHP

1) 测试httpd, php是否正常工作

[root@web_server ~]# vim /app/httpd/htdocs/a.php
[root@web_server ~]# cat /app/httpd/htdocs/a.php
    <?php
        phpinfo()
    ?>

浏览器访问:
      http://192.168.175.100/a.php

2) 测试PHP、MySQL
[root@web_server ~]# cat /app/httpd/htdocs/b.php
      <?php
      // 参考  https://www.runoob.com/php/php-mysql-connect.html

      $servername = "localhost";
      $username = "root";
      $password = "WWW.1.com";

      // 创建连接
      $conn = new mysqli($servername, $username, $password);

      // 检测连接
      if ($conn->connect_error) {
          die("连接失败: " . $conn->connect_error);
      }
      echo "连接成功";
      ?>

浏览器访问:
      http://192.168.175.100/b.php


TODO: 部署应用

---------------------------------------------------------------------------------------------------





---------------------------------------------------------------------------------------------------
网上资料:

httpd 官网:
    https://httpd.apache.org/

httpd 下载页面:
    https://httpd.apache.org/download.cgi


apr 和 apr-util 官网:
    http://apr.apache.org/

apr 和 apr-util 最新推荐版本的 下载页面:
    http://apr.apache.org/download.cgi

apr 和 apr-util 就版本下载列表 页面:
    https://archive.apache.org/dist/apr/





