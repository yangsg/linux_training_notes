
注: 本例 演示 通过 rpm 方式安装 mysql5.7 后 并设置 默认的 utf8 支持
     其实 在 mysql 中 最好是 不要 使用 utf8 而是 使用 utf8mb4

// 操作系统信息
[root@mysql5server ~]# cat /etc/redhat-release
    CentOS Linux release 7.4.1708 (Core)
[root@mysql5server ~]# uname -r
    3.10.0-693.el7.x86_64

// 查看 本机 ip
[root@mysql5server ~]# ip addr show ens33  | awk '/inet / {print $2}'  # 查看 ip 地址
    192.168.175.36/24


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
        mysql-connectors-community/x86_64  MySQL Connectors Community    enabled:    108
        mysql-connectors-community-source  MySQL Connectors Community -  disabled
        mysql-tools-community/x86_64       MySQL Tools Community         enabled:     90
        mysql-tools-community-source       MySQL Tools Community - Sourc disabled
        mysql-tools-preview/x86_64         MySQL Tools Preview           disabled
        mysql-tools-preview-source         MySQL Tools Preview - Source  disabled
        mysql55-community/x86_64           MySQL 5.5 Community Server    disabled
        mysql55-community-source           MySQL 5.5 Community Server -  disabled
        mysql56-community/x86_64           MySQL 5.6 Community Server    disabled
        mysql56-community-source           MySQL 5.6 Community Server -  disabled
        mysql57-community/x86_64           MySQL 5.7 Community Server    disabled
        mysql57-community-source           MySQL 5.7 Community Server -  disabled
        mysql80-community/x86_64           MySQL 8.0 Community Server    enabled:    113
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
      mysql-connectors-community/x86_64 MySQL Connectors Community                 108
      mysql-tools-community/x86_64      MySQL Tools Community                       90
      mysql57-community/x86_64          MySQL 5.7 Community Server                 347

// 开始安装 mysql-community-server
[root@mysql5server ~]# yum -y install mysql-community-server

// 验证安装
[root@mysql5server ~]# rpm -q mysql-community-server
    mysql-community-server-5.7.26-1.el7.x86_64

        #// 注：如果只是想收集mysql-community-server相关的rpm文件，可以执行类似如下命令只下载不安装
        #// yum install mysql-community-server --downloadonly --downloaddir=/tmp/mysql_rpm_files
        #//                 [root@mysql5server ~]# tree /tmp/mysql_rpm_files/
        #//                 /tmp/mysql_rpm_files/
        #//                 ├── mysql-community-client-5.7.26-1.el7.x86_64.rpm
        #//                 ├── mysql-community-common-5.7.26-1.el7.x86_64.rpm
        #//                 ├── mysql-community-libs-5.7.26-1.el7.x86_64.rpm
        #//                 ├── mysql-community-libs-compat-5.7.26-1.el7.x86_64.rpm
        #//                 ├── mysql-community-server-5.7.26-1.el7.x86_64.rpm
        #//                 └── postfix-2.10.1-7.el7.x86_64.rpm



// 启动 mysql server
[root@mysql5server ~]# systemctl start mysqld.service     #//centos6 可使用命令 `sudo service mysqld start`
[root@mysql5server ~]# systemctl enable mysqld.service    # 设置开机自启
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
    2019-07-11T12:16:57.405614Z 1 [Note] A temporary password is generated for root@localhost: 1!&9aRnphwga

[root@mysql5server ~]# mysql -uroot -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit


