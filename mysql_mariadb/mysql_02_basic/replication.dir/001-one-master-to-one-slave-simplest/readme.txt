
ip信息：
    master: 192.168.175.100/24
    slave:  192.168.175.101/24

// 前期准备：设置时区 和 同步时间,  参考  https://github.com/yangsg/linux_training_notes/tree/master/ntp_chrony_basic

// master设置时区和同步时间
[root@master ~]# timedatectl set-timezone Asia/Shanghai
[root@master ~]# timedatectl status | grep 'Time zone'
       Time zone: Asia/Shanghai (CST, +0800)

[root@master ~]# yum -y install chrony
[root@master ~]# vim /etc/chrony.conf   #// 生产环境应该是同步到自己内部搭建的ntp服务器

      #server 0.centos.pool.ntp.org iburst
      #server 1.centos.pool.ntp.org iburst
      #server 2.centos.pool.ntp.org iburst
      #server 3.centos.pool.ntp.org iburst

      server ntp1.aliyun.com iburst
      server ntp2.aliyun.com iburst
      server ntp3.aliyun.com iburst
      server ntp4.aliyun.com iburst
      server ntp5.aliyun.com iburst
      server ntp6.aliyun.com iburst
      server ntp7.aliyun.com iburst

[root@master ~]# systemctl start chronyd
[root@master ~]# systemctl enable chronyd

[root@master ~]# chronyc sources -v
[root@master ~]# timedatectl | grep 'NTP enabled'
     NTP enabled: yes


// slave 上按照与master相同的方式设置时区和同步时间
[root@slave ~]# timedatectl set-timezone Asia/Shanghai
[root@slave ~]# timedatectl status | grep 'Time zone'
       Time zone: Asia/Shanghai (CST, +0800)

[root@slave ~]# yum -y install chrony
[root@slave ~]# vim /etc/chrony.conf   #// 生产环境应该是同步到自己内部搭建的ntp服务器

      #server 0.centos.pool.ntp.org iburst
      #server 1.centos.pool.ntp.org iburst
      #server 2.centos.pool.ntp.org iburst
      #server 3.centos.pool.ntp.org iburst

      server ntp1.aliyun.com iburst
      server ntp2.aliyun.com iburst
      server ntp3.aliyun.com iburst
      server ntp4.aliyun.com iburst
      server ntp5.aliyun.com iburst
      server ntp6.aliyun.com iburst
      server ntp7.aliyun.com iburst

[root@slave ~]# systemctl start chronyd
[root@slave ~]# systemctl enable chronyd

[root@slave ~]# chronyc sources -v
[root@slave ~]# timedatectl | grep 'NTP enabled'
     NTP enabled: yes


// 安装 mysql 参考  https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_01_install/mysql_install_from_rpm_5.7
[root@master ~]# mkdir download && cd download
[root@master download]# wget --no-check-certificate https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@master download]# yum -y install mysql80-community-release-el7-2.noarch.rpm
[root@master download]# ls /etc/yum.repos.d/ | grep mysql
    mysql-community.repo
    mysql-community-source.repo
[root@master download]# ls /etc/yum.repos.d/ | grep mysql
    mysql-community.repo
    mysql-community-source.repo

[root@master download]# yum repolist all | grep mysql
      mysql-cluster-7.5-community/x86_64 MySQL Cluster 7.5 Community   disabled
      mysql-cluster-7.5-community-source MySQL Cluster 7.5 Community - disabled
      mysql-cluster-7.6-community/x86_64 MySQL Cluster 7.6 Community   disabled
      mysql-cluster-7.6-community-source MySQL Cluster 7.6 Community - disabled
      mysql-connectors-community/x86_64  MySQL Connectors Community    enabled:     95
      mysql-connectors-community-source  MySQL Connectors Community -  disabled
      mysql-tools-community/x86_64       MySQL Tools Community         enabled:     84
      mysql-tools-community-source       MySQL Tools Community - Sourc disabled
      mysql-tools-preview/x86_64         MySQL Tools Preview           disabled
      mysql-tools-preview-source         MySQL Tools Preview - Source  disabled
      mysql55-community/x86_64           MySQL 5.5 Community Server    disabled
      mysql55-community-source           MySQL 5.5 Community Server -  disabled
      mysql56-community/x86_64           MySQL 5.6 Community Server    disabled
      mysql56-community-source           MySQL 5.6 Community Server -  disabled
      mysql57-community/x86_64           MySQL 5.7 Community Server    disabled
      mysql57-community-source           MySQL 5.7 Community Server -  disabled
      mysql80-community/x86_64           MySQL 8.0 Community Server    enabled:     82
      mysql80-community-source           MySQL 8.0 Community Server -  disabled


[root@master download]# vim /etc/yum.repos.d/mysql-community.repo
      # Enable to use MySQL 5.7
      [mysql57-community]
      name=MySQL 5.7 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-5.7-community/el/7/$basearch/
      #// enabled=1 表示启用仓库
      enabled=1
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

      [mysql80-community]
      name=MySQL 8.0 Community Server
      baseurl=http://repo.mysql.com/yum/mysql-8.0-community/el/7/$basearch/
      #// enabled=0 表示禁用仓库
      enabled=0
      gpgcheck=1
      gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-mysql

[root@master download]# yum repolist enabled | grep mysql
      mysql-connectors-community/x86_64 MySQL Connectors Community                  95
      mysql-tools-community/x86_64      MySQL Tools Community                       84
      mysql57-community/x86_64          MySQL 5.7 Community Server                 327

[root@master download]# yum -y install mysql-community-server

[root@master download]# rpm -q mysql-community-server
      mysql-community-server-5.7.25-1.el7.x86_64

[root@master ~]# systemctl start mysqld.service
[root@master ~]# systemctl enable mysqld.service
[root@master ~]# systemctl status mysqld.service

[root@master ~]# grep 'temporary password' /var/log/mysqld.log
2019-04-04T13:05:09.097245Z 1 [Note] A temporary password is generated for root@localhost: h5GulK<>uN#s

[root@master ~]# mysql -u root -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
mysql> exit

[root@master ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2268/mysqld

[root@master ~]# ps -elf | grep mysql
    1 S mysql      2268      1  0  80   0 - 279981 poll_s 21:05 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid































