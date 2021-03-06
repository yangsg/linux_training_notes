Difference between PHP-CGI and PHP-FPM
  https://www.basezap.com/difference-php-cgi-php-fpm/
Differences and dis/advanages between: Fast-CGI, CGI, Mod-PHP, SuPHP, PHP-FPM
  https://serverfault.com/questions/645755/differences-and-dis-advanages-between-fast-cgi-cgi-mod-php-suphp-php-fpm

      https://github.com/yangsg/linux_training_notes/tree/master/httpd


#// 安装php-fpm server --------------------------------------------
[root@phpfpm7server ~]# yum -y install gcc gcc-c++ autoconf automake

[root@phpfpm7server ~]# yum install -y  libmcrypt libmcrypt-devel mcrypt mhash-devel mhash
[root@phpfpm7server ~]# yum install -y libxml2-devel bzip2-devel openssl-devel

[root@phpfpm7server ~]# mkdir download
[root@phpfpm7server ~]# cd download/
[root@phpfpm7server download]# wget http://120.52.51.15/cn2.php.net/distributions/php-5.6.40.tar.gz  #// https://www.php.net/releases/  #// https://www.php.net/git.php
[root@phpfpm7server download]# tar -xvf php-5.6.40.tar.gz
[root@phpfpm7server download]# cd php-5.6.40/
[root@phpfpm7server php-5.6.40]# ./configure --help


[root@phpfpm7server php-5.6.40]# ./configure --prefix=/app/php  \
--with-mysql  \
--with-mysqli  \
--with-openssl  \
--enable-mbstring  \
--with-freetype-dir  \
--with-jpeg-dir  \
--with-png-dir  \
--with-zlib  \
--with-libxml-dir=/app  \
--enable-xml  \
--enable-sockets  \
--enable-fpm  \
--with-mcrypt  \
--with-bz2  \
--with-config-file-path=/etc  \
--with-config-file-scan-dir=/etc/php.d  \


[root@phpfpm7server php-5.6.40]# make
[root@phpfpm7server php-5.6.40]# make install

// 查看一下 目录 /app/php/
[root@phpfpm7server php-5.6.40]# tree -L 1 /app/php/
      /app/php/
      ├── bin
      ├── etc
      ├── include
      ├── lib
      ├── php
      ├── sbin
      └── var


// 查看 php 的 help 信息
[root@phpfpm7server php-5.6.40]# /app/php/bin/php -h

// 查看 php 的 version 信息
[root@phpfpm7server php-5.6.40]# /app/php/bin/php -v

      PHP 5.6.40 (cli) (built: Jul 23 2019 14:29:38)
      Copyright (c) 1997-2016 The PHP Group
      Zend Engine v2.6.0, Copyright (c) 1998-2016 Zend Technologies



#// 复制php加载模块的配置文件
[root@phpfpm7server php-5.6.40]# cp php.ini-production  /etc/php.ini

#// 复制php-fpm的配置文件
[root@phpfpm7server php-5.6.40]# cp /app/php/etc/php-fpm.conf.default /app/php/etc/php-fpm.conf

[root@phpfpm7server php-5.6.40]# cp sapi/fpm/init.d.php-fpm /etc/init.d/php-fpm

[root@phpfpm7server php-5.6.40]# chmod a+x /etc/init.d/php-fpm
[root@phpfpm7server php-5.6.40]# chkconfig --add php-fpm
[root@phpfpm7server php-5.6.40]# chkconfig php-fpm on
[root@phpfpm7server php-5.6.40]# /etc/init.d/php-fpm --help
    Usage: /etc/init.d/php-fpm {start|stop|force-quit|restart|reload|status}

[root@phpfpm7server php-5.6.40]# vim /app/php/etc/php-fpm.conf
  pid = /app/php/var/run/php-fpm.pid
  listen = 192.168.175.101:9000  ;listen可支持的写法参考配置文件自带示例
  user = nginx
  group = nginx

  pm.max_children = 150
  pm.start_servers = 10
  pm.min_spare_servers = 10
  pm.max_spare_servers = 10
  ; 参数 pm.max_requests 对于避免 一些 第3方库 因 内存泄露 导致 内存溢出 很有用.
  ; 关于 内存泄露(memory leak) 和 内存溢出(out of memory) 的区别 和 联系 可参考 网上博文::
  ;     https://www.cnblogs.com/panxuejun/p/5883044.html
  pm.max_requests = 500

