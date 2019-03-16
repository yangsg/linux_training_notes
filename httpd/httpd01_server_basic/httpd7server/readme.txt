


[root@httpd7server ~]# yum -y install httpd
[root@httpd7server ~]# rpm -q httpd
    httpd-2.4.6-88.el7.centos.x86_64

[root@httpd7server ~]# vim /etc/httpd/conf/httpd.conf

        # 启用memory-mapping内存映射功能,可将部分内核与httpd进程的虚拟的内存地址空间映射到同一块相同的物理内存区域，
        # 减少数据在内核空间与用户空间的拷贝过程，从而提升httpd的性能。
        # https://httpd.apache.org/docs/2.4/en/mod/core.html#enablemmap
        EnableMMAP on
        # 启用内核的sendfile功能，使某些无需httpd进程访问的文件(如static file)可由内核直接发送给客户端，
        # 该功能避免了分离的read和send操作，以及buffer的分配,从而提升httpd的性能。
        # https://httpd.apache.org/docs/2.4/en/mod/core.html#enablesendfile
        EnableSendfile on



虚拟主机
参考：https://www.2daygeek.com/setup-apache-virtual-hosts-on-centos-rhel-fedora/

// 为虚拟主机的配置创建单独的目录
[root@httpd7server ~]# mkdir /etc/httpd/sites-available
[root@httpd7server ~]# mkdir /etc/httpd/sites-enabled

// 创建虚拟主机的配置文件
[root@httpd7server ~]# touch /etc/httpd/sites-available/name01.based.com.conf
[root@httpd7server ~]# touch /etc/httpd/sites-available/name02.based.com.conf
[root@httpd7server ~]# touch /etc/httpd/sites-available/ip01.based.com.conf
[root@httpd7server ~]# touch /etc/httpd/sites-available/ip02.based.com.conf

[root@httpd7server ~]# vim /etc/httpd/conf/httpd.conf
      IncludeOptional sites-enabled/*.conf


[root@httpd7server ~]# vim /etc/httpd/sites-available/name01.based.com.conf

[root@httpd7server ~]# tree /etc/httpd/sites-available
/etc/httpd/sites-available
├── ip01.based.com
├── ip02.based.com
├── name01.based.com
└── name02.based.com



// 创建虚拟主机内容目录
[root@httpd7server ~]# mkdir /var/www/ip01.based.com
[root@httpd7server ~]# mkdir /var/www/ip02.based.com
[root@httpd7server ~]# mkdir /var/www/name02.based.com
[root@httpd7server ~]# mkdir /var/www/name01.based.com

// 为虚拟主机创建首页
[root@httpd7server ~]# echo 'ip01.based.com'    >    /var/www/ip01.based.com/index.html
[root@httpd7server ~]# echo 'ip02.based.com'    >    /var/www/ip02.based.com/index.html
[root@httpd7server ~]# echo 'name02.based.com'  >    /var/www/name02.based.com/index.html
[root@httpd7server ~]# echo 'name01.based.com'  >    /var/www/name01.based.com/index.html

// 发布虚拟主机
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/ip01.based.com.conf    /etc/httpd/sites-enabled/ip01.based.com.conf
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/ip02.based.com.conf    /etc/httpd/sites-enabled/ip02.based.com.conf
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/name02.based.com.conf  /etc/httpd/sites-enabled/name02.based.com.conf
[root@httpd7server ~]# ln -s /etc/httpd/sites-available/name01.based.com.conf  /etc/httpd/sites-enabled/name01.based.com.conf

[root@httpd7server ~]# systemctl restart httpd

// 调试虚拟主机配置
[root@httpd7server ~]# httpd -S   # 同 apachectl -S
[root@httpd7server ~]# httpd -t   # 配置文件语法检查
[root@httpd7server ~]# httpd -t -D DUMP_VHOSTS   # 显示虚拟主机
[root@httpd7server ~]# httpd -t -D DUMP_MODULES  # 显示加载的module
[root@httpd7server ~]# httpd -t -D DUMP_VHOSTS -D DUMP_MODULES




