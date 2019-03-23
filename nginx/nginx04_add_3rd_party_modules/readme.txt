通过安装lua模块演示如何为nginx添加第3方模块

https://github.com/openresty/lua-nginx-module
https://blog.cloudflare.com/pushing-nginx-to-its-limit-with-lua/

luajit的安装参考资料 http://luajit.org/install.html

LuaJIT下载页
http://luajit.org/download.html

// 开始操作
// 下载LuaJIT
[root@nginx7server download]# wget http://luajit.org/download/LuaJIT-2.0.5.tar.gz
[root@nginx7server download]# tar -xvf LuaJIT-2.0.5.tar.gz
[root@nginx7server download]# cd LuaJIT-2.0.5/
[root@nginx7server LuaJIT-2.0.5]# make
[root@nginx7server LuaJIT-2.0.5]# make install PREFIX=/usr/local/luajit

// 导出LuaJIT的库文件
[root@nginx7server ~]# vim /etc/ld.so.conf.d/luajit.conf
    /usr/local/luajit/lib

[root@nginx7server ~]# ldconfig
[root@nginx7server ~]# ldconfig -p | grep -i lua
        libluajit-5.1.so.2 (libc6,x86-64) => /usr/local/luajit/lib/libluajit-5.1.so.2
        libluajit-5.1.so (libc6,x86-64) => /usr/local/luajit/lib/libluajit-5.1.so
        liblua-5.1.so (libc6,x86-64) => /lib64/liblua-5.1.so


// 配置luajit的环境变量
[root@nginx7server ~]# vim /etc/profile
    export LUAJIT_LIB=/usr/local/luajit/lib
    export LUAJIT_INC=/usr/local/luajit/include/luajit-2.0

[root@nginx7server ~]# source /etc/profile

// 测试lua解释器
[root@nginx7server ~]# vim hello.lua
    print("Hello World")

[root@nginx7server ~]# lua hello.lua
    Hello World

// 或以交互式的方式测试lua解释器
[root@nginx7server ~]# lua
Lua 5.1.4  Copyright (C) 1994-2008 Lua.org, PUC-Rio
> print("hello world")
hello world
>

// 安装nginx_lua三方模块
// 参考  https://github.com/openresty/lua-nginx-module#installation
[root@nginx7server ~]# cd download/
[root@nginx7server download]# wget https://github.com/simplresty/ngx_devel_kit/archive/v0.3.0.tar.gz
[root@nginx7server download]# wget https://github.com/openresty/lua-nginx-module/archive/v0.10.14.tar.gz
[root@nginx7server download]# tar -xvf v0.3.0.tar.gz       #ngx_devel_kit-0.3.0
[root@nginx7server download]# tar -xvf v0.10.14.tar.gz     #lua-nginx-module-0.10.14


// 查看已有nginx安装时的configure配置信息, 待会重新configure时会利用
[root@nginx7server ~]# /app/nginx/sbin/nginx -V
nginx version: nginx/1.14.2
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC) 
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/app/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre --with-file-aio --with-http_secure_link_module --with-threads --http-client-body-temp-path=/var/tmp/nginx/client --http-proxy-temp-path=/var/tmp/nginx/proxy --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi


[root@nginx7server ~]# cd download/nginx-1.14.2/
// 注意，如下./configure选项在原有的基础上加了两项：
//     --add-module=/root/download/ngx_devel_kit-0.3.0
//     --add-module=/root/download/lua-nginx-module-0.10.14
[root@nginx7server nginx-1.14.2]# ./configure  --prefix=/app/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre --with-file-aio --with-http_secure_link_module --with-threads --http-client-body-temp-path=/var/tmp/nginx/client --http-proxy-temp-path=/var/tmp/nginx/proxy --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi --add-module=/root/download/ngx_devel_kit-0.3.0 --add-module=/root/download/lua-nginx-module-0.10.14


[root@nginx7server nginx-1.14.2]# make

// 警告：
/  如下只是为了偷懒，直接安装覆盖既有的nginx,
// 实际生产环境中应该考虑是否需要在线升级
// 在线升级参考： https://github.com/yangsg/linux_training_notes/tree/master/nginx/nginx03_upgrade_executable_on_the_fly
[root@nginx7server nginx-1.14.2]# make install   #警告：实际生产环境中应该考虑在线升级，而不是直接覆盖

[root@nginx7server ~]# ls /app/nginx/sbin/
    nginx  nginx.old

[root@nginx7server ~]# /app/nginx/sbin/nginx -s stop

// 检查模块是否实际真的被添加进来,即看是否包含--add-module=/root/download/ngx_devel_kit-0.3.0 --add-module=/root/download/lua-nginx-module-0.10.14
[root@nginx7server ~]# /app/nginx/sbin/nginx -V
nginx version: nginx/1.14.2
built by gcc 4.8.5 20150623 (Red Hat 4.8.5-36) (GCC)
built with OpenSSL 1.0.2k-fips  26 Jan 2017
TLS SNI support enabled
configure arguments: --prefix=/app/nginx --user=nginx --group=nginx --with-http_ssl_module --with-http_flv_module --with-http_stub_status_module --with-http_gzip_static_module --with-pcre --with-file-aio --with-http_secure_link_module --with-threads --http-client-body-temp-path=/var/tmp/nginx/client --http-proxy-temp-path=/var/tmp/nginx/proxy --http-fastcgi-temp-path=/var/tmp/nginx/fastcgi --http-uwsgi-temp-path=/var/tmp/nginx/uwsgi --http-scgi-temp-path=/var/tmp/nginx/scgi --add-module=/root/download/ngx_devel_kit-0.3.0 --add-module=/root/download/lua-nginx-module-0.10.14







[root@nginx7server ~]# mkdir /app/nginx/{sites-available,sites-enabled}