[root@phpfpm7server php-5.6.40]# useradd -s /sbin/nologin nginx
[root@phpfpm7server php-5.6.40]# /etc/init.d/php-fpm start
    Starting php-fpm  done

[root@phpfpm7server php-5.6.40]# netstat -anptu | grep php
    tcp        0      0 192.168.175.101:9000    0.0.0.0:*               LISTEN      124283/php-fpm: mas

[root@phpfpm7server php-5.6.40]# ps -elf | grep php
    1 S root     124283      1  0  80   0 - 45064 ep_pol 13:30 ?        00:00:00 php-fpm: master process (/app/php/etc/php-fpm.conf)
    5 S nginx    124284 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124285 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124286 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124287 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124288 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124289 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124290 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124291 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124292 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www
    5 S nginx    124293 124283  0  80   0 - 45064 inet_c 13:30 ?        00:00:00 php-fpm: pool www




---------------------------------------------------------------------------------------------------
安装 开源的 php 优化插件 xcache

    参考笔记:
        https://github.com/yangsg/linux_training_notes/blob/master/nginx/nginx05_lnmp/concept_and_details.txt

  xcache 用于在 共享内存中 缓存 编译后的 .php 的 操作码(opcode), 从而避免了 重复的 解析编译 及 磁盘IO 访问的开销.

// 因 xcache 项目移到了 github, 所以现在只能从 github 上下载
[root@phpfpm7server download]# wget -O xcache-3.2.0.tar.gz  https://github.com/lighttpd/xcache/archive/3.2.0.tar.gz
[root@phpfpm7server download]# ls | grep xcache
      xcache-3.2.0.tar.gz

[root@phpfpm7server download]# tar -xvf xcache-3.2.0.tar.gz
[root@phpfpm7server download]# ls | grep xcache
        xcache-3.2.0
        xcache-3.2.0.tar.gz

[root@phpfpm7server download]# cd xcache-3.2.0/

// phpize 命令是用来准备 PHP 扩展库的编译环境的, 如生成 configure 命令等
[root@phpfpm7server xcache-3.2.0]# /app/php/bin/phpize --clean
[root@phpfpm7server xcache-3.2.0]# /app/php/bin/phpize
      Configuring for:
      PHP Api Version:         20131106
      Zend Module Api No:      20131226
      Zend Extension Api No:   220131226

[root@phpfpm7server xcache-3.2.0]# ./configure --help
[root@phpfpm7server xcache-3.2.0]# ./configure --enable-xcache --with-php-config=/app/php/bin/php-config
[root@phpfpm7server xcache-3.2.0]# make

[root@phpfpm7server xcache-3.2.0]# make install
        Installing shared extensions:     /app/php/lib/php/extensions/no-debug-non-zts-20131226/

[root@phpfpm7server xcache-3.2.0]# ls /app/php/lib/php/extensions/no-debug-non-zts-20131226/
        opcache.a  opcache.so  xcache.so


[root@phpfpm7server xcache-3.2.0]# mkdir /etc/php.d


[root@phpfpm7server xcache-3.2.0]# vim /etc/php.d/xcache.ini
    [xcache-common]
    extension = xcache.so

// 重启, 使 配置生效
[root@phpfpm7server xcache-3.2.0]# /etc/init.d/php-fpm restart


// 查看 模块
[root@phpfpm7server xcache-3.2.0]# /app/php/bin/php -m | grep -i xcache
    XCache
    XCache Cacher
    XCache
    XCache Cacher


// 查看版本信息
[root@phpfpm7server xcache-3.2.0]# /app/php/bin/php -v

      PHP 5.6.40 (cli) (built: Jul 23 2019 14:29:38)
      Copyright (c) 1997-2016 The PHP Group
      Zend Engine v2.6.0, Copyright (c) 1998-2016 Zend Technologies
          with XCache v3.2.0, Copyright (c) 2005-2014, by mOo
          with XCache Cacher v3.2.0, Copyright (c) 2005-2014, by mOo

      -------------
      // 其他有用的命令
      // 查看 默认的 extension-dir
      [root@phpfpm7server xcache-3.2.0]# /app/php/bin/php-config | grep  'extension-dir'
        --extension-dir     [/app/php/lib/php/extensions/no-debug-non-zts-20131226]

---------------------------------------------------------------------------------------------------





















