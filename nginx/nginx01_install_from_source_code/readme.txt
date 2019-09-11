
nginx官网资料
    http://nginx.org/
    http://nginx.org/en/docs/

其他参考:
    https://www.vultr.com/docs/how-to-compile-nginx-from-source-on-centos-7
    https://www.howtoforge.com/how-to-build-nginx-from-source-on-centos-7/
    https://sharadchhetri.com/2014/07/29/install-nginx-source-centos-7/


// 操作系统环境
[root@nginx7server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@nginx7server ~]# uname -r
    3.10.0-693.el7.x86_64
ip地址：192.168.175.10/24



// 构建基本的编译环境
[root@nginx7server ~]# yum -y install gcc gcc-c++ autoconf automake

// 安装相关依赖
[root@nginx7server ~]# yum install -y pcre-devel zlib-devel openssl-devel

// 创建独立的安装目录
[root@nginx7server ~]# mkdir /app

// 创建用户
[root@nginx7server ~]# useradd -M -s /sbin/nologin nginx


// 创建下载目录
[root@nginx7server ~]# mkdir download
[root@nginx7server ~]# cd download/

// 下载nginx源码tarball包
[root@nginx7server download]# wget http://nginx.org/download/nginx-1.14.2.tar.gz

[root@nginx7server download]# tar -xvf nginx-1.14.2.tar.gz
[root@nginx7server download]# cd nginx-1.14.2/

// 创建nginx用到的一些临时目录
[root@nginx7server nginx-1.14.2]# mkdir -p /var/tmp/nginx/{client,proxy,fastcgi,uwsgi,scgi}

[root@nginx7server nginx-1.14.2]# ./configure \
  --prefix=/app/nginx \
  --user=nginx \
  --group=nginx \
  --with-http_ssl_module \
  --with-http_flv_module \
  --with-http_stub_status_module \
  --with-http_gzip_static_module \
  --with-pcre \
  --with-file-aio \
  --with-http_secure_link_module \
  --with-threads \
  --http-client-body-temp-path=/var/tmp/nginx/client \
  --http-proxy-temp-path=/var/tmp/nginx/proxy \
  --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi \
  --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi \
  --http-scgi-temp-path=/var/tmp/nginx/scgi \

[root@nginx7server nginx-1.14.2]# make
[root@nginx7server nginx-1.14.2]# make install


[root@nginx7server ~]# tree /app/nginx/
        /app/nginx/
        ├── conf
        │   ├── fastcgi.conf
        │   ├── fastcgi.conf.default
        │   ├── fastcgi_params
        │   ├── fastcgi_params.default
        │   ├── koi-utf
        │   ├── koi-win
        │   ├── mime.types
        │   ├── mime.types.default
        │   ├── nginx.conf
        │   ├── nginx.conf.default
        │   ├── scgi_params
        │   ├── scgi_params.default
        │   ├── uwsgi_params
        │   ├── uwsgi_params.default
        │   └── win-utf
        ├── html
        │   ├── 50x.html
        │   └── index.html
        ├── logs
        └── sbin
            └── nginx


[root@nginx7server ~]# /app/nginx/sbin/nginx -h
      nginx version: nginx/1.14.2
      Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

      Options:
        -?,-h         : this help
        -v            : show version and exit
        -V            : show version and configure options then exit
        -t            : test configuration and exit
        -T            : test configuration, dump it and exit
        -q            : suppress non-error messages during configuration testing
        -s signal     : send signal to a master process: stop, quit, reopen, reload
        -p prefix     : set prefix path (default: /app/nginx/)
        -c filename   : set configuration file (default: conf/nginx.conf)
        -g directives : set global directives out of configuration file



// 启动nginx
[root@nginx7server ~]# /app/nginx/sbin/nginx

// 开机自启
[root@nginx7server ~]# vim /etc/rc.d/rc.local
    /app/nginx/sbin/nginx

[root@nginx7server ~]# chmod +x /etc/rc.d/rc.local


[root@nginx7server ~]# netstat -anptu | grep nginx
tcp        0      0 0.0.0.0:80              0.0.0.0:*               LISTEN      20180/nginx: master

[root@nginx7server ~]# ps -elf | grep nginx
1 S root      20180      1  0  80   0 - 11491 sigsus 19:28 ?        00:00:00 nginx: master process /app/nginx/sbin/nginx
5 S nginx     20181  20180  0  80   0 - 11607 ep_pol 19:28 ?        00:00:00 nginx: worker process
0 S root      20189   1302  0  80   0 - 28177 pipe_w 19:30 pts/1    00:00:00 grep --color=auto nginx




