
// 操作系统信息
[root@mysql5server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@mysql5server ~]# uname -r
    3.10.0-693.el7.x86_64



https://dev.mysql.com/downloads/repo/yum/

// MySQL Yum Repository快速指南
https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/

[root@mysql5server download]# wget https://dev.mysql.com/get/mysql80-community-release-el7-2.noarch.rpm
[root@mysql5server download]# yum -y install mysql80-community-release-el7-2.noarch.rpm

// 查看安装的如下两个mysql yum仓库配置文件
[root@mysql5server ~]# ls /etc/yum.repos.d/ | grep mysql
    mysql-community.repo
    mysql-community-source.repo

// 查看mysql yum仓库及其子仓库
[root@mysql5server ~]# yum repolist all | grep mysql
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


// 编辑mysql-community.repo 来禁用mysql80仓库并启用mysql57仓库
[root@mysql5server ~]# vim /etc/yum.repos.d/mysql-community.repo
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

// 注意：应该在任何时刻只启用enable一个特定mysql版本的的仓库，否则如果启用多个，最新版本的mysql会被安装
// 检查如上的mysql-community.repo编辑是否符合预期
[root@mysql5server ~]# yum repolist enabled | grep mysql
      mysql-connectors-community/x86_64 MySQL Connectors Community                  95
      mysql-tools-community/x86_64      MySQL Tools Community                       84
      mysql57-community/x86_64          MySQL 5.7 Community Server                 327


// 开始安装 mysql-community-server
[root@mysql5server ~]# yum -y install mysql-community-server

// 验证安装
[root@mysql5server ~]# rpm -q mysql-community-server
    mysql-community-server-5.7.25-1.el7.x86_64


#// 注：如果只是想收集mysql-community-server相关的rpm文件，可以执行类似如下命令只下载不安装
#// yum install mysql-community-server --downloadonly --downloaddir=/tmp/mysql_rpm_files
#//            [root@mysql5server ~]# tree /tmp/mysql_rpm_files/
#//            /tmp/mysql_rpm_files/
#//            ├── mysql-community-client-5.7.25-1.el7.x86_64.rpm
#//            ├── mysql-community-common-5.7.25-1.el7.x86_64.rpm
#//            ├── mysql-community-libs-5.7.25-1.el7.x86_64.rpm
#//            ├── mysql-community-libs-compat-5.7.25-1.el7.x86_64.rpm
#//            ├── mysql-community-server-5.7.25-1.el7.x86_64.rpm
#//            └── postfix-2.10.1-7.el7.x86_64.rpm
#//


// 启动 mysql server
[root@mysql5server ~]# systemctl start mysqld.service     #//centos6 可使用命令 `sudo service mysqld start`
[root@mysql5server ~]# systemctl status mysqld.service    # service mysqld status

#// mysql的一些初始化行为如下: https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/
#// MySQL Server Initialization (as of MySQL 5.7): At the initial start up of the server,
#// the following happens, given that the data directory of the server is empty:
#//
#//    The server is initialized.
#//
#//    An SSL certificate and key files are generated in the data directory.
#//
#//    The validate_password plugin is installed and enabled.
#//
#//    A superuser account 'root'@'localhost' is created. A password for the superuser is set and stored in the error log file. To reveal it, use the following command:
#//
#//        shell> sudo grep 'temporary password' /var/log/mysqld.log
#//
#// Change the root password as soon as possible by logging in with the generated, temporary password and set a custom password for the superuser account:
#//        shell> mysql -uroot -p
#//        mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass4!';
#//
#// Note:
#// MySQL's validate_password plugin is installed by default. This will require that passwords contain at least
#// one upper case letter, one lower case letter, one digit, and one special character, and that the total password length is at least 8 characters.
#// 密码规则：至少1个大写字母，1个小写字母，1个数字，1个特殊字符, 长度至少8字符

// 找出默认初始密码
[root@mysql5server ~]# grep 'temporary password' /var/log/mysqld.log
      2019-03-27T11:35:04.494744Z 1 [Note] A temporary password is generated for root@localhost: h!SJ,1/1)ufB

// 修改密码
[root@mysql5server ~]# mysql -uroot -p
mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
mysql> exit

#// 其他更多与安装mysql的信息，都可以查看访问 https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/




















