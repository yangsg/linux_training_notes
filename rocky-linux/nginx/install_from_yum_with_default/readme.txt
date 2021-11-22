[root@localhost ~]# yum -y install nginx

[root@localhost ~]# rpm -q nginx
nginx-1.14.1-9.module+el8.4.0+542+81547229.x86_64

[root@localhost ~]# nginx -V
nginx version: nginx/1.14.1
built by gcc 8.4.1 20200928 (Red Hat 8.4.1-1) (GCC)
built with OpenSSL 1.1.1g FIPS  21 Apr 2020
TLS SNI support enabled
configure arguments: --prefix=/usr/share/nginx --sbin-path=/usr/sbin/nginx --modules-path=/usr/lib64/nginx/modules --conf-path=/etc/nginx/nginx.conf --error-log-path=/var/log/nginx/error.log --http-log-path=/var/log/nginx/access.log --http-client-body-temp-path=/var/lib/nginx/tmp/client_body --http-proxy-temp-path=/var/lib/nginx/tmp/proxy --http-fastcgi-temp-path=/var/lib/nginx/tmp/fastcgi --http-uwsgi-temp-path=/var/lib/nginx/tmp/uwsgi --http-scgi-temp-path=/var/lib/nginx/tmp/scgi --pid-path=/run/nginx.pid --lock-path=/run/lock/subsys/nginx --user=nginx --group=nginx --with-file-aio --with-ipv6 --with-http_ssl_module --with-http_v2_module --with-http_realip_module --with-http_addition_module --with-http_xslt_module=dynamic --with-http_image_filter_module=dynamic --with-http_sub_module --with-http_dav_module --with-http_flv_module --with-http_mp4_module --with-http_gunzip_module --with-http_gzip_static_module --with-http_random_index_module --with-http_secure_link_module --with-http_degradation_module --with-http_slice_module --with-http_stub_status_module --with-http_perl_module=dynamic --with-http_auth_request_module --with-mail=dynamic --with-mail_ssl_module --with-pcre --with-pcre-jit --with-stream=dynamic --with-stream_ssl_module --with-debug --with-cc-opt='-O2 -g -pipe -Wall -Werror=format-security -Wp,-D_FORTIFY_SOURCE=2 -Wp,-D_GLIBCXX_ASSERTIONS -fexceptions -fstack-protector-strong -grecord-gcc-switches -specs=/usr/lib/rpm/redhat/redhat-hardened-cc1 -specs=/usr/lib/rpm/redhat/redhat-annobin-cc1 -m64 -mtune=generic -fasynchronous-unwind-tables -fstack-clash-protection -fcf-protection' --with-ld-opt='-Wl,-z,relro -Wl,-z,now -specs=/usr/lib/rpm/redhat/redhat-hardened-ld -Wl,-E'



[root@localhost ~]# tree /etc/nginx/
		/etc/nginx/
		├── conf.d
		├── default.d
		├── fastcgi.conf
		├── fastcgi.conf.default
		├── fastcgi_params
		├── fastcgi_params.default
		├── koi-utf
		├── koi-win
		├── mime.types
		├── mime.types.default
		├── nginx.conf
		├── nginx.conf.default
		├── scgi_params
		├── scgi_params.default
		├── uwsgi_params
		├── uwsgi_params.default
		└── win-utf



[root@localhost ~]# rpm -ql nginx
		/etc/logrotate.d/nginx
		/etc/nginx/fastcgi.conf
		/etc/nginx/fastcgi.conf.default
		/etc/nginx/fastcgi_params
		/etc/nginx/fastcgi_params.default
		/etc/nginx/koi-utf
		/etc/nginx/koi-win
		/etc/nginx/mime.types
		/etc/nginx/mime.types.default
		/etc/nginx/nginx.conf
		/etc/nginx/nginx.conf.default
		/etc/nginx/scgi_params
		/etc/nginx/scgi_params.default
		/etc/nginx/uwsgi_params
		/etc/nginx/uwsgi_params.default
		/etc/nginx/win-utf
		/usr/bin/nginx-upgrade
		/usr/lib/.build-id
		/usr/lib/.build-id/2d
		/usr/lib/.build-id/2d/a6da8eadeb05c036be9b4ea9ec6aecde0fcc35
		/usr/lib/systemd/system/nginx.service
		/usr/lib64/nginx/modules
		/usr/sbin/nginx
		/usr/share/doc/nginx
		/usr/share/doc/nginx/CHANGES
		/usr/share/doc/nginx/README
		/usr/share/doc/nginx/README.dynamic
		/usr/share/licenses/nginx
		/usr/share/licenses/nginx/LICENSE
		/usr/share/man/man3/nginx.3pm.gz
		/usr/share/man/man8/nginx-upgrade.8.gz
		/usr/share/man/man8/nginx.8.gz
		/usr/share/nginx/html/404.html
		/usr/share/nginx/html/50x.html
		/usr/share/nginx/html/index.html
		/usr/share/nginx/html/nginx-logo.png
		/usr/share/nginx/html/poweredby.png
		/usr/share/vim/vimfiles/ftdetect/nginx.vim
		/usr/share/vim/vimfiles/indent/nginx.vim
		/usr/share/vim/vimfiles/syntax/nginx.vim
		/var/lib/nginx
		/var/lib/nginx/tmp
		/var/log/nginx




