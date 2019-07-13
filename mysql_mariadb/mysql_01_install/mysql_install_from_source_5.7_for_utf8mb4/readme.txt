
https://dev.mysql.com/doc/refman/5.7/en/source-installation.html

https://dev.mysql.com/doc/refman/5.7/en/getting-mysql.html
https://dev.mysql.com/downloads/
https://dev.mysql.com/doc/refman/5.7/en/postinstallation.html
https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html


// 删除mariadb, 避免冲突
[root@dbserver ~]# rpm -qa | grep mariadb
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
-DDEFAULT_CHARSET=utf8mb4 \
-DDEFAULT_COLLATION=utf8mb4_unicode_ci \
-DMYSQL_DATADIR=/mydata/data \
-DMYSQL_TCP_PORT=3306 \
-DWITH_BOOST=../boost/boost_1_59_0/ \
-DWITH_MYISAM_STORAGE_ENGINE=1 \
-DWITH_INNOBASE_STORAGE_ENGINE=1 \
-DWITH_ARCHIVE_STORAGE_ENGINE=1 \
-DWITH_BLACKHOLE_STORAGE_ENGINE=1 \


[root@dbserver build]# make
[root@dbserver build]# make install


[root@dbserver ~]# chown -R root:mysql /app/mysql/

[root@dbserver ~]# vim /etc/profile
      export PATH=$PATH:/app/mysql/bin

[root@dbserver ~]# source /etc/profile

// 初始化数据库
// https://dev.mysql.com/doc/refman/5.7/en/data-directory-initialization.html

[root@dbserver ~]# mysqld --initialize --user=mysql --basedir=/app/mysql/  --datadir=/mydata/data     #注意记录下该命令生成的临时密码
      2019-07-12T01:52:54.230447Z 1 [Note] A temporary password is generated for root@localhost: p>uHsTkl#5pF  #<<<<<<<记下临时密码

---------------------------------------------------------------------------------------------------
// 准备mysql的配置文件
// 注：从mysql5.7.18开始，安装后不再有support-files/my-default.cnf 文件了, 见  https://dev.mysql.com/doc/refman/5.7/en/server-configuration-defaults.html
//     解决办法，从其他版本的安装目录中的support-files目录下copy一份过来
[root@dbserver ~]# wget -O  /etc/my.cnf https://raw.githubusercontent.com/yangsg/linux_training_notes/master/mysql_mariadb/mysql_01_install/mysql_install_from_source_5.7/support-files/my-default.cnf

[root@dbserver ~]# vim /etc/my.cnf
            # 这里之所以 在 [client] 和 [mysql] 中 明确 设置 default-character-set=utf8mb4
            # , 是为了 使 各种 本地的 mysql client 客户端 在 与 mysql server 通信时 使用
            # utf8mb4, 使其 不不同的环节 是的 字符编码 都能保持一致 (即使用 utf8mb4)
            # 在 该配置 写在 option files 里 也避免了 调用 mysql client 相关程序时
            # 因未指定 编码参数时 而 犯错
            [client]   # 注: 其实 [client] group 中的 设置 会被所有的 mysql client 客户端程序 读取
            default-character-set=utf8mb4

            # 其实有了前面 [client] 中与 [mysql] 相同配置, [mysql] 中与之重复的相同
            # 的配置不是必须的, 但这里还是明确重复给出一遍, 应该是考虑到 更好的可读性,
            # 可以 明确的 提示 管理员或开发者在 connect 到 mysql server 时需要 关心考虑
            # 参数设置
            [mysql]
            default-character-set=utf8mb4

            [mysqld]
            # 参考 https://dev.mysql.com/doc/refman/5.5/en/charset-applications.html
            # 因为 此处 采用的 是源码编译 安装, 指定了 构建参数, 如下:
            # cmake .  -DDEFAULT_CHARSET=utf8mb4  -DDEFAULT_COLLATION=utf8mb4_unicode_ci
            # 所有 无需在 startup 时再指定 --character-set-server 和 --collation-server
            # 以及 无需在 connected 到 server 之后 再 使用 SET NAMES 或 等价的指定 来
            # 配置 其 connection.
            # 不过 出于 可读性 和 提示 的考虑, 这里还是 给出了 启动时的 相应配置:
            character-set-server=utf8mb4            # 保持 可读性(可选, 因cmake 时已指定其设置)
            collation-server=utf8mb4_unicode_ci     # 保持 可读性(可选, 因cmake 时已指定其设置)
            character-set-client-handshake = FALSE  # 该行必须 # To ignore client information and use the default server character set

            basedir=/app/mysql
            datadir=/mydata/data
            port=3306
            server_id=30
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
      tcp6       0      0 :::3306                 :::*                    LISTEN      36443/mysqld


