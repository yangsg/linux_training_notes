

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









