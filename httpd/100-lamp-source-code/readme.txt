

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

// 卸载系统自带的mariadb

[root@web_server ~]# rpm -qa | grep mariadb
      mariadb-libs-5.5.56-2.el7.x86_64
[root@web_server ~]# rpm -e --nodeps mariadb-libs




https://dev.mysql.com/doc/refman/5.7/en/binary-installation.html
https://dev.mysql.com/doc/refman/5.7/en/replace-third-party-yum.html







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





