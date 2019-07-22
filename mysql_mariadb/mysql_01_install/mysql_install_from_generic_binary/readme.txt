

安装通用二进制格式的 mysql

https://dev.mysql.com/doc/refman/5.7/en/source-installation.html

https://dev.mysql.com/doc/refman/5.7/en/getting-mysql.html
https://dev.mysql.com/downloads/
https://dev.mysql.com/doc/refman/5.7/en/postinstallation.html
https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html

---------------------------------------------------------------------------------------------------

// 下载 或 准备 通用二进制格式的 mysql 软件安装包
[root@dbserver ~]# mkdir download
[root@dbserver ~]# cd download/
[root@dbserver download]# tree
      .
      └── mysql-5.7.27-linux-glibc2.12-x86_64.tar.gz


// 卸载系统自带的mariadb
[root@dbserver ~]# rpm -qa | grep -i mariadb
    mariadb-libs-5.5.56-2.el7.x86_64
[root@dbserver ~]# rpm -e --nodeps mariadb-libs


// 确认 或 安装 通用二进制格式的 mysql 需要的依赖
[root@dbserver ~]# rpm -qa | grep -i libaio
    libaio-0.3.109-13.el7.x86_64   <---- 已经安装

// For MySQL 5.7.19 and later, 通用二进制的 mysql 会依赖 libnuma 库
[root@dbserver ~]# yum search libnuma
[root@dbserver ~]# yum -y install numactl-libs



[root@dbserver ~]# mkdir /app

[root@dbserver ~]# useradd -M -s /sbin/nologin mysql
[root@dbserver ~]# mkdir -p /mydata/data
[root@dbserver ~]# chown -R mysql:mysql /mydata/data/


[root@dbserver ~]# cd download/
[root@dbserver download]# ls
          mysql-5.7.27-linux-glibc2.12-x86_64.tar.gz

[root@dbserver download]# tar -xvf mysql-5.7.27-linux-glibc2.12-x86_64.tar.gz  -C /app/
[root@dbserver download]# cd /app/
[root@dbserver app]# ls
      mysql-5.7.27-linux-glibc2.12-x86_64

[root@dbserver app]# mv mysql-5.7.27-linux-glibc2.12-x86_64/ mysql
[root@dbserver app]# ls
      mysql

[root@dbserver app]# cd
[root@dbserver ~]# chown -R root:mysql /app/mysql/

[root@dbserver ~]# vim /etc/profile
      export PATH=$PATH:/app/mysql/bin

[root@dbserver ~]# source /etc/profile

// 初始化数据库
// https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html
[root@dbserver ~]# mysqld --initialize --user=mysql --basedir=/app/mysql/  --datadir=/mydata/data     #注意记录下该命令生成的临时密码
    2019-07-22T10:05:48.638560Z 1 [Note] A temporary password is generated for root@localhost: hca;a_baF1x1    #<<<<<<<记下临时密码

[root@dbserver ~]# vim /etc/my.cnf
    [mysqld]
    basedir=/app/mysql
    datadir=/mydata/data
    port=3306
    server_id=20
    socket=/tmp/mysql.sock

// 启动mysqld服务
[root@dbserver ~]# cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld
[root@dbserver ~]# chmod a+x /etc/init.d/mysqld
[root@dbserver ~]# chkconfig --add mysqld
[root@dbserver ~]# chkconfig mysqld on
[root@dbserver ~]# chkconfig --list mysqld

[root@dbserver ~]# /etc/init.d/mysqld start
Starting MySQL.Logging to '/mydata/data/dbserver.err'.
 SUCCESS!

[root@dbserver ~]# netstat -antp | grep :3306
      tcp6       0      0 :::3306                 :::*                    LISTEN      1867/mysqld

// 数据库初始化安全设置 https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html
[root@dbserver ~]# mysql_secure_installation

[root@dbserver ~]# mysql -h localhost -u root -p
mysql> pager less -Fi
mysql> show global variables like '%log%';



---------------------------------------------------------------------------------------------------
#其他一些小技巧：
https://www.psce.com/en/blog/2012/06/02/how-to-find-mysql-binary-logs-error-logs-temporary-files/
  lsof -nc mysqld | grep -vE '(.so(..*)?$|.frm|.MY?|.ibd|ib_logfile|ibdata|TCP)'