// 数据库初始化安全设置 https://dev.mysql.com/doc/refman/5.7/en/mysql-secure-installation.html
[root@dbserver ~]# mysql_secure_installation

[root@dbserver ~]# mysql -h localhost -u root -p
mysql> pager less -Fi
mysql> show global variables like '%log%';



---------------------------------------------------------------------------------------------------
与字符编码相关信息:

[root@dbserver ~]# mysqld --verbose --help | grep -E 'char|collation'
            --character-set-client-handshake
                                Don't ignore client side character set value sent during
                                (Defaults to on; use --skip-character-set-client-handshake to disable.)
            --character-set-filesystem=name
                                Set the filesystem character set.
            -C, --character-set-server=name
                                Set the default character set.
            --character-sets-dir=name
                                Directory where character sets are
            --collation-server=name
                                Set the default collation.
                                InnoDB Fulltext search maximum token size in characters
                                InnoDB Fulltext search minimum token size in characters
                                This characterizes the number of hits a hot block has to
                                characters
                                characteristics (isolation level, read only/read write,
          character-set-client-handshake                               FALSE   <---------观察
          character-set-filesystem                                     binary
          character-set-server                                         utf8mb4 <---------观察
          character-sets-dir                                           /app/mysql/share/charsets/
          collation-server                                             utf8mb4_unicode_ci  <---------观察
          session-track-system-variables                               time_zone,autocommit,character_set_client,character_set_results,character_set_connection


[root@dbserver ~]# mysql --help | grep char
          --character-sets-dir=name
                              Directory for character set files.
          --default-character-set=name
                              Set the default character set.
        character-sets-dir                (No default value)
        default-character-set             utf8mb4 <---------观察

[root@dbserver ~]# mysqldump --help | grep default-character-set
          --default-character-set=name
        default-character-set             utf8mb4 <---------观察

---------------------------------------------------------------------------------------------------
在 client 端 测试检查 字符编码 相关信息

// 安装 client 客户端 工具
[root@client ~]# yum -y install mariadb

[root@client ~]# mysql -h 192.168.175.30 -u root -p

MySQL [(none)]> SHOW VARIABLES LIKE 'character%';
            +--------------------------+----------------------------+
            | Variable_name            | Value                      |
            +--------------------------+----------------------------+
            | character_set_client     | utf8mb4                    | <-----(这几项应保持一致) 参考: https://www.jianshu.com/p/f7d7609de6b0
            | character_set_connection | utf8mb4                    | <-----
            | character_set_database   | utf8mb4                    | <-----
            | character_set_filesystem | binary                     |
            | character_set_results    | utf8mb4                    | <-----
            | character_set_server     | utf8mb4                    | <-----
            | character_set_system     | utf8                       |
            | character_sets_dir       | /app/mysql/share/charsets/ |
            +--------------------------+----------------------------+



MySQL [(none)]> SHOW VARIABLES LIKE 'collation%';
            +----------------------+--------------------+
            | Variable_name        | Value              |
            +----------------------+--------------------+
            | collation_connection | utf8mb4_unicode_ci |
            | collation_database   | utf8mb4_unicode_ci |
            | collation_server     | utf8mb4_unicode_ci |
            +----------------------+--------------------+


// 一条更 方便的语句. 参考  https://www.jianshu.com/p/f7d7609de6b0
MySQL [(none)]> SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';
            +--------------------------+----------------------------+
            | Variable_name            | Value                      |
            +--------------------------+----------------------------+
            | character_set_client     | utf8mb4                    | <-----
            | character_set_connection | utf8mb4                    | <-----
            | character_set_database   | utf8mb4                    | <-----
            | character_set_filesystem | binary                     |
            | character_set_results    | utf8mb4                    | <-----
            | character_set_server     | utf8mb4                    | <-----
            | character_set_system     | utf8                       |
            | character_sets_dir       | /app/mysql/share/charsets/ |
            | collation_connection     | utf8mb4_unicode_ci         |
            | collation_database       | utf8mb4_unicode_ci         |
            | collation_server         | utf8mb4_unicode_ci         |
            +--------------------------+----------------------------+


MySQL [(none)]> status;
            --------------
            mysql  Ver 15.1 Distrib 5.5.60-MariaDB, for Linux (x86_64) using readline 5.1

            Connection id:          4
            Current database:
            Current user:           root@192.168.175.139
            SSL:                    Not in use
            Current pager:          stdout
            Using outfile:          ''
            Using delimiter:        ;
            Server:                 MySQL
            Server version:         5.7.25 Source distribution
            Protocol version:       10
            Connection:             192.168.175.30 via TCP/IP
            Server characterset:    utf8mb4  <---------观察
            Db     characterset:    utf8mb4  <---------观察
            Client characterset:    utf8mb4  <---------观察
            Conn.  characterset:    utf8mb4  <---------观察
            TCP port:               3306
            Uptime:                 52 min 27 sec

            Threads: 3  Questions: 17  Slow queries: 0  Opens: 112  Flush tables: 1  Open tables: 105  Queries per second avg: 0.005
            --------------


---------------------------------------------------------------------------------------------------
网上资料:

关于 jdbc driver:
    https://dev.mysql.com/downloads/connector/j/
      MySQL Connector/J 8.0 is highly recommended for use with MySQL Server 8.0, 5.7, 5.6, and 5.5. Please upgrade to MySQL Connector/J 8.0.

      [root@dbserver download]# wget https://dev.mysql.com/get/Downloads/Connector-J/mysql-connector-java-8.0.16.tar.gz



关于 mysql utf8 和 utf8mb4 的资料:

      https://blog.csdn.net/u010584271/article/details/80835547
      https://yq.aliyun.com/articles/138488
      https://mathiasbynens.be/notes/mysql-utf8mb4
      https://blog.csdn.net/leipeng321123/article/details/50428020
      https://blog.csdn.net/l1028386804/article/details/53441395
      https://stackoverflow.com/questions/30074492/what-is-the-difference-between-utf8mb4-and-utf8-charsets-in-mysql
      https://www.cnblogs.com/straybirds/p/6392306.html

  mysql 设置 字符编码:
      https://dev.mysql.com/doc/refman/5.7/en/charset-server.html

  jdbc 关于 utf8mb4 的设置:
      https://stackoverflow.com/questions/44591895/utf8mb4-in-mysql-workbench-and-jdbc
      https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-charsets.html
      https://www.jianshu.com/p/f7d7609de6b0
      https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-usagenotes-troubleshooting.html


      http://unicode-table.com/

在线工具列表:
      https://github.com/yangsg/linux_training_notes/tree/master/linux_basic/centos7.4
---------------------------------------------------------------------------------------------------
https://dev.mysql.com/doc/connector-j/5.1/en/connector-j-reference-charsets.html
https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-reference-charsets.html

    更多信息见官网
Warning
    Do not issue the query SET NAMES with Connector/J, as the driver will not detect that the character
    set has been changed by the query, and will continue to use the character set configured when the connection was first set up.


mysql 8.0 jdbc 驱动的变化:
    https://www.runoob.com/java/java-mysql-connect.html

        MySQL 8.0 以上版本的数据库连接有所不同：
              1、MySQL 8.0 以上版本驱动包版本 mysql-connector-java-8.0.16.jar。
              2、com.mysql.jdbc.Driver 更换为 com.mysql.cj.jdbc.Driver。
              MySQL 8.0 以上版本不需要建立 SSL 连接的，需要显示关闭。
              最后还需要设置 CST。
---------------------------------------------------------------------------------------------------

#其他一些小技巧：
https://www.psce.com/en/blog/2012/06/02/how-to-find-mysql-binary-logs-error-logs-temporary-files/
  lsof -nc mysqld | grep -vE '(.so(..*)?$|.frm|.MY?|.ibd|ib_logfile|ibdata|TCP)'


