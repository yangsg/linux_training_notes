
// 显示帮助
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


// 检查配置文件语法
[root@nginx7server ~]# /app/nginx/sbin/nginx -t

// 检查版本
[root@nginx7server ~]# /app/nginx/sbin/nginx -v
    nginx version: nginx/1.14.2

// 显示版本及在安装执行./configure 时的配置选项
[root@nginx7server ~]# /app/nginx/sbin/nginx -V








