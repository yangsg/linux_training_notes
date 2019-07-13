
// 查看本机 ip 地址
[root@mycatserver ~]# ip addr show ens33  | awk '/inet / {print $2}'  # 查看 ip 地址
192.168.175.88/24


注: 本示例 假设 后端的 master 和 slave 中 使用的字符编码设置如下:

            [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
            default-character-set = utf8mb4

            [mysql]
            default-character-set = utf8mb4


            [mysqld]
            # 设置 mysql 字符集为 utf8
            character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
            character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
            collation-server = utf8mb4_unicode_ci

---------------------------------------------------------------------------------------------------
该 示例 使用了 master - slave 的 mysql replication 环境, 具体见:

    https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/001-one-master-to-one-slave-simplest

针对本示例 对 数据库 执行的 一些 操作(如下操作都是在 master 上执行, 然后 自动同步 给 slave):


// 创建 示例数据库 , 语法 参见 https://dev.mysql.com/doc/refman/5.7/en/charset-database.html
mysql> CREATE DATABASE jiaowu CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;


// 创建 mycat 访问 后台 mysql servers 的 user 和 对其进行 授权
mysql> create user 'admin'@'192.168.175.88' identified by 'WWW.1.com';
mysql> grant all on jiaowu.* to 'admin'@'192.168.175.88';

---------------------------------------------------------------------------------------------------

// 下载 mycat
[root@mycatserver ~]# mkdir download && cd download
[root@mycatserver download]# wget http://dl.mycat.io/1.6.7.1/Mycat-server-1.6.7.1-release-20190627191042-linux.tar.gz

// 查看 以准备的 软件包
[root@mycatserver download]# tree
      .
      ├── jdk-8u202-linux-x64.tar.gz
      └── Mycat-server-1.6.7.1-release-20190627191042-linux.tar.gz

---------------------------------------------------------------------------------------------------
// 安装 jdk (因 mycat 由 java 实现, 且 至少 jdk7)

[root@mycatserver download]# mkdir /app     # 创建自定义 软件 安装目录
[root@mycatserver download]# tar -xvf jdk-8u202-linux-x64.tar.gz -C /app

[root@mycatserver download]# ls /app/
        jdk1.8.0_202

// 配置 jdk 相关 环境变量
[root@mycatserver download]# vim /etc/profile
        # 安装 jdk 都 最好定义变量 JAVA_HOME, 因为许多 java的 程序或框架会依赖该变量
        export JAVA_HOME=/app/jdk1.8.0_202
        export PATH=$PATH:$JAVA_HOME/bin

// 执行 /etc/profile
[root@mycatserver download]# source /etc/profile

// 验证 jdk
[root@mycatserver download]# java -version
java version "1.8.0_202"
Java(TM) SE Runtime Environment (build 1.8.0_202-b08)
Java HotSpot(TM) 64-Bit Server VM (build 25.202-b08, mixed mode)

---------------------------------------------------------------------------------------------------
// 安装 mycat

[root@mycatserver download]# tar -xvf Mycat-server-1.6.7.1-release-20190627191042-linux.tar.gz -C /app
[root@mycatserver download]# ls /app/
      jdk1.8.0_202  mycat

[root@mycatserver download]# cd /app/mycat/
[root@mycatserver mycat]# ls
      bin  catlet  conf  lib  logs  version.txt

// 设置 环境变量 MYCAT_HOME
[root@mycatserver mycat]# vim /etc/profile
      export MYCAT_HOME=/app/mycat

[root@mycatserver mycat]# source /etc/profile



// 查看一下 版本信息
[root@mycatserver mycat]# cat version.txt
        BuildTime  2019-06-27 11:10:41
        GitVersion   738757c133cad7a06a690cb35196e00b37db2eab
        MavenVersion 1.6.7.1-release
        GitUrl https://github.com/MyCATApache/Mycat-Server.git
        MyCatSite http://www.mycat.org.cn
        QQGroup 106088787


// 查看一下 conf 目录
[root@mycatserver mycat]# ls conf/
    autopartition-long.txt      ehcache.xml                  partition-hash-int.txt    sequence_db_conf.properties           wrapper.conf
    auto-sharding-long.txt      index_to_charset.properties  partition-range-mod.txt   sequence_distributed_conf.properties  zkconf
    auto-sharding-rang-mod.txt  log4j2.xml                   rule.xml                  sequence_time_conf.properties         zkdownload
    cacheservice.properties     migrateTables.properties     schema.xml                server.xml
    dbseq.sql                   myid.properties              sequence_conf.properties  sharding-by-enum.txt

// 查看一下 bin 目录
[root@mycatserver mycat]# ls bin/
    dataMigrate.sh  init_zk_data.sh  mycat  rehash.sh  startup_nowrap.sh  wrapper-linux-ppc-64  wrapper-linux-x86-32  wrapper-linux-x86-64


[root@mycatserver mycat]# cp conf/schema.xml conf/schema.xml.bak
[root@mycatserver mycat]# vim conf/schema.xml
        <?xml version="1.0"?>
        <!DOCTYPE mycat:schema SYSTEM "schema.dtd">
        <mycat:schema xmlns:mycat="http://io.mycat/">

          <schema name="jiaowu" checkSQLschema="false" sqlMaxLimit="100" dataNode="dn1"></schema>

          <dataNode name="dn1" dataHost="dh1" database="jiaowu" />

          <dataHost name="dh1" maxCon="1000" minCon="10" balance="1"
            writeType="0" dbType="mysql" dbDriver="native" switchType="1"  slaveThreshold="100">
            <heartbeat>select user()</heartbeat>

            <writeHost host="hostM1" url="192.168.175.100:3306" user="admin" password="WWW.1.com"></writeHost>
            <writeHost host="hostS1" url="192.168.175.101:3306" user="admin" password="WWW.1.com" />

          </dataHost>
        </mycat:schema>



[root@mycatserver mycat]# cp conf/server.xml  conf/server.xml.bak
[root@mycatserver mycat]# vim conf/server.xml

        <!-- 找到 <system> 标签, 在其中添加 charset 的设置, 此处使用 utf8mb4 -->
        <system>
          <property name="charset">utf8mb4</property>
        </system>


        <!-- 删除多余的 <user> 标签, 值保留修改需要的 user 配置 -->
        <user name="mycatuser">
                <property name="password">1234</property>
                <property name="schemas">jiaowu</property>
        </user>


[root@mycatserver ~]# useradd -M -s /sbin/nologin mycat
[root@mycatserver ~]# chown -R mycat:mycat /app/mycat/
[root@mycatserver ~]# chmod -R go-rwx /app/mycat/

[root@mycatserver ~]# su - mycat -s /bin/bash -c 'cd /app/mycat/bin/  && ./mycat start'

// 查看 mycat 对应的 java 进程
[root@mycatserver ~]# ps -elf | grep java

[root@mycatserver ~]# netstat -anptu | grep java
        tcp        0      0 127.0.0.1:32000         0.0.0.0:*               LISTEN      1374/java
        tcp6       0      0 :::41013                :::*                    LISTEN      1374/java
        tcp6       0      0 :::1984                 :::*                    LISTEN      1374/java
        tcp6       0      0 :::8066                 :::*                    LISTEN      1374/java   <---- 8066 为 server port, 类似于 mysql 的 3306 端口
        tcp6       0      0 :::9066                 :::*                    LISTEN      1374/java   <---- 9066 为 管理端口(managerPort)
        tcp6       0      0 :::44138                :::*                    LISTEN      1374/java
        tcp6       0      0 192.168.175.88:50806    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 127.0.0.1:31000         127.0.0.1:32000         ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:51560    192.168.175.101:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50810    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50818    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50814    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50812    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50804    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50808    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50802    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50820    192.168.175.100:3306    ESTABLISHED 1374/java
        tcp6       0      0 192.168.175.88:50816    192.168.175.100:3306    ESTABLISHED 1374/java


// 查看一下 其 日志目录 下的 内容
[root@mycatserver ~]# ls /app/mycat/logs/
        mycat.log  mycat.pid  wrapper.log
      其中 wrapper.log 是 启动过程日志, mycat.log 是 运行过程日志, 另外还可在 conf/log4j2.xml 中调整日志 level

---------------------------------------------------------------------------------------------------
测试 test:

// 先查看一下  index_to_charset.properties 中的 index 为 33 和 45 时的对应值
[root@mycatserver ~]# grep -E '^(33|45)=' /app/mycat/conf/index_to_charset.properties
      33=utf8
      45=utf8mb4


// 随便找台 安装了 mysql client 客户端程序 测试( 只要有权限访问即可 ):
[root@dbserver ~]# mysql -h 192.168.175.88 -u mycatuser -p -P 8066  --default-character-set=utf8mb4

                      Enter password:    # <------ 键入 mycatuser 的密码
                      Welcome to the MySQL monitor.  Commands end with ; or \g.
                      Your MySQL connection id is 3
                      Server version: 5.6.29-mycat-1.6.7.1-release-20190627191042 MyCat Server (OpenCloudDB)

                      Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

                      Oracle is a registered trademark of Oracle Corporation and/or its
                      affiliates. Other names may be trademarks of their respective
                      owners.

                      Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

                      mysql> status;    # <------------- 查看状态
                      --------------
                      mysql  Ver 14.14 Distrib 5.7.26, for Linux (x86_64) using  EditLine wrapper

                      Connection id:          3
                      Current database:       jiaowu
                      Current user:           admin@192.168.175.88
                      SSL:                    Not in use
                      Current pager:          stdout
                      Using outfile:          ''
                      Using delimiter:        ;
                      Server version:         5.6.29-mycat-1.6.7.1-release-20190627191042 MyCat Server (OpenCloudDB)
                      Protocol version:       10
                      Connection:             192.168.175.88 via TCP/IP
                      Server characterset:    utf8mb4
                      Db     characterset:    utf8mb4
                      Client characterset:    utf8mb4
                      Conn.  characterset:    utf8mb4
                      TCP port:               8066
                      --------------

                      mysql> show databases;  # <----------- 查看 database
                      +----------+
                      | DATABASE |
                      +----------+
                      | jiaowu   |
                      +----------+
                      1 row in set (0.00 sec)



[root@dbserver ~]# mysql -h 192.168.175.88 -u mycatuser -p -P 9066 --default-character-set=utf8mb4
    Enter password:
    Welcome to the MySQL monitor.  Commands end with ; or \g.
    Your MySQL connection id is 8
    Server version: 5.6.29-mycat-1.6.7.1-release-20190627191042 MyCat Server (monitor)

    Copyright (c) 2000, 2019, Oracle and/or its affiliates. All rights reserved.

    Oracle is a registered trademark of Oracle Corporation and/or its
    affiliates. Other names may be trademarks of their respective
    owners.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    mysql> show @@backend;
    +------------+------+---------+-----------------+------+--------+--------+---------+------+--------+----------+------------+--------+---------+---------+------------+
    | processor  | id   | mysqlId | host            | port | l_port | net_in | net_out | life | closed | borrowed | SEND_QUEUE | schema | charset | txlevel | autocommit |
    +------------+------+---------+-----------------+------+--------+--------+---------+------+--------+----------+------------+--------+---------+---------+------------+
    | Processor0 |    1 |       7 | 192.168.175.100 | 3306 |  52460 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    2 |       5 | 192.168.175.100 | 3306 |  52446 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    3 |       9 | 192.168.175.100 | 3306 |  52452 |    573 |     178 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    4 |       8 | 192.168.175.100 | 3306 |  52450 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    5 |       6 | 192.168.175.100 | 3306 |  52458 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    6 |      12 | 192.168.175.100 | 3306 |  52448 |    573 |     178 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    7 |      10 | 192.168.175.100 | 3306 |  52454 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    8 |       4 | 192.168.175.100 | 3306 |  52444 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |    9 |      11 | 192.168.175.100 | 3306 |  52456 |    653 |     196 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |   10 |      13 | 192.168.175.100 | 3306 |  52462 |    573 |     178 |  669 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    | Processor0 |   11 |       4 | 192.168.175.101 | 3306 |  35600 |   5833 |    1434 |  666 | false  | false    |          0 | jiaowu | utf8:45 | 3       | true       |
    +------------+------+---------+-----------------+------+--------+--------+---------+------+--------+----------+------------+--------+---------+---------+------------+
    11 rows in set (0.00 sec)

    mysql> show @@connection;
    +------------+------+----------------+------+------------+-----------+--------+---------+--------+---------+---------------+-------------+------------+---------+------------+
    | PROCESSOR  | ID   | HOST           | PORT | LOCAL_PORT | USER      | SCHEMA | CHARSET | NET_IN | NET_OUT | ALIVE_TIME(S) | RECV_BUFFER | SEND_QUEUE | txlevel | autocommit |
    +------------+------+----------------+------+------------+-----------+--------+---------+--------+---------+---------------+-------------+------------+---------+------------+
    | Processor0 |    8 | 192.168.175.40 | 9066 |      58646 | mycatuser | NULL   | utf8:45 |    167 |    1803 |            18 |        4096 |          0 |         |            |
    +------------+------+----------------+------+------------+-----------+--------+---------+--------+---------+---------------+-------------+------------+---------+------------+
    1 row in set (0.00 sec)

    mysql> show @@heartbeat;
    +--------+-------+-----------------+------+---------+-------+--------+---------+--------------+---------------------+-------+
    | NAME   | TYPE  | HOST            | PORT | RS_CODE | RETRY | STATUS | TIMEOUT | EXECUTE_TIME | LAST_ACTIVE_TIME    | STOP  |
    +--------+-------+-----------------+------+---------+-------+--------+---------+--------------+---------------------+-------+
    | hostM1 | mysql | 192.168.175.100 | 3306 |       1 |     0 | idle   |   30000 | 1,1,1        | 2019-07-13 08:52:33 | false |
    | hostS1 | mysql | 192.168.175.101 | 3306 |       1 |     0 | idle   |   30000 | 1,1,2        | 2019-07-13 08:52:33 | false |
    +--------+-------+-----------------+------+---------+-------+--------+---------+--------------+---------------------+-------+
    2 rows in set (0.00 sec)






---------------------------------------------------------------------------------------------------
其他:

// 停止 mycat 的命令:
[root@mycatserver ~]# su - mycat -s /bin/bash -c 'cd /app/mycat/bin/  && ./mycat stop'


---------------------------------------------------------------------------------------------------
mycat 开机自启的设置:

---------
// 方式01: 修改文件 /etc/rc.d/rc.local
[root@mycatserver ~]# vim /etc/rc.d/rc.local
        su - mycat -s /bin/bash -c 'cd /app/mycat/bin/  && ./mycat start'

[root@mycatserver ~]# chmod +x /etc/rc.d/rc.local


---------
// 方式02

// 创建 mycat 的 init script, 参考了 less /app/mycat/bin/mycat 中 chkconfig 设置
[root@mycatserver ~]# vim /etc/init.d/mycat

                #!/bin/bash

                # chkconfig: 2345 20 80
                # description:  Mycat-server init script of myself

                case "$1" in
                  'console'|'start'|'stop'|'restart'|'status'|'dump')
                    command_line="cd /app/mycat/bin/  && ./mycat $@"
                    # 注: 如下语句 执行 $command_line 表示的命令时, 会自动读取 /etc/profile, 所以不用重复设置如 JAVA_HOME 之类的环境变量
                    su - mycat -s /bin/bash -c "$command_line"
                    exit $?
                    ;;
                esac

                echo "Usage: $0 { console | start | stop | restart | status | dump }"
                exit 1



