


// apr apr-util相关的网址:
// http://apr.apache.org/
// http://apr.apache.org/download.cgi
// apr: Apache Portable Runtime library,一个免费的C语言库，包含一些数据结构和例程，形成一个在不同操作系统之间的可移植层。
// apr-util和apr类似，也是一个包含了数据结构和例程的C语言库，它为apr提供了额外的实用程序接口,
// 包含了对XML, LDAP, database interfaces, URI parsing等的支持

// 构建基础编译环境
[root@httpd7server ~]# yum -y install gcc gcc-c++ autoconf automake

// 下载httpd的tarball源码包及其相关的依赖库
[root@httpd7server ~]# mkdir download
[root@httpd7server ~]# cd download/
[root@httpd7server download]# wget http://mirrors.shu.edu.cn/apache/httpd/httpd-2.4.38.tar.gz
[root@httpd7server download]# wget http://mirrors.shu.edu.cn/apache/apr/apr-1.6.5.tar.gz
[root@httpd7server download]# wget http://mirrors.shu.edu.cn/apache/apr/apr-util-1.6.1.tar.gz


// 新建独立的程序安装目录
[root@httpd7server ~]# mkdir /app

// 安装httpd其他依赖库
//  pcre: Perl-compatible regular expression library 兼容于perl正则表达式的库
[root@httpd7server ~]# yum -y install pcre-devel openssl-devel

// 安装apr-util的依赖库
[root@httpd7server ~]# yum -y install expat-devel   #如果不安装,make apr-util时会报错"fatal error: expat.h: No such file or directory"



// 解压并将apr和apr-util放置于httpd下的srclib目录
[root@httpd7server download]# tar -xvf httpd-2.4.38.tar.gz
[root@httpd7server download]# tar -xvf apr-1.6.5.tar.gz
[root@httpd7server download]# tar -xvf apr-util-1.6.1.tar.gz
[root@httpd7server download]# cp -r apr-1.6.5 httpd-2.4.38/srclib/apr
[root@httpd7server download]# cp -r apr-util-1.6.1 httpd-2.4.38/srclib/apr-util

[root@httpd7server download]# cd httpd-2.4.38/
[root@httpd7server httpd-2.4.38]# ./configure \
  --prefix=/app/httpd \
  --with-included-apr \
  --enable-so \
  --enable-rewrite \
  --enable-ssl \
  --enable-cgi --enable-cgid \
  --enable-modules=most \
  --enable-mods-shared=most \
  --enable-mpm-shared=all \
  --with-mpm=event


[root@httpd7server httpd-2.4.38]# make
[root@httpd7server httpd-2.4.38]# make install
[root@httpd7server ~]# /app/httpd/bin/httpd -V
          Server version: Apache/2.4.38 (Unix)
          Server built:   Mar 18 2019 15:36:40
          Server's Module Magic Number: 20120211:83
          Server loaded:  APR 1.6.5, APR-UTIL 1.6.1
          Compiled using: APR 1.6.5, APR-UTIL 1.6.1
          Architecture:   64-bit
          Server MPM:     event
            threaded:     yes (fixed thread count)
              forked:     yes (variable process count)
          Server compiled with....
           -D APR_HAS_SENDFILE
           -D APR_HAS_MMAP
           -D APR_HAVE_IPV6 (IPv4-mapped addresses enabled)
           -D APR_USE_SYSVSEM_SERIALIZE
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


[root@httpd7server httpd-2.4.38]# tree -L 1 /app/httpd/
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


[root@httpd7server ~]# vim /etc/profile
      export PATH=/app/httpd/bin:$PATH

[root@httpd7server ~]# source /etc/profile

// 查看httpd命令的简要帮助
[root@httpd7server ~]# /app/httpd/bin/httpd -h
      Usage: /app/httpd/bin/httpd [-D name] [-d directory] [-f file]
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


[root@httpd7server ~]# /app/httpd/bin/httpd -k start

[root@httpd7server ~]# netstat -anptu  | grep httpd

// 设置开机自启
[root@httpd7server ~]# vim /etc/rc.d/rc.local
      /app/httpd/bin/httpd -k start

[root@httpd7server ~]# chmod +x /etc/rc.d/rc.local




相关参考：
    https://my.oschina.net/yuanhaohao/blog/1933528
    http://httpd.apache.org/docs/2.4/install.html      //APR and APR-Util
    [root@httpd7server httpd-2.4.38]# less INSTALL

---------------------------------------------------------------------






