// 查看启动信息
[root@mysql5server ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2266/mysqld
[root@mysql5server ~]# ps -elf | grep mysql
    1 S mysql      2266      1  0  80   0 - 279982 poll_s 20:17 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid

---------------------------------------------------------------------------------------------------
设置 字符集 为 utf8 (注: mysql 中 utf8 并非并非最佳选择, utf8mb4 才是)

[root@mysql5server ~]# vim /etc/my.cnf

          [client]   # 注: 其实 [client] group 中的 设置 会被所有的 mysql client 客户端程序 读取
          default-character-set=utf8

          [mysql]
          default-character-set=utf8

          [mysqld]
          # 注: 如果使用 utf8 和 utf8_general_ci, 则 [mysqld] group 的字符集相关配置只需如下 2 行即可
          character-set-server=utf8  # 注: 设置了 character-set-server 就应该 同时设置 collation-server
          collation-server=utf8_general_ci #注: 实际中应 思考应使用了 utf8_general_ci 还是 utf8_unicode_ci,  utf8_general_ci 更快(可能快不了多少), utf8_unicode_ci 更精准

          ## 如果要使用 utf8 和 utf8_unicode_ci, 则 最好的解决的办法是 自己手动源码编译安装 mysql,
          ## 在在构建的时候指定 cmake . -DDEFAULT_CHARSET=utf8  -DDEFAULT_COLLATION=utf8_unicode_ci 设置,
          ## 见 https://dev.mysql.com/doc/refman/5.5/en/charset-applications.html

          ##character-set-server=utf8  # 注: 设置了 character-set-server 就应该 同时设置 collation-server
          ##注: 实际中应 思考应使用了 utf8_general_ci 还是 utf8_unicode_ci,  utf8_general_ci 更快(可能快不了多少), utf8_unicode_ci 更精准
          ##collation-server=utf8_unicode_ci
          ##忽略客户端信息并使用server默认字符集 # https://dev.mysql.com/doc/refman/5.7/en/server-options.html#option_mysqld_character-set-client-handshake
          ##character-set-client-handshake=FALSE
          ##https://dev.mysql.com/doc/refman/5.5/en/server-system-variables.html#sysvar_init_connect
          ##https://dev.mysql.com/doc/refman/5.5/en/charset-applications.html
          ## 注: 对于具有 SUPER privilege 的 user, init_connect的 内容不会被执行,
          ##     这有可能 导致 数据的不一致。这一特性的存在时 为了 让 SUPER privilege的
          ##     user 在 init_connect 的 内容 存在 error 时 仍然能够 connect 到 server
          ##     并 修改 error 或 bug.
          ##https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_collation_connection
          ##init_connect='SET collation_connection = utf8_unicode_ci'
          ##init_connect='SET NAMES utf8'    # 使 client 与 server 通信时使用 utf8  # https://dev.mysql.com/doc/refman/5.7/en/set-names.html

          ##utf8_unicode_ci 和 utf8_general_ci 的区别见:
          ##   https://stackoverflow.com/questions/766809/whats-the-difference-between-utf8-general-ci-and-utf8-unicode-ci

[root@mysql5server ~]# mysql --help | grep char
            --character-sets-dir=name
                                Directory for character set files.
            --default-character-set=name
                                Set the default character set.
          character-sets-dir                (No default value)
          default-character-set             utf8  <----------- 观察

[root@mysql5server ~]# mysqld --verbose --help | grep -E 'character-set|collation-server'
            --character-set-client-handshake
                                (Defaults to on; use --skip-character-set-client-handshake to disable.)
            --character-set-filesystem=name
            -C, --character-set-server=name
            --character-sets-dir=name
            --collation-server=name
          character-set-client-handshake                               TRUE  <----------- 观察
          character-set-filesystem                                     binary
          character-set-server                                         utf8  <----------- 观察
          character-sets-dir                                           /usr/share/mysql/charsets/
          collation-server                                             utf8_general_ci  <----------- 观察




// 重启 mysqld 是 /etc/my.cnf 修改的配置 生效
[root@mysql5server ~]# systemctl restart mysqld


[root@mysql5server ~]# mysql -u root -p

mysql> SHOW VARIABLES LIKE 'character%';
          +--------------------------+----------------------------+
          | Variable_name            | Value                      |
          +--------------------------+----------------------------+
          | character_set_client     | utf8                       | <-----(这几项应保持一致) 参考: https://www.jianshu.com/p/f7d7609de6b0
          | character_set_connection | utf8                       | <-----
          | character_set_database   | utf8                       | <-----
          | character_set_filesystem | binary                     |
          | character_set_results    | utf8                       | <-----
          | character_set_server     | utf8                       | <-----
          | character_set_system     | utf8                       |
          | character_sets_dir       | /usr/share/mysql/charsets/ |
          +--------------------------+----------------------------+

mysql> SHOW VARIABLES LIKE 'collation%';
          +----------------------+-----------------+
          | Variable_name        | Value           |
          +----------------------+-----------------+
          | collation_connection | utf8_general_ci |
          | collation_database   | utf8_general_ci |
          | collation_server     | utf8_general_ci |
          +----------------------+-----------------+


// 一条更 方便的语句. 参考  https://www.jianshu.com/p/f7d7609de6b0
mysql> SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';
          +--------------------------+----------------------------+
          | Variable_name            | Value                      |
          +--------------------------+----------------------------+
          | character_set_client     | utf8                       | <-----
          | character_set_connection | utf8                       | <-----
          | character_set_database   | utf8                       | <-----
          | character_set_filesystem | binary                     |
          | character_set_results    | utf8                       | <-----
          | character_set_server     | utf8                       | <-----
          | character_set_system     | utf8                       |
          | character_sets_dir       | /usr/share/mysql/charsets/ |
          | collation_connection     | utf8_general_ci            |
          | collation_database       | utf8_general_ci            |
          | collation_server         | utf8_general_ci            |
          +--------------------------+----------------------------+

mysql> status
          --------------
          mysql  Ver 14.14 Distrib 5.7.26, for Linux (x86_64) using  EditLine wrapper

          Connection id:          2
          Current database:
          Current user:           root@localhost
          SSL:                    Not in use
          Current pager:          stdout
          Using outfile:          ''
          Using delimiter:        ;
          Server version:         5.7.26 MySQL Community Server (GPL)
          Protocol version:       10
          Connection:             Localhost via UNIX socket
          Server characterset:    utf8
          Db     characterset:    utf8
          Client characterset:    utf8
          Conn.  characterset:    utf8
          UNIX socket:            /var/lib/mysql/mysql.sock
          Uptime:                 15 min 18 sec

          Threads: 2  Questions: 14  Slow queries: 0  Opens: 112  Flush tables: 1  Open tables: 105  Queries per second avg: 0.015
          --------------



---------------------------------------------------------------------------------------------------
网上资料:

#// 其他更多与安装mysql的信息，都可以查看访问 https://dev.mysql.com/doc/mysql-yum-repo-quick-guide/en/

    https://stackoverflow.com/questions/38949115/how-to-change-the-connection-collation-of-mysql
    https://www.jb51.net/article/92802.htm

帮助体会源码编译的好处:
      https://dev.mysql.com/doc/refman/5.5/en/charset-applications.html


utf8mb4_unicode_ci 和  utf8mb4_general_ci 的区别
    https://stackoverflow.com/questions/766809/whats-the-difference-between-utf8-general-ci-and-utf8-unicode-ci

    大体上,
        utf8mb4_unicode_ci 更精准, 基于 Unicode standard, 在 更广范围的语言的排序时 更精准.
        utf8mb4_general_ci 速度更快(但在现代服务器上, 这种性能提升几乎可以忽略不计), 但其 没有完全 遵循 Unicode sorting rules,
                           在某些情况下可能导致 undesirable sorting,
                           特别是使用某些特定的 particular languages 或 characters 时.

