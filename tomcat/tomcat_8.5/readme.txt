

http://tomcat.apache.org/
http://tomcat.apache.org/whichversion.html

http://tomcat.apache.org/migration-85.html


# apache-tomcat-8.5.39.tar.gz中已包含 tomcat-native.tar.gz, 所以不用单独下载了， 参考 http://tomcat.apache.org/tomcat-8.5-doc/apr.html



// 将下载好的相关文件放到 ~/download 目录下, 如下：
[root@tomcat85server ~]# tree download/
download/
├── apache-tomcat-8.5.39.tar.gz
├── jdk-8u202-linux-x64.tar.gz
└── tomcat-native-1.2.21-src.tar.gz # apache-tomcat-8.5.39.tar.gz中已包含 tomcat-native.tar.gz, 所以不用单独下载了， 参考 http://tomcat.apache.org/tomcat-8.5-doc/apr.html


// 安装 oracle 的 java jdk
[root@tomcat85server ~]# cd download/
[root@tomcat85server download]# mkdir /app
[root@tomcat85server download]# tar -xvf jdk-8u202-linux-x64.tar.gz -C /app
[root@tomcat85server download]# ls /app/
    jdk1.8.0_202

[root@tomcat85server download]# vim /etc/profile
      # tomcat需要 JAVA_HOME 这样的环境变量
      export JAVA_HOME=/app/jdk1.8.0_202
      export PATH=$PATH:$JAVA_HOME/bin

[root@tomcat85server download]# source /etc/profile
[root@tomcat85server download]# java -version

    java version "1.8.0_202"
    Java(TM) SE Runtime Environment (build 1.8.0_202-b08)
    Java HotSpot(TM) 64-Bit Server VM (build 25.202-b08, mixed mode)



// 安装 tomcat-8.5.39
// 参考： https://tomcat.apache.org/tomcat-8.5-doc/RUNNING.txt  或 less /app/apache-tomcat-8.5.39/RUNNING.txt
// 注：除了 CATALINA_HOME and CATALINA_BASE 之外，所有其他环境变量都可以在 $CATALINA_HOME/bin/setenv.sh 中设置

[root@tomcat85server download]# tar -xvf apache-tomcat-8.5.39.tar.gz -C /app/
[root@tomcat85server download]# ls /app/
      apache-tomcat-8.5.39  jdk1.8.0_202

[root@tomcat85server download]# vim /etc/profile
        # 类似tomcat的一些启动脚本会使用 CATALINA_HOME 环境变量
        export CATALINA_HOME=/app/apache-tomcat-8.5.39

// 启动 tomcat 服务  (参考 less /app/apache-tomcat-8.5.39/RUNNING.txt 帮助文档 )
[root@tomcat85server ~]# $CATALINA_HOME/bin/startup.sh      #或 $CATALINA_HOME/bin/catalina.sh start

[root@tomcat85server ~]# netstat -anptu | grep java
    tcp6       0      0 :::8080                 :::*                    LISTEN      17067/java
    tcp6       0      0 127.0.0.1:8005          :::*                    LISTEN      17067/java
    tcp6       0      0 :::8009                 :::*                    LISTEN      17067/java


// 停止 tomcat 服务
[root@tomcat85server ~]# $CATALINA_HOME/bin/shutdown.sh     #或 $CATALINA_HOME/bin/catalina.sh stop





// 安装可选的组件 Apache Tomcat Native Library (如果不想安装此可选组件，可直接跳过, 不过生产环境建议安装)
//     http://tomcat.apache.org/native-doc/
//     http://tomcat.apache.org/download-native.cgi
Apache Tomcat Native Library 是一个允许tomcat 使用特定本地资源用于优化和兼容的可选组件,
Specifically, the Apache Tomcat Native Library gives Tomcat access to the Apache Portable Runtime
(APR) library's network connection (socket) implementation and random-number generator.
See the Apache Tomcat documentation for more information on how to configure Tomcat to use the APR connector.

Features of the APR connector:

    - Non-blocking I/O for Keep-Alive requests (between requests)
    - Uses OpenSSL for TLS/SSL capabilities (if supported by linked APR library)
    - FIPS 140-2 support for TLS/SSL (if supported by linked OpenSSL library)


// 安装 tc-native 的依赖组件 (centos上 tc-native 依赖apr-devel openssl-devel,
// 但yum仓库中apr-devel版本比较旧，所以待会直接编译安装apr)
[root@tomcat85server ~]# yum -y install openssl-devel

// 安装基础编译构建环境
[root@tomcat85server ~]# yum -y install gcc gcc-c++ autoconf automake

[root@tomcat85server download]# wget http://mirrors.shu.edu.cn/apache/apr/apr-1.6.5.tar.gz

[root@tomcat85server download]# tar -xvf apr-1.6.5.tar.gz
[root@tomcat85server download]# cd apr-1.6.5/


[root@tomcat85server apr-1.6.5]# ./configure --prefix=/app/apr-1.6.5
[root@tomcat85server apr-1.6.5]# make
[root@tomcat85server apr-1.6.5]# make install
[root@tomcat85server apr-1.6.5]# ls /app/
    apache-tomcat-8.5.39  apr-1.6.5  jdk1.8.0_202

[root@tomcat85server ~]# cd /app/apache-tomcat-8.5.39/bin/
[root@tomcat85server bin]# tar -xvf tomcat-native.tar.gz
[root@tomcat85server bin]# cd tomcat-native-1.2.21-src/native/

[root@tomcat85server native]# ./configure --help   #参考 http://tomcat.apache.org/native-doc/
[root@tomcat85server native]# ./configure --with-apr=/app/apr-1.6.5/bin/apr-1-config \
            --with-java-home=/app/jdk1.8.0_202/ \
            --with-ssl=yes \
            --prefix=/app/apache-tomcat-8.5.39

