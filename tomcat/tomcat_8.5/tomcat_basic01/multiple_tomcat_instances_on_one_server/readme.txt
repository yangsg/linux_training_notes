https://dzone.com/articles/running-multiple-tomcat
http://kief.com/configuring-the-tomcat-manager-webapp.html
https://dzone.com/articles/run-configure-multiple-instance-in-a-single-tomcat
https://crunchify.com/how-to-run-multiple-tomcat-instances-on-one-server/
https://tomcat.apache.org/tomcat-8.5-doc/RUNNING.txt  或 less /app/apache-tomcat-8.5.39/RUNNING.txt

https://blog.csdn.net/mqf163/article/details/52953499
https://blog.csdn.net/a503921892/article/details/39048889
https://www.cnblogs.com/mafly/p/tomcat.html

https://www.cnblogs.com/cxzdy/p/5388509.html
Java虚拟机（JVM）体系结构概述及各种性能参数优化总结


https://tomcat.apache.org/tomcat-8.5-doc/
https://tomcat.apache.org/tomcat-8.5-doc/architecture/overview.html

//TODO: 修改为使用普通账号运行tomcat服务

[root@tomcat85server ~]# mkdir -pv /app/tomcat_multi_instances/{tomcat01,tomcat02}/{bin,conf,lib,logs,webapps,work,temp}

// http://tomcat.apache.org/tomcat-8.5-doc/introduction.html
// 实际生产环境中， 最好将 CATALINA_HOME/conf 下的所有内容copy到 CATALINA_BASE/conf/
// 原文:
//     We also recommend you copy all configuration files from the CATALINA_HOME/conf directory into the CATALINA_BASE/conf/
//     directory. In case a configuration file is missing in CATALINA_BASE, there is no fallback to CATALINA_HOME. Consequently, this may cause failure.
//
// At minimum, CATALINA_BASE must contain: conf/server.xml  conf/web.xml

[root@tomcat85server ~]# cp -a /app/apache-tomcat-8.5.39/conf/{server.xml,web.xml} /app/tomcat_multi_instances/tomcat01/conf/
[root@tomcat85server ~]# cp -a /app/apache-tomcat-8.5.39/conf/{server.xml,web.xml} /app/tomcat_multi_instances/tomcat02/conf/

// 编辑如下基础的端口号
[root@tomcat85server ~]# vim /app/tomcat_multi_instances/tomcat01/conf/server.xml

 <!-- server的port 8105 只会绑定在ip: 127.0.0.1 上 -->
 <Server port="8105" shutdown="SHUTDOWN">

     <Connector port="8180" protocol="HTTP/1.1"
                connectionTimeout="20000"
                redirectPort="8143" />

      <!-- 如果没有httpd 通过 ajp 协议访问 tomcat, 该 ajp connector 可以通过注释或删除来禁用 -->
      <Connector port="8109" protocol="AJP/1.3" redirectPort="8143" />


// 按相同的套路修改 tomcat02 实例 的 server.xml 配置文件
[root@tomcat85server ~]# vim /app/tomcat_multi_instances/tomcat02/conf/server.xml

  <Server port="8205" shutdown="SHUTDOWN">

    <Connector port="8280" protocol="HTTP/1.1"
               connectionTimeout="20000"
               redirectPort="8243" />

    <Connector port="8209" protocol="AJP/1.3" redirectPort="8243" />


// TODO: 该脚本有待完善
[root@tomcat85server ~]# vim /app/tomcat_multi_instances/tomcat01/tomcat.sh
      #!/bin/bash

      export CATALINA_HOME=/app/apache-tomcat-8.5.39
      export CATALINA_BASE=/app/tomcat_multi_instances/tomcat01

      case $1 in
      start)
        $CATALINA_HOME/bin/startup.sh
        ;;
      stop)
        $CATALINA_HOME/bin/shutdown.sh
        ;;
      restart)
        $CATALINA_HOME/bin/shutdown.sh
        sleep 3
        $CATALINA_HOME/bin/startup.sh
        ;;
      esac


[root@tomcat85server ~]# vim /app/tomcat_multi_instances/tomcat02/tomcat.sh
      #!/bin/bash

      export CATALINA_HOME=/app/apache-tomcat-8.5.39
      export CATALINA_BASE=/app/tomcat_multi_instances/tomcat02

      case $1 in
      start)
        $CATALINA_HOME/bin/startup.sh
        ;;
      stop)
        $CATALINA_HOME/bin/shutdown.sh
        ;;
      restart)
        $CATALINA_HOME/bin/shutdown.sh
        sleep 3
        $CATALINA_HOME/bin/startup.sh
        ;;
      esac

[root@tomcat85server ~]# chmod a+x /app/tomcat_multi_instances/tomcat01/tomcat.sh
[root@tomcat85server ~]# chmod a+x /app/tomcat_multi_instances/tomcat02/tomcat.sh

