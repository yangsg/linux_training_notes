

https://redis.io/topics/sentinel


参考笔记:

    https://github.com/yangsg/linux_training_notes/blob/master/cluster-storage/125-redis/111-high-availability-redis-sentinel/100-redis-sentinel-demo01.draft.txt
    https://github.com/yangsg/linux_training_notes/tree/master/cluster-storage/125-redis/111-high-availability-redis-sentinel

----------------------------------------------------------------------------------------------------


redis_sentinel01: 192.168.175.101:26379   <----采用 sentinel 默认的 tcp 端口 26379, 其用于接收 其他 Sentinel instances 的 connections.
redis_sentinel02: 192.168.175.102:26379
redis_sentinel03: 192.168.175.103:26379

redis_server01: 192.168.175.111:6379  (master)
redis_server02: 192.168.175.112:6379  (slave)

client: 192.168.175.30  <-----用于测试

注: 仅需手动 在 sentinel 上配置 当前 master 的信息,
    而其他信息(如其他 sentinels, slaves) 由 sentinel system
    通过其 auto discovery 机制自动动态配置


----------------------------------------------------------------------------------------------------
在所有节点(即如下主机)上 安装 redis 软件

      redis_sentinel01
      redis_sentinel02
      redis_sentinel03
      redis_server01
      redis_server02
      client

此处以在 redis_server01 上安装  redis 软件为例:

[root@redis_server01 ~]# yum -y install gcc gcc-c++ autoconf automake

[root@redis_server01 ~]# mkdir /app


[root@redis_server01 ~]# mkdir download
[root@redis_server01 ~]# cd download/

[root@redis_server01 download]# wget http://download.redis.io/releases/redis-5.0.5.tar.gz

[root@redis_server01 download]# ls
    redis-5.0.5.tar.gz

[root@redis_server01 download]# tar -xvf redis-5.0.5.tar.gz

[root@redis_server01 download]# ls
      redis-5.0.5  redis-5.0.5.tar.gz

[root@redis_server01 download]# cd redis-5.0.5/

[root@redis_server01 redis-5.0.5]# ls      #发现已经存在 Makefile 文件, 所有无需执行 configure 命令了
      00-RELEASENOTES  CONTRIBUTING  deps     Makefile   README.md   runtest          runtest-moduleapi  sentinel.conf  tests
      BUGS             COPYING       INSTALL  MANIFESTO  redis.conf  runtest-cluster  runtest-sentinel   src            utils

[root@redis_server01 redis-5.0.5]# make
[root@redis_server01 redis-5.0.5]# make PREFIX=/app/redis install

[root@redis_server01 redis-5.0.5]# cd
[root@redis_server01 ~]# vim /etc/profile

        export PATH=$PATH:/app/redis/bin

[root@redis_server01 ~]# source /etc/profile

[root@redis_server01 ~]# which redis-server redis-sentinel redis-cli
    /app/redis/bin/redis-server
    /app/redis/bin/redis-sentinel
    /app/redis/bin/redis-cli


[root@redis_server01 ~]# tree /app/redis/
      /app/redis/
      └── bin
          ├── redis-benchmark                 #redis性能测试
          ├── redis-check-aof                 #检测aof日志文件
          ├── redis-check-rdb                 #检测rdb文件
          ├── redis-cli                       #redis客户端工具
          ├── redis-sentinel -> redis-server
          └── redis-server                    #启动redis服务





----------------------------------------------------------------------------------------------------
准备 redis_server01 作为 master



