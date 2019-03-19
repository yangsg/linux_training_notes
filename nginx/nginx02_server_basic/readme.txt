

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
      │   ├── access.log
      │   ├── error.log
      │   └── nginx.pid
      └── sbin
          └── nginx



[root@nginx7server ~]# mkdir /app/nginx/{sites-available,sites-enabled}

[root@nginx7server ~]# ln -s /app/nginx/sites-available/location.match.demo.com.conf /app/nginx/sites-enabled/location.match.demo.com.conf

[root@nginx7server ~]# /app/nginx/sbin/nginx -t
[root@nginx7server ~]# /app/nginx/sbin/nginx -s reload