[root@localhost ~]# cat /usr/lib/systemd/system/nginx.service
		[Unit]
		Description=The nginx HTTP and reverse proxy server
		After=network.target remote-fs.target nss-lookup.target

		[Service]
		Type=forking
		PIDFile=/run/nginx.pid
		# Nginx will fail to start if /run/nginx.pid already exists but has the wrong
		# SELinux context. This might happen when running `nginx -t` from the cmdline.
		# https://bugzilla.redhat.com/show_bug.cgi?id=1268621
		ExecStartPre=/usr/bin/rm -f /run/nginx.pid
		ExecStartPre=/usr/sbin/nginx -t
		ExecStart=/usr/sbin/nginx
		ExecReload=/bin/kill -s HUP $MAINPID
		KillSignal=SIGQUIT
		TimeoutStopSec=5
		KillMode=mixed
		PrivateTmp=true

		[Install]
		WantedBy=multi-user.target




[root@localhost ~]# systemctl start nginx
[root@localhost ~]# systemctl enable nginx
Created symlink /etc/systemd/system/multi-user.target.wants/nginx.service → /usr/lib/systemd/system/nginx.service.

[root@localhost ~]# ps -ef |grep nginx
root        1563       1  0 06:45 ?        00:00:00 nginx: master process /usr/sbin/nginx
nginx       1564    1563  0 06:45 ?        00:00:00 nginx: worker process
root        1586    1077  0 06:46 pts/1    00:00:00 grep --color=auto nginx

[root@localhost ~]# id nginx
uid=996(nginx) gid=993(nginx) groups=993(nginx)




[root@localhost ~]# yum -y install lsof
[root@localhost ~]# lsof -nc nginx | grep log
nginx   1563  root    2w      REG              253,0        0   873642 /var/log/nginx/error.log
nginx   1563  root    4w      REG              253,0        0   873642 /var/log/nginx/error.log
nginx   1563  root    7w      REG              253,0        0   873644 /var/log/nginx/access.log
nginx   1564 nginx    2w      REG              253,0        0   873642 /var/log/nginx/error.log
nginx   1564 nginx    4w      REG              253,0        0   873642 /var/log/nginx/error.log
nginx   1564 nginx    7w      REG              253,0        0   873644 /var/log/nginx/access.log

[root@localhost ~]# ss -pntl
State           Recv-Q          Send-Q                   Local Address:Port                     Peer Address:Port          Process
LISTEN          0               128                            0.0.0.0:80                            0.0.0.0:*              users:(("nginx",pid=1564,fd=8),("nginx",pid=1563,fd=8))
LISTEN          0               128                            0.0.0.0:22                            0.0.0.0:*              users:(("sshd",pid=844,fd=4))
LISTEN          0               128                               [::]:80                               [::]:*              users:(("nginx",pid=1564,fd=9),("nginx",pid=1563,fd=9))
LISTEN          0               128                               [::]:22                               [::]:*              users:(("sshd",pid=844,fd=6))



[root@localhost ~]# nginx -h
	nginx version: nginx/1.14.1
	Usage: nginx [-?hvVtTq] [-s signal] [-c filename] [-p prefix] [-g directives]

	Options:
		-?,-h         : this help
		-v            : show version and exit
		-V            : show version and configure options then exit
		-t            : test configuration and exit
		-T            : test configuration, dump it and exit
		-q            : suppress non-error messages during configuration testing
		-s signal     : send signal to a master process: stop, quit, reopen, reload
		-p prefix     : set prefix path (default: /usr/share/nginx/)
		-c filename   : set configuration file (default: /etc/nginx/nginx.conf)
		-g directives : set global directives out of configuration file



nginx 优化:
https://geekflare.com/nginx-production-configuration/
https://www.cnblogs.com/dazhidacheng/p/7772451.html
https://www.cnblogs.com/cheyunhua/p/10670070.html
https://blog.csdn.net/hanjinjuan/article/details/119744168
https://www.cnblogs.com/yuanzai12345/p/5951860.html


