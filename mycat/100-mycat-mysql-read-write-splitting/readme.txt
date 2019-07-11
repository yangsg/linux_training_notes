

// 安装 jdk (因 mycat 由 java 实现, 且 至少 jdk7)




// 下载 mycat
[root@mycatserver ~]# mkdir download && cd download
[root@mycatserver download]# wget http://dl.mycat.io/1.6.7.1/Mycat-server-1.6.7.1-release-20190627191042-linux.tar.gz

// 查看 以准备的 软件包
[root@mycatserver download]# tree
      .
      ├── jdk-8u202-linux-x64.tar.gz
      └── Mycat-server-1.6.7.1-release-20190627191042-linux.tar.gz

---------------------------------------------------------------------------------------------------
// 安装 jdk

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


// 查看一些 conf 目录
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
        <!-- 删除多余的 <user> 标签, 值保留修改需要的 user 配置 -->
        <user name="mycatuser">
                <property name="password">1234</property>
                <property name="schemas">jiaowu</property>
        </user>


[root@mycatserver ~]# useradd -s /sbin/nologin mycat
[root@mycatserver ~]# chown -R mycat:mycat /app/mycat/
[root@mycatserver ~]# chmod -R go-rwx /app/mycat/

[root@mycatserver ~]# su - mycat -s /bin/bash -c 'cd /app/mycat/bin/  && ./mycat start'
[root@mycatserver ~]# su - mycat -s /bin/bash -c 'cd /app/mycat/bin/  && ./mycat stop'






mysql> create user 'admin'@'192.168.175.88' identified by 'WWW.1.com';
mysql> grant all on jiaowu.* to 'admin'@'192.168.175.88';








[root@dbserver ~]# mysql -h 192.168.175.88 -u mycatuser -p   -P 8066




mysql> create database jiaowu default charset utf8;


---------------------------------------------------------------------------------------------------
mycat 开机自己的设置:

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
方式3:

[root@mycatserver ~]# touch /etc/systemd/system/mycat.service
[root@mycatserver ~]# chmod 664 /etc/systemd/system/mycat.service

---------