[root@tomcat85server ~]# mkdir /app/tomcat_multi_instances/tomcat01/webapps/ROOT
[root@tomcat85server ~]# mkdir /app/tomcat_multi_instances/tomcat02/webapps/ROOT

[root@tomcat85server ~]# echo '<h1>tomcat01 instance</h1>' > /app/tomcat_multi_instances/tomcat01/webapps/ROOT/index.jsp
[root@tomcat85server ~]# echo '<h1>tomcat02 instance</h1>' > /app/tomcat_multi_instances/tomcat02/webapps/ROOT/index.jsp


[root@tomcat85server ~]# tree /app/tomcat_multi_instances/tomcat01/
          /app/tomcat_multi_instances/tomcat01/
          ├── bin
          ├── conf
          │   ├── Catalina
          │   │   └── localhost
          │   ├── server.xml
          │   └── web.xml
          ├── lib
          ├── logs
          ├── temp
          ├── tomcat.sh
          ├── webapps
          │   └── ROOT
          │       └── index.jsp
          └── work


[root@tomcat85server ~]# /app/tomcat_multi_instances/tomcat01/tomcat.sh start
[root@tomcat85server ~]# /app/tomcat_multi_instances/tomcat02/tomcat.sh start

[root@tomcat85server ~]# netstat -anptu | grep java
      tcp6       0      0 127.0.0.1:8205          :::*                    LISTEN      4413/java
      tcp6       0      0 :::8109                 :::*                    LISTEN      4362/java
      tcp6       0      0 :::8209                 :::*                    LISTEN      4413/java
      tcp6       0      0 :::8180                 :::*                    LISTEN      4362/java
      tcp6       0      0 :::8280                 :::*                    LISTEN      4413/java
      tcp6       0      0 127.0.0.1:8105          :::*                    LISTEN      4362/java


// 浏览器访问： http://192.168.175.10:8180/
[root@tomcat85server ~]# tree /app/tomcat_multi_instances/tomcat01/
      /app/tomcat_multi_instances/tomcat01/
      ├── bin
      ├── conf
      │   ├── Catalina
      │   │   └── localhost
      │   ├── server.xml
      │   └── web.xml
      ├── lib
      ├── logs
      │   ├── catalina.out
      │   └── localhost_access_log.2019-04-06.txt
      ├── temp
      ├── tomcat.sh
      ├── webapps
      │   └── ROOT
      │       └── index.jsp
      └── work
          └── Catalina
              └── localhost
                  └── ROOT
                      └── org
                          └── apache
                              └── jsp
                                  ├── index_jsp.class
                                  └── index_jsp.java



// 浏览器访问： http://192.168.175.10:8280/
[root@tomcat85server ~]# tree /app/tomcat_multi_instances/tomcat02/
      /app/tomcat_multi_instances/tomcat02/
      ├── bin
      ├── conf
      │   ├── Catalina
      │   │   └── localhost
      │   ├── server.xml
      │   └── web.xml
      ├── lib
      ├── logs
      │   ├── catalina.out
      │   └── localhost_access_log.2019-04-06.txt
      ├── temp
      ├── tomcat.sh
      ├── webapps
      │   └── ROOT
      │       └── index.jsp
      └── work
          └── Catalina
              └── localhost
                  └── ROOT
                      └── org
                          └── apache
                              └── jsp
                                  ├── index_jsp.class
                                  └── index_jsp.java




// 其他： 如果存在 $CATALINA_BASE/bin/setenv.sh,
// 则tomcat对读取并执行 $CATALINA_BASE/bin/setenv.sh 而不会使用 $CATALINA_HOME/bin/setenv.sh
// 如果要自定义 $CATALINA_BASE/bin/setenv.sh, 又想使用 $CATALINA_HOME/bin/setenv.sh 中默认的配置，
// 可以按如下方式使用setenv.sh：
// 假设 $CATALINA_HOME/bin/setenv.sh 已有内容如下：
[root@tomcat85server ~]# cat /app/apache-tomcat-8.5.39/bin/setenv.sh
      LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CATALINA_HOME/lib
      export LD_LIBRARY_PATH

// 创建 $CATALINA_BASE/bin/setenv.sh 文件
[root@tomcat85server ~]# vim /app/tomcat_multi_instances/tomcat01/bin/setenv.sh
    source $CATALINA_HOME/bin/setenv.sh

[root@tomcat85server ~]# vim /app/tomcat_multi_instances/tomcat02/bin/setenv.sh
    source $CATALINA_HOME/bin/setenv.sh

// https://github.com/yangsg/linux_training_notes/blob/master/tomcat/tomcat_8.5/tomcat_basic01/multiple_tomcat_instances_on_one_server/tomcat85server/app/tomcat_multi_instances/tomcat01/bin/setenv.sh










