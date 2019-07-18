

半同步复制 Semisynchronous Replication

准备 实现 环境用的 3 台 主机:
master:  192.168.175.100
slave01: 192.168.175.101
slave02: 192.168.175.102


---------------------------------------------------------------------------------------------------
搭建 本地 yum repo 服务器

因为 外网 网速 太慢, 所有这次 准备自己 搭建 一台 简单的 local yum repo 服务器, 通过该 server 安装 mysql 软件.
具体步骤见:
      https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver


---------------------------------------------------------------------------------------------------
master 上 安装 mysql

// 配置 本地 yum 源, 参考 https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver
[root@master01 ~]# vim /etc/yum.repos.d/000-local-yum.repo

        [000-local-yum]
        name=000-local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0



[root@master ~]# yum repolist | grep local-yum
[root@master ~]# yum clean metadata
[root@master ~]# yum -y install mysql-community-server

[root@master ~]# rpm -q mysql-community-server
          mysql-community-server-5.7.26-1.el7.x86_64

[root@master ~]# yum list installed  mysql-community-server

[root@master ~]# systemctl start mysqld
[root@master ~]# systemctl enable mysqld.service
[root@master ~]# systemctl status mysqld.service

[root@master ~]# grep 'temporary password' /var/log/mysqld.log
        2019-07-18T02:35:40.301694Z 1 [Note] A temporary password is generated for root@localhost: O0MNuVV!7?#)

[root@master ~]# mysql -u root -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit

[root@master ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2067/mysqld

[root@master ~]# ps -elf | grep mysql
    1 S mysql      2067      1  0  80   0 - 279982 poll_s 15:52 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


---------------------------------------------------------------------------------------------------
在 slave01, slave02 上安装 mysql, 方法 与 如上 master 安装方法一样 (此处略)




---------------------------------------------------------------------------------------------------










---------------------------------------------------------------------------------------------------
网上资料:

16.3.9 Semisynchronous Replication
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html

16.3.9.1 Semisynchronous Replication Administrative Interface
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html

16.3.9.2 Semisynchronous Replication Installation and Configuration
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html

      5.5.1 Installing and Uninstalling Plugins
            https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html

16.3.9.3 Semisynchronous Replication Monitoring
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-monitoring.html






