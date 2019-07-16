
多源复制, 可理解为 多主一从


---------------------------------------------------------------------------------------------------
准备 实现 环境用的 3 台 主机:
master01
master02
slave

// 搭建 本地 yum repo 服务器
因为 外网 网速 太慢, 所有这次 准备自己 搭建 一台 简单的 local yum repo 服务器, 通过该 server 安装 mysql 软件.
具体步骤见:
      https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver

---------------------------------------------------------------------------------------------------
master01 上 安装 mysql

// 配置 本地 yum 源, 参考 https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver
[root@master01 ~]# vim /etc/yum.repos.d/000-local-yum.repo

        [000-local-yum]
        name=000-local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0



[root@master01 ~]# yum repolist | grep local-yum
[root@master01 ~]# yum clean metadata
[root@master01 ~]# yum -y install mysql-community-server

[root@master01 ~]# rpm -q mysql-community-server
[root@master01 ~]# yum list installed  mysql-community-server

[root@master01 ~]# systemctl start mysqld
[root@master01 ~]# systemctl enable mysqld.service
[root@master01 ~]# systemctl status mysqld.service

[root@master01 ~]# grep 'temporary password' /var/log/mysqld.log
        2019-07-16T07:52:45.755184Z 1 [Note] A temporary password is generated for root@localhost: M&ad)((tD0Y2

[root@master01 ~]# mysql -u root -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit

[root@master01 ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2067/mysqld

[root@master01 ~]# ps -elf | grep mysql
    1 S mysql      2067      1  0  80   0 - 279982 poll_s 15:52 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


---------------------------------------------------------------------------------------------------
在 master02, slave 上安装 mysql, 方法 与 如上 master01 安装方法一样 (此处略)

---------------------------------------------------------------------------------------------------



















---------------------------------------------------------------------------------------------------
网上资料:

16.1.4.1 MySQL Multi-Source Replication Overview
      https://dev.mysql.com/doc/refman/5.7/en/replication-multi-source-overview.html

16.2.3 Replication Channels
      https://dev.mysql.com/doc/refman/5.7/en/replication-channels.html



