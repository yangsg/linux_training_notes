


https://en.wikipedia.org/wiki/NoSQL

    NoSQL: non SQL 或 Not only SQL


https://redis.io/
https://redis.io/topics/introduction
https://github.com/antirez/redis-doc


https://github.com/ran-jit/tomcat-cluster-redis-session-manager
https://blog.51cto.com/13447608/2295799


一些 redis 的中文网:
      https://www.runoob.com/redis/redis-tutorial.html
      http://doc.redisfans.com/
      http://redisdoc.com/index.html
      http://www.redis.cn/




对于将 redis (master, slave 和 sentinel) 部署到 容器或使用的 ip 或 port remapping技术的环境中,
需要额外注意一些问题, 详细见

      Sentinel, Docker, NAT, and possible issues
          https://redis.io/topics/sentinel



注: 指令 slaveof 从 Redis 5 版本开始被废弃(Deprecated), 取而代之应该使用 replicaof


----------------------------------------------------------------------------------------------------
Redis数据库

    redis: REmote DIctionary Server

  数据库类型：

    关系型数据库
      MySQL, Oracle, SQL Server, postgresql, db2
      以表的形式存储结构化数据
      作用：
        业务数据持久化存储


    非关系型数据库   NoSQL   Not Only SQL
      以key-value键值对的方式存储非结构化数据
      memcached, mongoDB, redis, HBase
      作用：
        1) 缓存服务器
        2) 消息队列服务器， MQ， Messsage Queue   开发

          ZeroMQ
          RabbitMQ


Redis特性：

    开源数据库
    配置简单
    支持内存存储数据
    支持持久化存储数据
      datafile 数据文件   *.rdb
      aof(append only file)文件，日志文件
    支持多实例部署
    支持主从复制、分片集群、哨兵集群
    支持事务transaction
    以key-value键值对的方式存储
      value类型：string字符串、list列表、set集合、sorted_set有序集合、hash值




----------------------------------------------------------------------------------------------------
redis 的 安装 及 启动


// 构建基本的编译环境
[root@redis_server ~]# yum -y install gcc gcc-c++ autoconf automake

[root@redis_server ~]# mkdir /app

[root@redis_server ~]# mkdir download
[root@redis_server ~]# cd download/
[root@redis_server download]# wget http://download.redis.io/releases/redis-5.0.5.tar.gz

[root@redis_server download]# ls
      redis-5.0.5.tar.gz

[root@redis_server download]# tar -xvf redis-5.0.5.tar.gz
[root@redis_server download]# cd redis-5.0.5/
[root@redis_server redis-5.0.5]# ls   #发现已经存在 Makefile 文件, 所有无需执行 configure 命令了
            00-RELEASENOTES  CONTRIBUTING  deps     Makefile   README.md   runtest          runtest-moduleapi  sentinel.conf  tests
            BUGS             COPYING       INSTALL  MANIFESTO  redis.conf  runtest-cluster  runtest-sentinel   src            utils

[root@redis_server redis-5.0.5]# make
[root@redis_server redis-5.0.5]# make PREFIX=/app/redis install


[root@redis_server redis-5.0.5]# tree /app/redis/
      /app/redis/
      └── bin
          ├── redis-benchmark                 #redis性能测试
          ├── redis-check-aof                 #检测aof日志文件
          ├── redis-check-rdb                 #检测rdb文件
          ├── redis-cli                       #redis客户端工具
          ├── redis-sentinel -> redis-server
          └── redis-server                    #启动redis服务


[root@redis_server ~]# mkdir /app/redis/conf
[root@redis_server ~]# cp ~/download/redis-5.0.5/redis.conf /app/redis/conf/
[root@redis_server ~]# /app/redis/bin/redis-server /app/redis/conf/redis.conf &

  注意下面 3 个警告:
        5908:M 12 Sep 2019 11:12:40.678 # WARNING: The TCP backlog setting of 511 cannot be enforced because /proc/sys/net/core/somaxconn is set to the lower value of 128.
        5908:M 12 Sep 2019 11:12:40.678 # Server initialized
        5908:M 12 Sep 2019 11:12:40.678 # WARNING overcommit_memory is set to 0! Background save may fail under low memory condition. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
        5908:M 12 Sep 2019 11:12:40.678 # WARNING you have Transparent Huge Pages (THP) support enabled in your kernel. This will create latency and memory usage issues with Redis. To fix this issue run the command 'echo never > /sys/kernel/mm/transparent_hugepage/enabled' as root, and add it to your /etc/rc.local in order to retain the setting after a reboot. Redis must be restarted after THP is disabled.
        5908:M 12 Sep 2019 11:12:40.678 * Ready to accept connections


// 根据提示信息 解决 上面 3 个警告:
// 先查看一下 一些 内核参数
[root@redis_server ~]# sysctl -a | grep -Ein 'somaxconn|overcommit_memory|transparent_hugepage'
      235:net.core.somaxconn = 128   <-------观察
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"
      742:vm.overcommit_memory = 0  <--------观察


[root@redis_server ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

[root@redis_server ~]# sysctl -p
      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

[root@redis_server ~]# echo never > /sys/kernel/mm/transparent_hugepage/enabled
[root@redis_server ~]# vim /etc/rc.d/rc.local
    echo never > /sys/kernel/mm/transparent_hugepage/enabled

[root@redis_server ~]# chmod +x /etc/rc.d/rc.local

// 查看验证
[root@redis_server ~]# cat /proc/sys/net/core/somaxconn
    1024
[root@redis_server ~]# cat /proc/sys/vm/overcommit_memory
    1
[root@redis_server ~]# cat /sys/kernel/mm/transparent_hugepage/enabled
    always madvise [never]


// 重启 redis 服务
[root@redis_server ~]# /app/redis/bin/redis-cli shutdown

[root@redis_server ~]# vim /etc/profile
    export PATH=$PATH:/app/redis/bin

[root@redis_server ~]# source /etc/profile

[root@redis_server ~]# redis-server /app/redis/conf/redis.conf &



// 设置 redis 开机自启
[root@redis_server ~]# vim /etc/rc.d/rc.local
    echo never > /sys/kernel/mm/transparent_hugepage/enabled
    #注: redis 服务的启动一定要放在 transparent_hugepage 被禁用之后
    /app/redis/bin/redis-server  /app/redis/conf/redis.conf &


----------------------------------------------------------------------------------------------------

Redis安全设置:

1) 设置密码
[root@redis_server ~]# vim /app/redis/conf/redis.conf
      requirepass redhat

// 重新启动 redis
[root@redis_server ~]# redis-cli shutdown
[root@redis_server ~]# redis-server /app/redis/conf/redis.conf &

[root@redis_server ~]# redis-cli

    127.0.0.1:6379> auth redhat   <====验证密码 password
    OK
    127.0.0.1:6379> set name tom
    OK
    127.0.0.1:6379> get name
    "tom"
    127.0.0.1:6379> exit















