[root@mycatserver ~]# chmod 755 /etc/init.d/mycat
[root@mycatserver ~]# chkconfig --add mycat
[root@mycatserver ~]# chkconfig --list mycat

Note: This output shows SysV services only and does not include native
      systemd services. SysV configuration data might be overridden by native
      systemd configuration.

      If you want to list systemd services use 'systemctl list-unit-files'.
      To see services enabled on particular target use
      'systemctl list-dependencies [target]'.

mycat           0:off   1:off   2:on    3:on    4:on    5:on    6:off

// 查看 对应 directory 所发生的变量
[root@mycatserver ~]# find /etc/rc* | grep mycat
          /etc/rc.d/init.d/mycat
          /etc/rc.d/rc0.d/K80mycat
          /etc/rc.d/rc1.d/K80mycat
          /etc/rc.d/rc2.d/S20mycat
          /etc/rc.d/rc3.d/S20mycat
          /etc/rc.d/rc4.d/S20mycat
          /etc/rc.d/rc5.d/S20mycat
          /etc/rc.d/rc6.d/K80mycat

---------
方式03:

[root@mycatserver ~]# touch /etc/systemd/system/mycat.service
[root@mycatserver ~]# chmod 664 /etc/systemd/system/mycat.service
[root@mycatserver ~]# vim /etc/systemd/system/mycat.service

          [Unit]
          Description=Mycat-server
          After=network.target
          After=syslog.target

          [Service]
          User=mycat
          Group=mycat

          Type=forking
          ExecStart=/bin/bash -l -c 'cd /app/mycat/bin/  && ./mycat start'
          ExecStop=/bin/bash -l -c 'cd /app/mycat/bin/  && ./mycat stop'

          [Install]
          WantedBy=multi-user.target

[root@mycatserver ~]# systemctl daemon-reload
[root@mycatserver ~]# systemctl start mycat.service
[root@mycatserver ~]# systemctl enable mycat.service
        Created symlink from /etc/systemd/system/multi-user.target.wants/mycat.service to /etc/systemd/system/mycat.service.

---------


---------------------------------------------------------------------------------------------------
网上资料:

mycat 9066管理端口 常用命令
      https://www.cnblogs.com/parryyang/p/5606071.html


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

---------------------------------------------------------------------------------------------------



