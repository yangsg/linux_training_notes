http://nginx.org/en/docs/control.html

//-------------------------这段的操作只是为了观察用，不是必须的，所以可以skip略过-------------------
// 编译一个测试的脚本，检查旧版的nginx是否在升级过程中一直在线可用
// 如果使用了inspect_webserver_status.sh来观察nginx升级过程，
// 记得升级完后关闭这里启动的相应的观察进程
[root@nginx7server ~]# vim inspect_webserver_status.sh
    #!/usr/bin/bash

    while true; do
      http_code=$(curl -I 192.168.175.10 2> /dev/null | awk '/^HTTP/{print $2}')
      if [ $http_code -eq 200 ]; then
        echo nginx_success >> /tmp/inspect_webserver_status.sh.log
      else
        echo nginx_fail >> /tmp/inspect_webserver_status.sh.log
      fi
      sleep 1
    done

[root@nginx7server ~]# bash inspect_webserver_status.sh
[root@nginx7server ~]# tail -f /tmp/inspect_webserver_status.sh.log
//-----------------------------------------------------------------------------------------------------


// 准备旧版的nginx环境用于后面升级替换

// 开始实际的升级操作--------------------------------------------------

// 下载新版nginx的tarball源码包
[root@nginx7server ~]# cd download/
[root@nginx7server download]# wget http://nginx.org/download/nginx-1.14.2.tar.gz
[root@nginx7server download]# tar -xvf nginx-1.14.2.tar.gz
[root@nginx7server download]# cd nginx-1.14.2/

// 查看找出旧版nginx安装时configure配置选项信息
[root@nginx7server ~]# /app/nginx/sbin/nginx -V
nginx version: nginx/1.12.2
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC) 
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/app/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre --with-file-aio --with-http_secure_link_module --with-threads --http-client-body-temp-path=/var/tmp/nginx/client --http-proxy-temp-path=/var/tmp/nginx/proxy --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi


// 利用与旧版nginx安装时configure相同的选项参数对新版的nginx进行相同的configure操作:
[root@nginx7server nginx-1.14.2]# ./configure --prefix=/app/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre --with-file-aio --with-http_secure_link_module --with-threads --http-client-body-temp-path=/var/tmp/nginx/client --http-proxy-temp-path=/var/tmp/nginx/proxy --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi


[root@nginx7server nginx-1.14.2]# make  #注：make后千万别执行make install操作,应以后续特殊的操作来取代

[root@nginx7server nginx-1.14.2]# file objs/nginx

// 备份旧版的 nginx 可执行程序文件
[root@nginx7server nginx-1.14.2]# mv /app/nginx/sbin/nginx  /app/nginx/sbin/nginx.oldbin
[root@nginx7server nginx-1.14.2]# /app/nginx/sbin/nginx.oldbin -v
    nginx version: nginx/1.12.2

[root@nginx7server nginx-1.14.2]# cp objs/nginx  /app/nginx/sbin/
[root@nginx7server nginx-1.14.2]# cd /app/nginx/sbin/
[root@nginx7server sbin]# ls
    nginx  nginx.oldbin

[root@nginx7server sbin]# ps aux | grep nginx
    root       4342  0.0  0.1  45956  1128 ?        Ss   11:02   0:00 nginx: master process /app/nginx/sbin/nginx
    nginx      4343  0.0  0.2  46420  2140 ?        S    11:02   0:00 nginx: worker process

// 以特殊方式启动新版的 nginx 进程，后续这些新的 nginx 进程将逐步接替old nginx进程的工作
[root@nginx7server sbin]# kill -USR2 $(cat /app/nginx/logs/nginx.pid)

[root@nginx7server sbin]# ps aux | grep nginx
    root       4342  0.0  0.1  45956  1316 ?        Ss   11:02   0:00 nginx: master process /app/nginx/sbin/nginx
    nginx      4343  0.0  0.2  46420  2140 ?        S    11:02   0:00 nginx: worker process
    root      42976  0.0  0.3  45968  3292 ?        S    12:17   0:00 nginx: master process /app/nginx/sbin/nginx
    nginx     42977  0.0  0.2  46436  2152 ?        S    12:17   0:00 nginx: worker process

[root@nginx7server sbin]# ls /app/nginx/logs/
    access.log  error.log  nginx.pid  nginx.pid.oldbin

[root@nginx7server sbin]# cat /app/nginx/logs/nginx.pid
    42976
[root@nginx7server sbin]# cat /app/nginx/logs/nginx.pid.oldbin
    4342

// 平缓终止 old nginx的工作进程(worker process), 让其平静的退出历史舞台
[root@nginx7server sbin]# kill -WINCH $(cat /app/nginx/logs/nginx.pid.oldbin)

[root@nginx7server sbin]# ps aux | grep nginx
    root       4342  0.0  0.1  45956  1316 ?        Ss   11:02   0:00 nginx: master process /app/nginx/sbin/nginx
    root      42976  0.0  0.3  45968  3292 ?        S    12:17   0:00 nginx: master process /app/nginx/sbin/nginx
    nginx     42977  0.0  0.2  46436  2152 ?        S    12:17   0:00 nginx: worker process


// 终止 old nginx 的主进程(master process), 向其最后告别
[root@nginx7server sbin]# kill  $(cat /app/nginx/logs/nginx.pid.oldbin)

[root@nginx7server sbin]# ps aux | grep nginx
    root      42976  0.0  0.3  45968  3292 ?        S    12:17   0:00 nginx: master process /app/nginx/sbin/nginx
    nginx     42977  0.0  0.2  46436  2152 ?        S    12:17   0:00 nginx: worker process


// 确认新版 nginx 信息
[root@nginx7server sbin]# /app/nginx/sbin/nginx -v
    nginx version: nginx/1.14.2

[root@nginx7server sbin]# /app/nginx/sbin/nginx -V
    nginx version: nginx/1.14.2
    built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
    built with OpenSSL 1.0.2k-fips  26 Jan 2017
    TLS SNI support enabled
    configure arguments: --prefix=/app/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre --with-file-aio --with-http_secure_link_module --with-threads --http-client-body-temp-path=/var/tmp/nginx/client --http-proxy-temp-path=/var/tmp/nginx/proxy --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi

// 至此，升级完毕---------------------------------------------

// 可以观察一下升级过程中nginx的服务是否有无法访问的异常情况发生
[root@nginx7server ~]# grep fail /tmp/inspect_webserver_status.sh.log

// 如果使用了inspect_webserver_status.sh来观察升级过程，记得升级完后关闭相应的观察进程