[root@tomcat85server native]# make
[root@tomcat85server native]# make install

[root@tomcat85server native]# ls /app/apache-tomcat-8.5.39/lib | grep native
      libtcnative-1.a
      libtcnative-1.la
      libtcnative-1.so       <-----
      libtcnative-1.so.0
      libtcnative-1.so.0.2.21


// 此处如果 setenv.sh 不存在，则直接新建即可, 更多详细信息，见 less /app/apache-tomcat-8.5.39/RUNNING.txt
[root@tomcat85server ~]# vim /app/apache-tomcat-8.5.39/bin/setenv.sh

    LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CATALINA_HOME/lib
    export LD_LIBRARY_PATH



[root@tomcat85server ~]# source  /etc/profile

// 启动 tomcat 服务
[root@tomcat85server ~]# $CATALINA_HOME/bin/startup.sh
      Using CATALINA_BASE:   /app/apache-tomcat-8.5.39
      Using CATALINA_HOME:   /app/apache-tomcat-8.5.39
      Using CATALINA_TMPDIR: /app/apache-tomcat-8.5.39/temp
      Using JRE_HOME:        /app/jdk1.8.0_202
      Using CLASSPATH:       /app/apache-tomcat-8.5.39/bin/bootstrap.jar:/app/apache-tomcat-8.5.39/bin/tomcat-juli.jar
      Tomcat started.




// 如下是输出的部分日志信息
[root@tomcat85server ~]# tail -f /app/apache-tomcat-8.5.39/logs/catalina.2019-04-05.log   #该命令在启动之前执行可用于观察启动日志

      05-Apr-2019 13:19:02.808 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log OS Version:            3.10.0-693.el7.x86_64
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Architecture:          amd64
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Java Home:             /app/jdk1.8.0_202/jre
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Version:           1.8.0_202-b08
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log JVM Vendor:            Oracle Corporation
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_BASE:         /app/apache-tomcat-8.5.39
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log CATALINA_HOME:         /app/apache-tomcat-8.5.39
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.config.file=/app/apache-tomcat-8.5.39/conf/logging.properties
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djdk.tls.ephemeralDHKeySize=2048
      05-Apr-2019 13:19:02.809 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.protocol.handler.pkgs=org.apache.catalina.webresources
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dorg.apache.catalina.security.SecurityListener.UMASK=0027
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dignore.endorsed.dirs=
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.base=/app/apache-tomcat-8.5.39
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Dcatalina.home=/app/apache-tomcat-8.5.39
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.startup.VersionLoggerListener.log Command line argument: -Djava.io.tmpdir=/app/apache-tomcat-8.5.39/temp
      // ---------------------------------此处观察 tomcat native 相关信息-----------------------------------
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent Loaded APR based Apache Tomcat Native library [1.2.21] using APR version [1.6.5].
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR capabilities: IPv6 [true], sendfile [true], accept filters [false], random [true].
      05-Apr-2019 13:19:02.810 INFO [main] org.apache.catalina.core.AprLifecycleListener.lifecycleEvent APR/OpenSSL configuration: useAprConnector [false], useOpenSSL [true]
      05-Apr-2019 13:19:02.817 INFO [main] org.apache.catalina.core.AprLifecycleListener.initializeSSL OpenSSL successfully initialized [OpenSSL 1.0.2k-fips  26 Jan 2017]
      05-Apr-2019 13:19:03.159 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["http-nio-8080"]
      05-Apr-2019 13:19:03.182 INFO [main] org.apache.tomcat.util.net.NioSelectorPool.getSharedSelector Using a shared selector for servlet write/read
      05-Apr-2019 13:19:03.228 INFO [main] org.apache.coyote.AbstractProtocol.init Initializing ProtocolHandler ["ajp-nio-8009"]
      05-Apr-2019 13:19:03.229 INFO [main] org.apache.tomcat.util.net.NioSelectorPool.getSharedSelector Using a shared selector for servlet write/read
      05-Apr-2019 13:19:03.241 INFO [main] org.apache.catalina.startup.Catalina.load Initialization processed in 1348 ms
      05-Apr-2019 13:19:03.293 INFO [main] org.apache.catalina.core.StandardService.startInternal Starting service [Catalina]
      05-Apr-2019 13:19:03.293 INFO [main] org.apache.catalina.core.StandardEngine.startInternal Starting Servlet Engine: Apache Tomcat/8.5.39



// 设置开机自启
[root@tomcat85server ~]# vim /etc/rc.d/rc.local

      export JAVA_HOME=/app/jdk1.8.0_202
      export CATALINA_HOME=/app/apache-tomcat-8.5.39

      $CATALINA_HOME/bin/catalina.sh start

[root@tomcat85server ~]# chmod +x /etc/rc.d/rc.local





其他参考：
http://tomcat.apache.org/tomcat-8.5-doc/apr.html
https://stackoverflow.com/questions/4235171/installing-tomcat-7-on-linux-system-with-native-library
http://www.edwardbeckett.com/tomcat-8-java-8-apache-centos/
https://github.com/yangsg/linux_training_notes/tree/master/httpd/httpd02_install_from_source_code
https://jmchung.github.io/post/centos-installing-apache-portable-runtime-apr-for-tomcat/
http://www.studytrails.com/java/install-apache-tomcat-native/
https://www.howtoforge.com/tutorial/how-to-install-tomcat-on-centos/
https://stackoverflow.com/questions/19216979/ssl-configuration-in-tomcat-and-apr
https://advisor.dbu.edu/docs/apr.html
https://www.cnblogs.com/bigdevilking/p/9497991.html

