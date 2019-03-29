https://dev.mysql.com/doc/refman/5.7/en/source-installation.html

https://dev.mysql.com/doc/refman/5.7/en/getting-mysql.html
https://dev.mysql.com/downloads/
https://dev.mysql.com/doc/refman/5.7/en/postinstallation.html
https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html


// 删除mariadb, 避免冲突
[root@dbserver ~]#  rpm -qa | grep mariadb
    mariadb-libs-5.5.56-2.el7.x86_64
[root@dbserver ~]# rpm -e --nodeps mariadb-libs


[root@dbserver ~]# yum -y install gcc gcc-c++ autoconf automake
[root@dbserver ~]# yum -y install cmake
[root@dbserver ~]# yum -y install ncurses-devel bison


//参考 https://dev.mysql.com/doc/refman/5.7/en/installing-source-distribution.html


[root@dbserver ~]# mkdir /app   #// 创建目标安装目录，准备将mysql安装到该目录下

[root@dbserver ~]# mkdir download
[root@dbserver ~]# cd download/
[root@dbserver download]# wget https://dev.mysql.com/get/Downloads/MySQL-5.7/mysql-boost-5.7.25.tar.gz
[root@dbserver download]# tar -xvf mysql-boost-5.7.25.tar.gz
[root@dbserver download]# cd mysql-5.7.25/

[root@dbserver mysql-5.7.25]# useradd -M -s /sbin/nologin mysql
[root@dbserver mysql-5.7.25]# mkdir -p /mydata/data
[root@dbserver mysql-5.7.25]# chown -R mysql:mysql /mydata/data/

[root@dbserver mysql-5.7.25]# mkdir build     #创建外部构建目录
[root@dbserver mysql-5.7.25]# cd build/

[root@dbserver build]# cmake .. \
-DCMAKE_INSTALL_PREFIX=/app/mysql \
-DMYSQL_UNIX_ADDR=/tmp/mysql.sock \
-DDEFAULT_CHARSET=utf8 \
-DDEFAULT_COLLATION=utf8_general_ci \
-DMYSQL_DATADIR=/mydata/data \
-DMYSQL_TCP_PORT=3306 \
-DWITH_BOOST=../boost/boost_1_59_0/ \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_ARCHIVE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \

[root@dbserver bld]# make
[root@dbserver build]# make install

[root@dbserver ~]# chown -R root:mysql /app/mysql/

[root@dbserver ~]# vim /etc/profile
    export PATH=$PATH:/app/mysql/bin

[root@dbserver ~]# source /etc/profile

// 初始化数据库
// https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html
[root@dbserver ~]# mysqld --initialize --user=mysql --basedir=/app/mysql/  --datadir=/mydata/data     #注意记录下该命令生成的临时密码
      2019-03-29T04:23:41.694432Z 1 [Note] A temporary password is generated for root@localhost: 4-fHhZ.?DiIf    #<<<<<<<记下临时密码

// 准备mysql的配置文件
// 注：从mysql5.7.18开始，安装后不再有support-files/my-default.cnf 文件了, 见  https://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html
//     解决办法，从其他版本的安装目录中的support-files目录下copy一份过来
[root@dbserver ~]# wget -O  /etc/my.cnf https://raw.githubusercontent.com/yangsg/linux_training_notes/master/mysql_mariadb/mysql_01_install/mysql_install_from_source_5.7/support-files/my-default.cnf

[root@dbserver ~]# vim /etc/my.cnf
      [mysqld]
      basedir=/app/mysql
      datadir=/mydata/data
      port=3306
      server_id=136
      socket=/tmp/mysql.sock


// 启动mysqld服务
[root@dbserver ~]# cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld
[root@dbserver ~]# chmod a+x /etc/init.d/mysqld
[root@dbserver ~]# chkconfig --add mysqld
[root@dbserver ~]# chkconfig mysqld on
[root@dbserver ~]# chkconfig --list mysqld
[root@dbserver ~]# /etc/init.d/mysqld start
[root@dbserver ~]# netstat -antp | grep :3306
    tcp6       0      0 :::3306                 :::*                    LISTEN      1711/mysqld


// 数据库初始化安全设置 https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html
[root@dbserver ~]# mysql_secure_installation


[root@dbserver ~]# mysql -h localhost -u root -p
mysql> pager less -Fi
mysql> show global variables like '%log%';



#其他一些小技巧：
https://www.psce.com/en/blog/2012/06/02/how-to-find-mysql-binary-logs-error-logs-temporary-files/
  lsof -nc mysqld | grep -vE '(.so(..*)?$|.frm|.MY?|.ibd|ib_logfile|ibdata|TCP)'

