[root@redis_server01 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

[root@redis_server01 ~]# sysctl -p
    net.core.somaxconn = 1024
    vm.overcommit_memory = 1


[root@redis_server01 ~]# echo never > /sys/kernel/mm/transparent_hugepage/enabled
[root@redis_server01 ~]# vim /etc/rc.d/rc.local
      echo never > /sys/kernel/mm/transparent_hugepage/enabled

[root@redis_server01 ~]# chmod +x /etc/rc.d/rc.local

// 查看验证 如上设置
[root@redis_server01 ~]# cat /proc/sys/net/core/somaxconn
      1024
[root@redis_server01 ~]# cat /proc/sys/vm/overcommit_memory
      1
[root@redis_server01 ~]# cat /sys/kernel/mm/transparent_hugepage/enabled
      always madvise [never]


// 为了提高安全, 创建 redis 账号, 后续会以该 redis 普通账号的身份来启动 redis 相关服务
[root@redis_server01 ~]# useradd -M -s /sbin/nologin redis
[root@redis_server01 ~]# grep redis /etc/passwd
          redis:x:1001:1001::/home/redis:/sbin/nologin


// 创建并保护 数据文件目录
[root@redis_server01 ~]# mkdir /data  #该目录会用于存放 redis 的持久化文件(包括 rdb 和 aof 文件)
[root@redis_server01 ~]# chown redis:redis /data/
[root@redis_server01 ~]# chmod u=rwx,go-rwx /data

// 创建并保护 配置文件目录
[root@redis_server01 ~]# mkdir /app/redis/conf
[root@redis_server01 ~]# chown redis:redis /app/redis/conf/
[root@redis_server01 ~]# chmod u=rwx,go-rwx /app/redis/conf

// 创建并保护 运行时文件目录
[root@redis_server01 ~]# mkdir /var/run/redis/
[root@redis_server01 ~]# chown redis:redis /var/run/redis
[root@redis_server01 ~]# chmod u=rwx,go-rwx /var/run/redis


// 创建并保护 日志文件目录
[root@redis_server01 ~]# mkdir /var/log/redis
[root@redis_server01 ~]# chown redis:redis /var/log/redis/
[root@redis_server01 ~]# chmod u=rwx,go-rwx /var/log/redis


[root@redis_server01 ~]# cp ~/download/redis-5.0.5/redis.conf /app/redis/conf/
[root@redis_server01 ~]# chown -R redis:redis /app/redis/conf/



[root@redis_server01 ~]# vim /app/redis/conf/redis.conf

    bind 192.168.175.111 127.0.0.1
    port 6379
    #https://blog.csdn.net/ccy19910925/article/details/88396480
    #设置 tcp-backlog 时还需要设置或确认内核参数 somaxconn 和 tcp_max_syn_backlog 的值
    tcp-backlog 1024
    # Close the connection after a client is idle for N seconds (0 to disable)
    timeout 10
    daemonize yes
    pidfile /var/run/redis/redis_6379.pid
    logfile "/var/log/redis/redis_6379.log"
    dbfilename redis_db.rdb
    dir /data

    masterauth redhat
    requirepass redhat

    rename-command CONFIG e374fda5-dcf5-41f2-bf69-a5928aa81874--d1e25c85-961d-4e27-ba88-b8ecf7f99c7a

    #设置 maxclients 时, 注意使用命令 `ulimit -n 100032` 和 内核参数 file-max 设置 系统的限制
    maxclients 100000

    #建议为物理内存的 3/5
    maxmemory 614mb
    maxmemory-policy allkeys-lru

    #启用 aof 日志文件
    appendonly yes
    appendfilename "redis_appendonly.aof"


// 临时修改 nofile 的限制
[root@redis_server01 ~]# ulimit -n 100032

// 持久化 设置 nofile 的限制(centos7 中 相对于使用 ulimit 的方式)
[root@redis_server01 ~]# vim /etc/systemd/system.conf
      DefaultLimitNOFILE=100032




[root@redis_server01 ~]# sysctl -a | grep file-max
      fs.file-max = 95856  <------观察
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"



[root@redis_server01 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

      net.ipv4.tcp_max_syn_backlog = 1024

      fs.file-max = 100032


[root@redis_server01 ~]# sysctl -p
      net.core.somaxconn = 1024
      vm.overcommit_memory = 1
      net.ipv4.tcp_max_syn_backlog = 1024
      fs.file-max = 100032




[root@redis_server01 ~]# sysctl -a | grep -E  'somaxconn|overcommit_memory|tcp_max_syn_backlog|file-max'
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"
      fs.file-max = 100032        <-------
      net.core.somaxconn = 1024   <-------
      net.ipv4.tcp_max_syn_backlog = 1024  <-------
      vm.overcommit_memory = 1             <-------







// 启动 redis-server 服务
[root@redis_server01 ~]# su -l redis -s /bin/bash -c 'redis-server /app/redis/conf/redis.conf'
      su: warning: cannot change directory to /home/redis: No such file or directory


// 查看一下 网络端口
[root@redis_server01 ~]# netstat -anptu | grep redis
      tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      21450/redis-server
      tcp        0      0 192.168.175.111:6379    0.0.0.0:*               LISTEN      21450/redis-server


// 查看一下进程
[root@redis_server01 ~]# ps aux | grep redis
      redis     21450  0.1  0.5 163108  5144 ?        Ssl  14:36   0:00 redis-server 192.168.175.111:6379




// 查看一下日志
[root@redis_server01 ~]# cat /var/log/redis/redis_6379.log
        21429:C 22 Sep 2019 14:36:57.297 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
        21429:C 22 Sep 2019 14:36:57.297 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=21429, just started
        21429:C 22 Sep 2019 14:36:57.297 # Configuration loaded
                        _._
                   _.-``__ ''-._
              _.-``    `.  `_.  ''-._           Redis 5.0.5 (00000000/0) 64 bit
          .-`` .-```.  ```\/    _.,_ ''-._
         (    '      ,       .-`  | `,    )     Running in standalone mode
         |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
         |    `-._   `._    /     _.-'    |     PID: 21450
          `-._    `-._  `-./  _.-'    _.-'
         |`-._`-._    `-.__.-'    _.-'_.-'|
         |    `-._`-._        _.-'_.-'    |           http://redis.io
          `-._    `-._`-.__.-'_.-'    _.-'
         |`-._`-._    `-.__.-'    _.-'_.-'|
         |    `-._`-._        _.-'_.-'    |
          `-._    `-._`-.__.-'_.-'    _.-'
              `-._    `-.__.-'    _.-'
                  `-._        _.-'
                      `-.__.-'

        21450:M 22 Sep 2019 14:36:57.306 # Server initialized
        21450:M 22 Sep 2019 14:36:57.306 * Ready to accept connections



// 设置开机自启
[root@redis_server01 ~]# vim /etc/rc.d/rc.local

        echo never > /sys/kernel/mm/transparent_hugepage/enabled
        #注: redis 服务的启动一定要放在 transparent_hugepage 被禁用之后
        su -l redis -s /bin/bash -c 'redis-server /app/redis/conf/redis.conf'














----------------------------------------------------------------------------------------------------
准备 redis_server02 作为 slave



[root@redis_server02 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

[root@redis_server02 ~]# sysctl -p
    net.core.somaxconn = 1024
    vm.overcommit_memory = 1


[root@redis_server02 ~]# echo never > /sys/kernel/mm/transparent_hugepage/enabled
[root@redis_server02 ~]# vim /etc/rc.d/rc.local
      echo never > /sys/kernel/mm/transparent_hugepage/enabled

[root@redis_server02 ~]# chmod +x /etc/rc.d/rc.local

// 查看验证 如上设置
[root@redis_server02 ~]# cat /proc/sys/net/core/somaxconn
      1024
[root@redis_server02 ~]# cat /proc/sys/vm/overcommit_memory
      1
[root@redis_server02 ~]# cat /sys/kernel/mm/transparent_hugepage/enabled
      always madvise [never]


// 为了提高安全, 创建 redis 账号, 后续会以该 redis 普通账号的身份来启动 redis 相关服务
[root@redis_sentinel01 ~]# useradd -M -s /sbin/nologin redis
[root@redis_sentinel01 ~]# grep redis /etc/passwd
          redis:x:1001:1001::/home/redis:/sbin/nologin


// 创建并保护 数据文件目录
[root@redis_server02 ~]# mkdir /data  #该目录会用于存放 redis 的持久化文件(包括 rdb 和 aof 文件)
[root@redis_server02 ~]# chown redis:redis /data/
[root@redis_server02 ~]# chmod u=rwx,go-rwx /data

// 创建并保护 配置文件目录
[root@redis_server02 ~]# mkdir /app/redis/conf
[root@redis_server02 ~]# chown redis:redis /app/redis/conf/
[root@redis_server02 ~]# chmod u=rwx,go-rwx /app/redis/conf

// 创建并保护 运行时文件目录
[root@redis_server02 ~]# mkdir /var/run/redis/
[root@redis_server02 ~]# chown redis:redis /var/run/redis
[root@redis_server02 ~]# chmod u=rwx,go-rwx /var/run/redis


// 创建并保护 日志文件目录
[root@redis_server02 ~]# mkdir /var/log/redis
[root@redis_server02 ~]# chown redis:redis /var/log/redis/
[root@redis_server02 ~]# chmod u=rwx,go-rwx /var/log/redis


[root@redis_server02 ~]# cp ~/download/redis-5.0.5/redis.conf /app/redis/conf/
[root@redis_server02 ~]# chown -R redis:redis /app/redis/conf/



[root@redis_server02 ~]# vim /app/redis/conf/redis.conf

    bind 192.168.175.112 127.0.0.1
    port 6379
    #https://blog.csdn.net/ccy19910925/article/details/88396480
    #设置 tcp-backlog 时还需要设置或确认内核参数 somaxconn 和 tcp_max_syn_backlog 的值
    tcp-backlog 1024
    # Close the connection after a client is idle for N seconds (0 to disable)
    timeout 10
    daemonize yes
    pidfile /var/run/redis/redis_6379.pid
    logfile "/var/log/redis/redis_6379.log"
    dbfilename redis_db.rdb
    dir /data

    #从 Redis 5 版本开始, 指令 slaveof 被废弃了(Deprecated), 取而代之应该使用 指令 replicaof
    replicaof 192.168.175.111 6379

    masterauth redhat
    requirepass redhat

    rename-command CONFIG e374fda5-dcf5-41f2-bf69-a5928aa81874--d1e25c85-961d-4e27-ba88-b8ecf7f99c7a

    #设置 maxclients 时, 注意使用命令 `ulimit -n 100032` 和 内核参数 file-max 设置 系统的限制
    maxclients 100000

    #建议为物理内存的 3/5
    maxmemory 614mb
    maxmemory-policy allkeys-lru

    #启用 aof 日志文件
    appendonly yes
    appendfilename "redis_appendonly.aof"


// 临时修改 nofile 的限制
[root@redis_server02 ~]# ulimit -n 100032

// 持久化 设置 nofile 的限制(centos7 中 相对于使用 ulimit 的方式)
[root@redis_server02 ~]# vim /etc/systemd/system.conf
      DefaultLimitNOFILE=100032




[root@redis_server02 ~]# sysctl -a | grep file-max
      fs.file-max = 95856  <------观察
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"



[root@redis_server02 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

      net.ipv4.tcp_max_syn_backlog = 1024

      fs.file-max = 100032


[root@redis_server02 ~]# sysctl -p
      net.core.somaxconn = 1024
      vm.overcommit_memory = 1
      net.ipv4.tcp_max_syn_backlog = 1024
      fs.file-max = 100032




[root@redis_server02 ~]# sysctl -a | grep -E  'somaxconn|overcommit_memory|tcp_max_syn_backlog|file-max'
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"
      fs.file-max = 100032        <-------
      net.core.somaxconn = 1024   <-------
      net.ipv4.tcp_max_syn_backlog = 1024  <-------
      vm.overcommit_memory = 1             <-------







// 启动 redis-server 服务
[root@redis_server02 ~]# su -l redis -s /bin/bash -c 'redis-server /app/redis/conf/redis.conf'
      su: warning: cannot change directory to /home/redis: No such file or directory


// 查看一下 网络端口
// 在 redis_server02(即当前的 slave) 上查看一下 redis 端口信息
[root@redis_server02 ~]# netstat -anptu | grep redis
      tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      56660/redis-server
      tcp        0      0 192.168.175.112:6379    0.0.0.0:*               LISTEN      56660/redis-server
      tcp        0      0 192.168.175.112:43855   192.168.175.111:6379    ESTABLISHED 56660/redis-server  <-----观察(已建立 replicate 用的 connection)

// 在 redis_server01(即当前的 master) 上查看一下 redis 端口信息
[root@redis_server01 ~]# netstat -anptu | grep redis
      tcp        0      0 127.0.0.1:6379          0.0.0.0:*               LISTEN      21450/redis-server
      tcp        0      0 192.168.175.111:6379    0.0.0.0:*               LISTEN      21450/redis-server
      tcp        0      0 192.168.175.111:6379    192.168.175.112:43855   ESTABLISHED 21450/redis-server  <-----观察(已建立 replicate 用的 connection)



// 查看一下进程
[root@redis_server02 ~]# ps aux | grep redis
      redis     56660  0.2  0.5 163108  5412 ?        Ssl  15:55   0:00 redis-server 192.168.175.112:6379




// 查看一下日志
[root@redis_server02 ~]# cat /var/log/redis/redis_6379.log
              56639:C 22 Sep 2019 15:55:10.478 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
              56639:C 22 Sep 2019 15:55:10.479 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=56639, just started
              56639:C 22 Sep 2019 15:55:10.479 # Configuration loaded
                              _._
                         _.-``__ ''-._
                    _.-``    `.  `_.  ''-._           Redis 5.0.5 (00000000/0) 64 bit
                .-`` .-```.  ```\/    _.,_ ''-._
               (    '      ,       .-`  | `,    )     Running in standalone mode
               |`-._`-...-` __...-.``-._|'` _.-'|     Port: 6379
               |    `-._   `._    /     _.-'    |     PID: 56660
                `-._    `-._  `-./  _.-'    _.-'
               |`-._`-._    `-.__.-'    _.-'_.-'|
               |    `-._`-._        _.-'_.-'    |           http://redis.io
                `-._    `-._`-.__.-'_.-'    _.-'
               |`-._`-._    `-.__.-'    _.-'_.-'|
               |    `-._`-._        _.-'_.-'    |
                `-._    `-._`-.__.-'_.-'    _.-'
                    `-._    `-.__.-'    _.-'
                        `-._        _.-'
                            `-.__.-'

              56660:S 22 Sep 2019 15:55:10.535 # Server initialized
              56660:S 22 Sep 2019 15:55:10.535 * Ready to accept connections
              56660:S 22 Sep 2019 15:55:10.536 * Connecting to MASTER 192.168.175.111:6379
              56660:S 22 Sep 2019 15:55:10.536 * MASTER <-> REPLICA sync started
              56660:S 22 Sep 2019 15:55:10.549 * Non blocking connect for SYNC fired the event.
              56660:S 22 Sep 2019 15:55:10.550 * Master replied to PING, replication can continue...
              56660:S 22 Sep 2019 15:55:10.565 * Partial resynchronization not possible (no cached master)
              56660:S 22 Sep 2019 15:55:10.601 * Full resync from master: 22615cdd1f3de28f5ef9e624015d45ca5749ccb6:0
              56660:S 22 Sep 2019 15:55:10.725 * MASTER <-> REPLICA sync: receiving 175 bytes from master
              56660:S 22 Sep 2019 15:55:10.725 * MASTER <-> REPLICA sync: Flushing old data
              56660:S 22 Sep 2019 15:55:10.726 * MASTER <-> REPLICA sync: Loading DB in memory
              56660:S 22 Sep 2019 15:55:10.726 * MASTER <-> REPLICA sync: Finished with success
              56660:S 22 Sep 2019 15:55:10.727 * Background append only file rewriting started by pid 56665
              56660:S 22 Sep 2019 15:55:10.765 * AOF rewrite child asks to stop sending diffs.
              56665:C 22 Sep 2019 15:55:10.765 * Parent agreed to stop sending diffs. Finalizing AOF...
              56665:C 22 Sep 2019 15:55:10.766 * Concatenating 0.00 MB of AOF diff received from parent.
              56665:C 22 Sep 2019 15:55:10.766 * SYNC append only file rewrite performed
              56665:C 22 Sep 2019 15:55:10.783 * AOF rewrite: 0 MB of memory used by copy-on-write
              56660:S 22 Sep 2019 15:55:10.839 * Background AOF rewrite terminated with success
              56660:S 22 Sep 2019 15:55:10.839 * Residual parent diff successfully flushed to the rewritten AOF (0.00 MB)
              56660:S 22 Sep 2019 15:55:10.839 * Background AOF rewrite finished successfully


// 查看一下  目录 /data 下的数据文件 (rdb 和 aof 两种格式)
[root@redis_server02 ~]# ls /data/
      redis_appendonly.aof  redis_db.rdb



// 设置开机自启
[root@redis_server02 ~]# vim /etc/rc.d/rc.local

        echo never > /sys/kernel/mm/transparent_hugepage/enabled
        #注: redis 服务的启动一定要放在 transparent_hugepage 被禁用之后
        su -l redis -s /bin/bash -c 'redis-server /app/redis/conf/redis.conf'

----------------------------------------------------------------------------------------------------
// 测试 redis_server01(master) 到 redis_server02(slave) 的主从复制

// 在 redis_server01 上写入一些数据
[root@redis_server01 ~]# redis-cli
      127.0.0.1:6379> AUTH redhat
      OK
      127.0.0.1:6379> set a 1  <-----因为设置了连接空闲(idle)超时(timeout), 所以执行 指令 auth 之后 需要快一点执行 set 指令
      OK
      127.0.0.1:6379> set name Tom
      OK


// 在 redis_server02 查看 redis_server01 上写入的数据
[root@redis_server02 ~]# redis-cli
      127.0.0.1:6379> AUTH redhat
      OK
      127.0.0.1:6379> get a
      "1"
      127.0.0.1:6379> get name
      "Tom"


// 在 redis_server01 上(当前 master)清理测试数据
[root@redis_server01 ~]# redis-cli
      127.0.0.1:6379> AUTH redhat
      OK
      127.0.0.1:6379> DEL a
      (integer) 1
      127.0.0.1:6379> DEL name
      (integer) 1
      127.0.0.1:6379> get a
      (nil)
      127.0.0.1:6379> get name
      (nil)

// 在 redis_server02 上(当前 slave) 查看 redis_server01 上(当前 master)清理的测试数据
[root@redis_server02 ~]# redis-cli
      127.0.0.1:6379> AUTH redhat
      OK
      127.0.0.1:6379> get a
      (nil)
      127.0.0.1:6379> get name
      (nil)
      127.0.0.1:6379>




----------------------------------------------------------------------------------------------------
准备 redis_sentinel01

      注: 如果 是在 docker 等 重映射了 ip 或 port 的环境中部署redis, 需要注意其他事项





// 为了提高安全, 创建 redis 账号, 后续会以该 redis 普通账号的身份来启动 redis 相关服务
[root@redis_sentinel01 ~]# useradd -M -s /sbin/nologin redis
[root@redis_sentinel01 ~]# grep redis /etc/passwd
      redis:x:1001:1001::/home/redis:/sbin/nologin




// 创建并保护 配置文件目录
[root@redis_sentinel01 ~]# mkdir /app/redis/conf
[root@redis_sentinel01 ~]# chown redis:redis /app/redis/conf/
[root@redis_sentinel01 ~]# chmod u=rwx,go-rwx /app/redis/conf


// 创建并保护 运行时文件目录
[root@redis_sentinel01 ~]# mkdir /var/run/redis/
[root@redis_sentinel01 ~]# chown redis:redis /var/run/redis
[root@redis_sentinel01 ~]# chmod u=rwx,go-rwx /var/run/redis



// 创建并保护 日志文件目录
[root@redis_sentinel01 ~]# mkdir /var/log/redis
[root@redis_sentinel01 ~]# chown redis:redis /var/log/redis/
[root@redis_sentinel01 ~]# chmod u=rwx,go-rwx /var/log/redis

[root@redis_sentinel01 ~]# cp ~/download/redis-5.0.5/sentinel.conf /app/redis/conf/
[root@redis_sentinel01 ~]# chown -R redis:redis /app/redis/conf/


[root@redis_sentinel01 ~]# vim /app/redis/conf/sentinel.conf

          # 注意, bind 中 各 ip 的顺序很重要,即 127.0.0.1 必须出现在 192.168.175.101 之后, 否则
          # sentinel 无法正常工作, 更多信息见 后面的 "注意事项01"
          #bind 127.0.0.1 192.168.175.101  <----错误
          bind 192.168.175.101 127.0.0.1
          protected-mode yes
          port 26379
          daemonize yes
          pidfile /var/run/redis/redis-sentinel.pid
          logfile /var/log/redis/redis-sentinel.log
          #sentinel monitor <master-name> <ip> <redis-port> <quorum>
          sentinel monitor mymaster 192.168.175.111 6379 2
          #sentinel auth-pass <master-name> <password>
          sentinel auth-pass mymaster redhat
          #sentinel down-after-milliseconds <master-name> <milliseconds>
          # 此处设置为 5 seconds
          sentinel down-after-milliseconds mymaster 5000
          #sentinel parallel-syncs <master-name> <numreplicas>
          sentinel parallel-syncs mymaster 1
          # sentinel failover-timeout <master-name> <milliseconds>
          # 此处设置为 3 minutes
          sentinel failover-timeout mymaster 180000
          # 重命名 指令 CONFIG
          SENTINEL rename-command mymaster CONFIG e374fda5-dcf5-41f2-bf69-a5928aa81874--d1e25c85-961d-4e27-ba88-b8ecf7f99c7a
          # 从 Redis 5.0.1 版本开始, 还可以使用指令 requirepass 为 Sentinel instance 本身设置认证密码
          requirepass redhat_sentinel






// 临时修改 nofile 的限制
[root@redis_sentinel01 ~]# ulimit -n 100032

// 持久化 设置 nofile 的限制(centos7 中 相对于使用 ulimit 的方式)
[root@redis_sentinel01 ~]# vim /etc/systemd/system.conf
      DefaultLimitNOFILE=100032

[root@redis_server01 ~]# sysctl -a | grep file-max
      fs.file-max = 95856  <------观察
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"



[root@redis_sentinel01 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

      net.ipv4.tcp_max_syn_backlog = 1024

      fs.file-max = 100032


[root@redis_sentinel01 ~]# sysctl -p
      net.core.somaxconn = 1024
      vm.overcommit_memory = 1
      net.ipv4.tcp_max_syn_backlog = 1024
      fs.file-max = 100032





[root@redis_sentinel01 ~]# sysctl -a | grep -E  'somaxconn|overcommit_memory|tcp_max_syn_backlog|file-max'
        fs.file-max = 100032   <-------
        sysctl: reading key "net.ipv6.conf.all.stable_secret"
        sysctl: reading key "net.ipv6.conf.default.stable_secret"
        sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
        sysctl: reading key "net.ipv6.conf.lo.stable_secret"
        net.core.somaxconn = 1024  <-------
        net.ipv4.tcp_max_syn_backlog = 1024 <-------
        vm.overcommit_memory = 1  <-------













----------------------------------------------------------------------------------------------------
准备 redis_sentinel02

      注: 如果 是在 docker 等 重映射了 ip 或 port 的环境中部署redis, 需要注意其他事项





// 为了提高安全, 创建 redis 账号, 后续会以该 redis 普通账号的身份来启动 redis 相关服务
[root@redis_sentinel02 ~]# useradd -M -s /sbin/nologin redis
[root@redis_sentinel02 ~]# grep redis /etc/passwd
      redis:x:1001:1001::/home/redis:/sbin/nologin


// 创建并保护 配置文件目录
[root@redis_sentinel02 ~]# mkdir /app/redis/conf
[root@redis_sentinel02 ~]# chown redis:redis /app/redis/conf/
[root@redis_sentinel02 ~]# chmod u=rwx,go-rwx /app/redis/conf


// 创建并保护 运行时文件目录
[root@redis_sentinel02 ~]# mkdir /var/run/redis/
[root@redis_sentinel02 ~]# chown redis:redis /var/run/redis
[root@redis_sentinel02 ~]# chmod u=rwx,go-rwx /var/run/redis



// 创建并保护 日志文件目录
[root@redis_sentinel02 ~]# mkdir /var/log/redis
[root@redis_sentinel02 ~]# chown redis:redis /var/log/redis/
[root@redis_sentinel02 ~]# chmod u=rwx,go-rwx /var/log/redis

[root@redis_sentinel02 ~]# cp ~/download/redis-5.0.5/sentinel.conf /app/redis/conf/
[root@redis_sentinel02 ~]# chown -R redis:redis /app/redis/conf/

[root@redis_sentinel02 ~]# rsync -av root@192.168.175.101:/app/redis/conf/sentinel.conf  /app/redis/conf/sentinel.conf
[root@redis_sentinel02 ~]# ls -l /app/redis/conf/sentinel.conf
      -rw-r--r-- 1 redis redis 10317 Sep 22  2019 /app/redis/conf/sentinel.conf





[root@redis_sentinel02 ~]# vim /app/redis/conf/sentinel.conf

          # 注意, bind 中 各 ip 的顺序很重要,即 127.0.0.1 必须出现在 192.168.175.102 之后, 否则
          # sentinel 无法正常工作, 更多信息见 后面的 "注意事项01"
          #bind 127.0.0.1 192.168.175.102  <----错误
          bind 192.168.175.102 127.0.0.1
          protected-mode yes





// 临时修改 nofile 的限制
[root@redis_sentinel02 ~]# ulimit -n 100032

// 持久化 设置 nofile 的限制(centos7 中 相对于使用 ulimit 的方式)
[root@redis_sentinel02 ~]# vim /etc/systemd/system.conf
      DefaultLimitNOFILE=100032

[root@redis_server02 ~]# sysctl -a | grep file-max
      fs.file-max = 95856  <------观察
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"



[root@redis_sentinel02 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

      net.ipv4.tcp_max_syn_backlog = 1024

      fs.file-max = 100032


[root@redis_sentinel02 ~]# sysctl -p
      net.core.somaxconn = 1024
      vm.overcommit_memory = 1
      net.ipv4.tcp_max_syn_backlog = 1024
      fs.file-max = 100032


[root@redis_sentinel02 ~]# sysctl -a | grep -E  'somaxconn|overcommit_memory|tcp_max_syn_backlog|file-max'
        sysctl: reading key "net.ipv6.conf.all.stable_secret"
        sysctl: reading key "net.ipv6.conf.default.stable_secret"
        sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
        sysctl: reading key "net.ipv6.conf.lo.stable_secret"
        fs.file-max = 100032   <-------
        net.core.somaxconn = 1024   <-------
        net.ipv4.tcp_max_syn_backlog = 1024   <-------
        vm.overcommit_memory = 1   <-------













----------------------------------------------------------------------------------------------------
准备 redis_sentinel03

      注: 如果 是在 docker 等 重映射了 ip 或 port 的环境中部署redis, 需要注意其他事项





// 为了提高安全, 创建 redis 账号, 后续会以该 redis 普通账号的身份来启动 redis 相关服务
[root@redis_sentinel03 ~]# useradd -M -s /sbin/nologin redis
[root@redis_sentinel03 ~]# grep redis /etc/passwd
      redis:x:1001:1001::/home/redis:/sbin/nologin


// 创建并保护 配置文件目录
[root@redis_sentinel03 ~]# mkdir /app/redis/conf
[root@redis_sentinel03 ~]# chown redis:redis /app/redis/conf/
[root@redis_sentinel03 ~]# chmod u=rwx,go-rwx /app/redis/conf


// 创建并保护 运行时文件目录
[root@redis_sentinel03 ~]# mkdir /var/run/redis/
[root@redis_sentinel03 ~]# chown redis:redis /var/run/redis
[root@redis_sentinel03 ~]# chmod u=rwx,go-rwx /var/run/redis



// 创建并保护 日志文件目录
[root@redis_sentinel03 ~]# mkdir /var/log/redis
[root@redis_sentinel03 ~]# chown redis:redis /var/log/redis/
[root@redis_sentinel03 ~]# chmod u=rwx,go-rwx /var/log/redis

[root@redis_sentinel03 ~]# cp ~/download/redis-5.0.5/sentinel.conf /app/redis/conf/
[root@redis_sentinel03 ~]# chown -R redis:redis /app/redis/conf/

[root@redis_sentinel03 ~]# rsync -av root@192.168.175.101:/app/redis/conf/sentinel.conf  /app/redis/conf/sentinel.conf
[root@redis_sentinel03 ~]# ls -l /app/redis/conf/sentinel.conf
      -rw-r--r-- 1 redis redis 10317 Sep 22  2019 /app/redis/conf/sentinel.conf





[root@redis_sentinel03 ~]# vim /app/redis/conf/sentinel.conf

          # 注意, bind 中 各 ip 的顺序很重要,即 127.0.0.1 必须出现在 192.168.175.103 之后, 否则
          # sentinel 无法正常工作, 更多信息见 后面的 "注意事项01"
          #bind 127.0.0.1 192.168.175.103  <----错误
          bind 192.168.175.103 127.0.0.1
          protected-mode yes




// 临时修改 nofile 的限制
[root@redis_sentinel03 ~]# ulimit -n 100032

// 持久化 设置 nofile 的限制(centos7 中 相对于使用 ulimit 的方式)
[root@redis_sentinel03 ~]# vim /etc/systemd/system.conf
      DefaultLimitNOFILE=100032

[root@redis_server02 ~]# sysctl -a | grep file-max
      fs.file-max = 95856  <------观察
      sysctl: reading key "net.ipv6.conf.all.stable_secret"
      sysctl: reading key "net.ipv6.conf.default.stable_secret"
      sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
      sysctl: reading key "net.ipv6.conf.lo.stable_secret"



[root@redis_sentinel03 ~]# vim /etc/sysctl.conf

      net.core.somaxconn = 1024
      vm.overcommit_memory = 1

      net.ipv4.tcp_max_syn_backlog = 1024

      fs.file-max = 100032


[root@redis_sentinel03 ~]# sysctl -p
      net.core.somaxconn = 1024
      vm.overcommit_memory = 1
      net.ipv4.tcp_max_syn_backlog = 1024
      fs.file-max = 100032


[root@redis_sentinel03 ~]# sysctl -a | grep -E  'somaxconn|overcommit_memory|tcp_max_syn_backlog|file-max'
        sysctl: reading key "net.ipv6.conf.all.stable_secret"
        sysctl: reading key "net.ipv6.conf.default.stable_secret"
        sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
        sysctl: reading key "net.ipv6.conf.lo.stable_secret"
        fs.file-max = 100032   <-------
        net.core.somaxconn = 1024   <-------
        net.ipv4.tcp_max_syn_backlog = 1024   <-------
        vm.overcommit_memory = 1   <-------





====================================================================================================

// 启动  redis_sentinel01 上的 redis-sentinel
[root@redis_sentinel01 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'
        su: warning: cannot change directory to /home/redis: No such file or directory

// 查看 redis_sentinel01 上的 日志文件
[root@redis_sentinel01 ~]# cat /var/log/redis/redis-sentinel.log
        6404:X 23 Sep 2019 20:08:25.544 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
        6404:X 23 Sep 2019 20:08:25.544 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=6404, just started
        6404:X 23 Sep 2019 20:08:25.544 # Configuration loaded
        6425:X 23 Sep 2019 20:08:25.548 * Running mode=sentinel, port=26379.
        6425:X 23 Sep 2019 20:08:25.550 # Sentinel ID is dace638f24504101e3328d2b93c4c2f153d2b8bd
        6425:X 23 Sep 2019 20:08:25.550 # +monitor master mymaster 192.168.175.111 6379 quorum 2
        6425:X 23 Sep 2019 20:08:25.562 * +slave slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379



// 启动  redis_sentinel02 上的 redis-sentinel
[root@redis_sentinel02 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'
        su: warning: cannot change directory to /home/redis: No such file or directory


// 查看 redis_sentinel02 上的 日志文件
[root@redis_sentinel02 ~]# cat /var/log/redis/redis-sentinel.log
        6051:X 23 Sep 2019 20:10:42.956 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
        6051:X 23 Sep 2019 20:10:42.956 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=6051, just started
        6051:X 23 Sep 2019 20:10:42.956 # Configuration loaded
        6072:X 23 Sep 2019 20:10:42.962 * Running mode=sentinel, port=26379.
        6072:X 23 Sep 2019 20:10:42.963 # Sentinel ID is 0525b602bd6806c3ebc5269a626d0ba5bcb329d3
        6072:X 23 Sep 2019 20:10:42.963 # +monitor master mymaster 192.168.175.111 6379 quorum 2
        6072:X 23 Sep 2019 20:10:42.966 * +slave slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379
        6072:X 23 Sep 2019 20:10:43.593 * +sentinel sentinel dace638f24504101e3328d2b93c4c2f153d2b8bd 192.168.175.101 26379 @ mymaster 192.168.175.111 6379

// 查看 启动  redis_sentinel02 上的 redis-sentinel 后 redis_sentinel01 上 redis-sentinel 的 日志文件 新增的内容
[root@redis_sentinel01 ~]# cat /var/log/redis/redis-sentinel.log

      6425:X 23 Sep 2019 20:10:45.460 * +sentinel sentinel 0525b602bd6806c3ebc5269a626d0ba5bcb329d3 192.168.175.102 26379 @ mymaster 192.168.175.111 6379


// 在 redis_sentinel01 实时观察 redis-sentinel 上的日志文件:
[root@redis_sentinel01 ~]# tail -f  /var/log/redis/redis-sentinel.log


// 在 redis_sentinel02 实时观察 redis-sentinel 上的日志文件:
[root@redis_sentinel02 ~]# tail -f  /var/log/redis/redis-sentinel.log


// 启动  redis_sentinel03 上的 redis-sentinel
[root@redis_sentinel03 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'
        su: warning: cannot change directory to /home/redis: No such file or directory

[root@redis_sentinel03 ~]# cat /var/log/redis/redis-sentinel.log
        6380:X 23 Sep 2019 20:17:56.717 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
        6380:X 23 Sep 2019 20:17:56.717 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=6380, just started
        6380:X 23 Sep 2019 20:17:56.717 # Configuration loaded
        6401:X 23 Sep 2019 20:17:56.725 * Running mode=sentinel, port=26379.
        6401:X 23 Sep 2019 20:17:56.726 # Sentinel ID is b033e9929be780dfbc017d8a5debb02c43378510
        6401:X 23 Sep 2019 20:17:56.726 # +monitor master mymaster 192.168.175.111 6379 quorum 2
        6401:X 23 Sep 2019 20:17:56.729 * +slave slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379
        6401:X 23 Sep 2019 20:17:58.166 * +sentinel sentinel dace638f24504101e3328d2b93c4c2f153d2b8bd 192.168.175.101 26379 @ mymaster 192.168.175.111 6379
        6401:X 23 Sep 2019 20:17:58.564 * +sentinel sentinel 0525b602bd6806c3ebc5269a626d0ba5bcb329d3 192.168.175.102 26379 @ mymaster 192.168.175.111 6379


// 如下为 在 redis_sentinel01 上实时观察到的 redis-sentinel 的日志文件中 新增的内容:
      6425:X 23 Sep 2019 20:17:59.637 * +sentinel sentinel b033e9929be780dfbc017d8a5debb02c43378510 192.168.175.103 26379 @ mymaster 192.168.175.111 6379

// 如下为 在 redis_sentinel02 上实时观察到的 redis-sentinel 的日志文件中 新增的内容:
      6072:X 23 Sep 2019 20:17:59.180 * +sentinel sentinel b033e9929be780dfbc017d8a5debb02c43378510 192.168.175.103 26379 @ mymaster 192.168.175.111 6379

[root@redis_sentinel01 ~]# netstat -anptu | grep redis
      tcp        0      0 127.0.0.1:26379         0.0.0.0:*               LISTEN      6425/redis-sentinel
      tcp        0      0 192.168.175.101:26379   0.0.0.0:*               LISTEN      6425/redis-sentinel
      tcp        0      0 192.168.175.101:26379   192.168.175.102:39513   ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:53357   192.168.175.111:6379    ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:34547   192.168.175.112:6379    ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:35918   192.168.175.111:6379    ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:34227   192.168.175.102:26379   ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:26379   192.168.175.103:40669   ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:58321   192.168.175.103:26379   ESTABLISHED 6425/redis-sentinel
      tcp        0      0 192.168.175.101:35788   192.168.175.112:6379    ESTABLISHED 6425/redis-sentinel


[root@redis_sentinel01 ~]# ps aux | grep redis
      redis      6425  0.3  0.7 153892  7848 ?        Ssl  20:08   0:07 redis-sentinel 192.168.175.101:26379 [sentinel]



[root@redis_sentinel01 ~]# redis-cli -p 26379
      127.0.0.1:26379> auth redhat_sentinel
      OK
      127.0.0.1:26379> sentinel master mymaster    <=====执行命令, Asking Sentinel about the state of a master
       1) "name"
       2) "mymaster"
       3) "ip"
       4) "192.168.175.111"
       5) "port"
       6) "6379"
       7) "runid"
       8) "dc41151f036d8dfc3704f5ce1bb83ad28b093ab6"
       9) "flags"  <=====执行命令, Asking Sentinel about the state of a master
      10) "master"
      11) "link-pending-commands"
      12) "0"
      13) "link-refcount"
      14) "1"
      15) "last-ping-sent"
      16) "0"
      17) "last-ok-ping-reply"
      18) "235"
      19) "last-ping-reply"
      20) "235"
      21) "down-after-milliseconds"
      22) "5000"
      23) "info-refresh"
      24) "1198"
      25) "role-reported"
      26) "master"
      27) "role-reported-time"
      28) "2319916"
      29) "config-epoch"
      30) "0"
      31) "num-slaves"   <---------------------观察(检测到 master 有 1 个 slave)
      32) "1"
      33) "num-other-sentinels"   <-------------------观察(检测到还有其他 2 个 sentinels)
      34) "2"
      35) "quorum"
      36) "2"
      37) "failover-timeout"
      38) "180000"
      39) "parallel-syncs"
      40) "1"
      127.0.0.1:26379> SENTINEL slaves mymaster   <=========执行命令, 查看 master ‘mymaster’ 中的 slaves 的 state 和 info
      1)  1) "name"
          2) "192.168.175.112:6379"
          3) "ip"
          4) "192.168.175.112"
          5) "port"
          6) "6379"
          7) "runid"
          8) "9337a3cb7f6ccb998dda8f61da804c16d2ccb136"
          9) "flags"
         10) "slave"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "169"
         19) "last-ping-reply"
         20) "169"
         21) "down-after-milliseconds"
         22) "5000"
         23) "info-refresh"
         24) "1512"
         25) "role-reported"
         26) "slave"
         27) "role-reported-time"
         28) "2380846"
         29) "master-link-down-time"
         30) "0"
         31) "master-link-status"
         32) "ok"
         33) "master-host"
         34) "192.168.175.111"
         35) "master-port"
         36) "6379"
         37) "slave-priority"
         38) "100"
         39) "slave-repl-offset"
         40) "1294524"
      127.0.0.1:26379> SENTINEL get-master-addr-by-name mymaster   <=========执行命令, 查看 mymaster 中 当前 master 的 ip 和 port 信息
      1) "192.168.175.111"
      2) "6379"
      127.0.0.1:26379> SENTINEL masters  <========执行命令, 查看该 sentinel instance 监视的 masters 列表 及其 状态信息
      1)  1) "name"
          2) "mymaster"
          3) "ip"
          4) "192.168.175.111"
          5) "port"
          6) "6379"
          7) "runid"
          8) "dc41151f036d8dfc3704f5ce1bb83ad28b093ab6"
          9) "flags"
         10) "master"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "436"
         19) "last-ping-reply"
         20) "436"
         21) "down-after-milliseconds"
         22) "5000"
         23) "info-refresh"
         24) "42"
         25) "role-reported"
         26) "master"
         27) "role-reported-time"
         28) "2499531"
         29) "config-epoch"
         30) "0"
         31) "num-slaves"
         32) "1"
         33) "num-other-sentinels"
         34) "2"
         35) "quorum"
         36) "2"
         37) "failover-timeout"
         38) "180000"
         39) "parallel-syncs"
         40) "1"
      127.0.0.1:26379> SENTINEL sentinels mymaster  <=====执行命令, 查看其他 sentinels 相关信息
      1)  1) "name"
          2) "b033e9929be780dfbc017d8a5debb02c43378510"
          3) "ip"
          4) "192.168.175.103"
          5) "port"
          6) "26379"
          7) "runid"
          8) "b033e9929be780dfbc017d8a5debb02c43378510"
          9) "flags"
         10) "sentinel"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "562"
         19) "last-ping-reply"
         20) "562"
         21) "down-after-milliseconds"
         22) "5000"
         23) "last-hello-message"
         24) "909"
         25) "voted-leader"
         26) "?"
         27) "voted-leader-epoch"
         28) "0"
      2)  1) "name"
          2) "0525b602bd6806c3ebc5269a626d0ba5bcb329d3"
          3) "ip"
          4) "192.168.175.102"
          5) "port"
          6) "26379"
          7) "runid"
          8) "0525b602bd6806c3ebc5269a626d0ba5bcb329d3"
          9) "flags"
         10) "sentinel"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "561"
         19) "last-ping-reply"
         20) "561"
         21) "down-after-milliseconds"
         22) "5000"
         23) "last-hello-message"
         24) "906"
         25) "voted-leader"
         26) "?"
         27) "voted-leader-epoch"
         28) "0"
      127.0.0.1:26379> SENTINEL ckquorum mymaster    <===============执行命令, 检查 是否 当前的 Sentinel configuration 是否具备故障转移的能力
      OK 3 usable Sentinels. Quorum and failover authorization can be reached


                                命令 SENTINEL ckquorum <master name> 的作用:
                                            // 检查当前 Sentinel configuration 是否能够 达到 故障转移 a master
                                            // 所需的 quorum, 以及 达到 故障转移所需的 the majority.
                                            // 该命令应该被用于  监视 systems 来 检查 a Sentinel deployment 是否 ok


--------------------------------------------------
Testing the failover  (测试故障转移)

// 让 master 睡眠 30 seconds, 使其 不可达(no longer reachable)
[root@redis_server01 ~]# redis-cli -h 127.0.0.1 -a redhat -p 6379 DEBUG sleep 30



// 观察 redis_sentinel01 上 /var/log/redis/redis-sentinel.log 日志信息
      6425:X 23 Sep 2019 20:56:25.450 # +sdown master mymaster 192.168.175.111 6379
      6425:X 23 Sep 2019 20:56:25.949 # +new-epoch 1
      6425:X 23 Sep 2019 20:56:25.950 # +vote-for-leader b033e9929be780dfbc017d8a5debb02c43378510 1
      6425:X 23 Sep 2019 20:56:26.535 # +odown master mymaster 192.168.175.111 6379 #quorum 3/2
      6425:X 23 Sep 2019 20:56:26.536 # Next failover delay: I will not start a failover before Mon Sep 23 21:02:26 2019
      6425:X 23 Sep 2019 20:56:27.142 # +config-update-from sentinel b033e9929be780dfbc017d8a5debb02c43378510 192.168.175.103 26379 @ mymaster 192.168.175.111 6379
      6425:X 23 Sep 2019 20:56:27.142 # +switch-master mymaster 192.168.175.111 6379 192.168.175.112 6379
      6425:X 23 Sep 2019 20:56:27.146 * +slave slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6425:X 23 Sep 2019 20:56:32.152 # +sdown slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6425:X 23 Sep 2019 20:56:50.057 # -sdown slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6425:X 23 Sep 2019 20:57:00.067 * +convert-to-slave slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379




// 观察 redis_sentinel02 上 /var/log/redis/redis-sentinel.log 日志信息
      6072:X 23 Sep 2019 20:56:25.465 # +sdown master mymaster 192.168.175.111 6379
      6072:X 23 Sep 2019 20:56:25.492 # +new-epoch 1
      6072:X 23 Sep 2019 20:56:25.493 # +vote-for-leader b033e9929be780dfbc017d8a5debb02c43378510 1
      6072:X 23 Sep 2019 20:56:25.536 # +odown master mymaster 192.168.175.111 6379 #quorum 3/2
      6072:X 23 Sep 2019 20:56:25.552 # Next failover delay: I will not start a failover before Mon Sep 23 21:02:26 2019
      6072:X 23 Sep 2019 20:56:26.685 # +config-update-from sentinel b033e9929be780dfbc017d8a5debb02c43378510 192.168.175.103 26379 @ mymaster 192.168.175.111 6379
      6072:X 23 Sep 2019 20:56:26.686 # +switch-master mymaster 192.168.175.111 6379 192.168.175.112 6379
      6072:X 23 Sep 2019 20:56:26.687 * +slave slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6072:X 23 Sep 2019 20:56:31.701 # +sdown slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6072:X 23 Sep 2019 20:56:49.575 # -sdown slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379


// 观察 redis_sentinel03 上 /var/log/redis/redis-sentinel.log 日志信息
      6401:X 23 Sep 2019 20:56:24.959 # +sdown master mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:25.036 # +odown master mymaster 192.168.175.111 6379 #quorum 2/2
      6401:X 23 Sep 2019 20:56:25.036 # +new-epoch 1
      6401:X 23 Sep 2019 20:56:25.036 # +try-failover master mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:25.037 # +vote-for-leader b033e9929be780dfbc017d8a5debb02c43378510 1
      6401:X 23 Sep 2019 20:56:25.042 # dace638f24504101e3328d2b93c4c2f153d2b8bd voted for b033e9929be780dfbc017d8a5debb02c43378510 1
      6401:X 23 Sep 2019 20:56:25.043 # 0525b602bd6806c3ebc5269a626d0ba5bcb329d3 voted for b033e9929be780dfbc017d8a5debb02c43378510 1
      6401:X 23 Sep 2019 20:56:25.128 # +elected-leader master mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:25.128 # +failover-state-select-slave master mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:25.182 # +selected-slave slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:25.182 * +failover-state-send-slaveof-noone slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:25.283 * +failover-state-wait-promotion slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:26.125 # +promoted-slave slave 192.168.175.112:6379 192.168.175.112 6379 @ mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:26.125 # +failover-state-reconf-slaves master mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:26.223 # +failover-end master mymaster 192.168.175.111 6379
      6401:X 23 Sep 2019 20:56:26.223 # +switch-master mymaster 192.168.175.111 6379 192.168.175.112 6379
      6401:X 23 Sep 2019 20:56:26.225 * +slave slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6401:X 23 Sep 2019 20:56:31.272 # +sdown slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379
      6401:X 23 Sep 2019 20:56:49.067 # -sdown slave 192.168.175.111:6379 192.168.175.111 6379 @ mymaster 192.168.175.112 6379



[root@redis_sentinel01 ~]# redis-cli -p 26379
      127.0.0.1:26379> auth redhat_sentinel
      OK
      127.0.0.1:26379> SENTINEL ckquorum mymaster  <=====执行命令, 检查 故障转移后当前的 Sentinel configuration 是否具备故障转移的能力
      OK 3 usable Sentinels. Quorum and failover authorization can be reached

      127.0.0.1:26379> SENTINEL get-master-addr-by-name mymaster  <====执行命令, 查看 故障转移后 当前的 master 的 ip 和 port
      1) "192.168.175.112"
      2) "6379"


      127.0.0.1:26379> SENTINEL masters   <======执行命令, 查看当前 监视的所有 masters
      1)  1) "name"
          2) "mymaster"
          3) "ip"
          4) "192.168.175.112"
          5) "port"
          6) "6379"
          7) "runid"
          8) "9337a3cb7f6ccb998dda8f61da804c16d2ccb136"
          9) "flags"
         10) "master"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "235"
         19) "last-ping-reply"
         20) "235"
         21) "down-after-milliseconds"
         22) "5000"
         23) "info-refresh"
         24) "2347"
         25) "role-reported"
         26) "master"
         27) "role-reported-time"
         28) "193023"
         29) "config-epoch"
         30) "1"
         31) "num-slaves"
         32) "1"
         33) "num-other-sentinels"
         34) "2"
         35) "quorum"
         36) "2"
         37) "failover-timeout"
         38) "180000"
         39) "parallel-syncs"
         40) "1"
      127.0.0.1:26379> SENTINEL slaves mymaster  <=======执行命令, 查看 mymaster 当前的 slaves
      1)  1) "name"
          2) "192.168.175.111:6379"
          3) "ip"
          4) "192.168.175.111"
          5) "port"
          6) "6379"
          7) "runid"
          8) "dc41151f036d8dfc3704f5ce1bb83ad28b093ab6"
          9) "flags"
         10) "slave"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "707"
         19) "last-ping-reply"
         20) "707"
         21) "down-after-milliseconds"
         22) "5000"
         23) "info-refresh"
         24) "1914"
         25) "role-reported"
         26) "slave"
         27) "role-reported-time"
         28) "212802"
         29) "master-link-down-time"
         30) "0"
         31) "master-link-status"
         32) "ok"
         33) "master-host"
         34) "192.168.175.112"
         35) "master-port"
         36) "6379"
         37) "slave-priority"
         38) "100"
         39) "slave-repl-offset"
         40) "1455644"
      127.0.0.1:26379> SENTINEL sentinels mymaster   <========执行命令, 查看 监视 mymaster 的其他 sentinels 的信息
      1)  1) "name"
          2) "b033e9929be780dfbc017d8a5debb02c43378510"
          3) "ip"
          4) "192.168.175.103"
          5) "port"
          6) "26379"
          7) "runid"
          8) "b033e9929be780dfbc017d8a5debb02c43378510"
          9) "flags"
         10) "sentinel"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "424"
         19) "last-ping-reply"
         20) "424"
         21) "down-after-milliseconds"
         22) "5000"
         23) "last-hello-message"
         24) "675"
         25) "voted-leader"
         26) "?"
         27) "voted-leader-epoch"
         28) "0"
      2)  1) "name"
          2) "0525b602bd6806c3ebc5269a626d0ba5bcb329d3"
          3) "ip"
          4) "192.168.175.102"
          5) "port"
          6) "26379"
          7) "runid"
          8) "0525b602bd6806c3ebc5269a626d0ba5bcb329d3"
          9) "flags"
         10) "sentinel"
         11) "link-pending-commands"
         12) "0"
         13) "link-refcount"
         14) "1"
         15) "last-ping-sent"
         16) "0"
         17) "last-ok-ping-reply"
         18) "424"
         19) "last-ping-reply"
         20) "424"
         21) "down-after-milliseconds"
         22) "5000"
         23) "last-hello-message"
         24) "182"
         25) "voted-leader"
         26) "?"
         27) "voted-leader-epoch"
         28) "0"
      127.0.0.1:26379>









====================================================================================================
设置 redis_sentinel01 上 sentinel 的开机自启


[root@redis_sentinel01 ~]# vim /app/redis/conf/sentinel.sh

          #!/bin/bash

          export PATH=$PATH:/app/redis/bin

          pidfile=/var/run/redis/redis-sentinel.pid
          debug_file=/dev/null
          sentinel_port=26379
          sentinel_password=redhat_sentinel


          function start() {
            redis-sentinel /app/redis/conf/sentinel.conf
            sleep 1
            # 使用指令 SENTINEL RESET 刷新旧的状态数据
            redis-cli -h 127.0.0.1 -a $sentinel_password -p $sentinel_port  SENTINEL RESET mymaster
          }

          function stop() {
            if [ ! -f "$pidfile" ]; then
              echo "文件${pidfile} 不存在" >> debug_file
              exit 1
            fi

            pid=$(cat $pidfile)
            if [[ ! $pid =~ ^[[:digit:]]+$ ]]; then
              echo "文件${pidfile} 内容不为数字" >> debug_file
              exit 2
            fi

            kill -s SIGTERM $pid
          }

          function restart() {
            stop
            sleep 2
            start
          }

          case "$1" in
            start|stop|restart)
              $1
              ;;
            *)
              echo $"Usage: $0 {start|stop|restart}"
              exit 2
              ;;
          esac
          exit $?




[root@redis_sentinel01 ~]# chown redis:redis /app/redis/conf/sentinel.sh
[root@redis_sentinel01 ~]# chmod u=rwx,go-rwx /app/redis/conf/sentinel.sh


[root@redis_sentinel01 ~]# touch /etc/systemd/system/redis-sentinel.service
[root@redis_sentinel01 ~]# chmod 664 /etc/systemd/system/redis-sentinel.service
[root@redis_sentinel01 ~]# vim /etc/systemd/system/redis-sentinel.service

[root@redis_sentinel01 ~]# cat /etc/systemd/system/redis-sentinel.service
        [Unit]
        Description=Redis Sentinel
        After=network.target
        After=network-online.target
        Wants=network-online.target

        [Service]
        ExecStartPre=/usr/bin/echo never > /sys/kernel/mm/transparent_hugepage/enabled
        ExecStart=/app/redis/conf/sentinel.sh start
        ExecStop=/app/redis/conf/sentinel.sh stop
        Type=forking
        User=redis
        Group=redis
        PIDFile=/var/run/redis/redis-sentinel.pid
        LimitNOFILE=100032


        [Install]
        WantedBy=multi-user.target



[root@redis_sentinel01 ~]# systemctl daemon-reload
[root@redis_sentinel01 ~]# systemctl start redis-sentinel.service
[root@redis_sentinel01 ~]# systemctl enable redis-sentinel.service
      Created symlink from /etc/systemd/system/multi-user.target.wants/redis-sentinel.service to /etc/systemd/system/redis-sentinel.service.
























----------------------------------------------------------------------------------------------------
搭建中遇到的一下问题 或 注意事项

注意事项01:
关于 bind 和 protected-mode 配置的问题:
sentinel 配置中 默认 protected-mode 是 enabled(即默认其值为 yes)
如下列出了 能正常工作 和 不能够正常工作的 一些配置:

            ------------------------------
            // 方式一  ok(可以通过 192.168.175.102 或 127.0.0.1 访问):
            #  https://stackoverflow.com/questions/34417051/redis-sentinel-marks-slaves-as-down
            #  https://github.com/antirez/redis/commit/edd4d555df57dc84265fdfb4ef59a4678832f6da
            # 注意: 这里 bind 中 ips 的 顺序很重要, 其中 127.0.0.1 必须在 192.168.175.102 之后, 否该该 sentinel 实例无法正常工作
            bind 192.168.175.102 127.0.0.1
            protected-mode yes
            ------------------------------

            ------------------------------
            // 方式二  ok(类似于方式一, 只是无法再通过 127.0.0.1 访问):
            bind 192.168.175.102
            protected-mode yes
            ------------------------------

            ------------------------------
            //方式三 ok (即不指定bind, 可以通过所有 interfaces 或 所有ip 访问)
            #bind 192.168.175.102
            protected-mode no
            ------------------------------

            ------------------------------
            //方式四 wrong, not work(虽然看起来和 方式一相似, 但是 此处因为指令 bind 中顺序上 127.0.0.1 在 192.168.175.102 之前, 所以sentinel 无法正常工作)
            // wrong, not work
            bind 127.0.0.1 192.168.175.102
            protected-mode yes
            ------------------------------

            ------------------------------
            //方式五 wrong, not work(和 方式四类似. 即使把protected-mode 设置为 no, 因为指令 bind 中顺序上 127.0.0.1 在 192.168.175.102 之前, 所以sentinel 还是无法正常工作)
            // wrong, not work
            bind 127.0.0.1 192.168.175.102
            protected-mode no
            ------------------------------

      // 注: 如上 无法 使 sentinel 正常工作的配置(即错误的 方式四 和 方式五) 会导致类似如下的 日志中的错误信息:
      [root@redis_sentinel01 ~]# cat /var/log/redis/redis-sentinel.log
            6570:X 23 Sep 2019 11:19:35.484 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
            6570:X 23 Sep 2019 11:19:35.484 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=6570, just started
            6570:X 23 Sep 2019 11:19:35.484 # Configuration loaded
            6591:X 23 Sep 2019 11:19:35.489 * Running mode=sentinel, port=26379.
            6591:X 23 Sep 2019 11:19:35.490 # Sentinel ID is efe2afc86b74c88bd2f342be15bc7e65d5012630
            6591:X 23 Sep 2019 11:19:35.490 # +monitor master mymaster 192.168.175.111 6379 quorum 2
            6591:X 23 Sep 2019 11:19:40.535 # +sdown master mymaster 192.168.175.111 6379 <-------观察(始终为 +sdown , 这是一个非正常现象)



注意事项02:
   有时 使用命令 `redis-sentinel /app/redis/conf/sentinel.conf` 启动 redis-sentinel 后 查看日志, 发现仍然还是
   类似 '+sdown master mymaster 192.168.175.111 6379' 这样的效果, 此时可以使用指令 `SENTINEL reset <pattern>` 来
   refresh 一下 master 相关的信息, 如下:

        redis-cli -h 192.168.175.101  -a redhat_sentinel -p 26379  SENTINEL RESET mymaster


  https://redis.io/topics/sentinel

      SENTINEL reset <pattern>  说明: This command will reset all the masters with matching name. The pattern argument
                                      is a glob-style pattern. The reset process clears any previous state in
                                      a master (including a failover in progress), and removes every slave
                                      and sentinel already discovered and associated with the master.

----------------------------------------------------------------------------------------------------







