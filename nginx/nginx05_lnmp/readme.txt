Difference between PHP-CGI and PHP-FPM
  https://www.basezap.com/difference-php-cgi-php-fpm/
Differences and dis/advanages between: Fast-CGI, CGI, Mod-PHP, SuPHP, PHP-FPM
  https://serverfault.com/questions/645755/differences-and-dis-advanages-between-fast-cgi-cgi-mod-php-suphp-php-fpm




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



#// -------------------------------------------------------------







