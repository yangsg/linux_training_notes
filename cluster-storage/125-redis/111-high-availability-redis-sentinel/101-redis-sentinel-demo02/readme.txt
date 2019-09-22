

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
[root@redis_sentinel01 ~]# useradd -M -s /sbin/nologin redis
[root@redis_sentinel01 ~]# grep redis /etc/passwd
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

          bind 127.0.0.1 192.168.175.101
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





[root@redis_sentinel01 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'
      su: warning: cannot change directory to /home/redis: No such file or directory

[root@redis_sentinel01 ~]# netstat -anptu | grep redis
      tcp        0      0 192.168.175.101:26379   0.0.0.0:*               LISTEN      22393/redis-sentine
      tcp        0      0 127.0.0.1:26379         0.0.0.0:*               LISTEN      22393/redis-sentine


[root@redis_sentinel01 ~]# ps aux | grep redis
      redis     22393  0.4  0.7 153892  7860 ?        Ssl  20:48   0:00 redis-sentinel 127.0.0.1:26379 [sentinel]

[root@redis_sentinel01 ~]# cat /var/log/redis/redis-sentinel.log
      22372:X 22 Sep 2019 20:48:06.658 # oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
      22372:X 22 Sep 2019 20:48:06.658 # Redis version=5.0.5, bits=64, commit=00000000, modified=0, pid=22372, just started
      22372:X 22 Sep 2019 20:48:06.658 # Configuration loaded
      22393:X 22 Sep 2019 20:48:06.964 * Running mode=sentinel, port=26379.
      22393:X 22 Sep 2019 20:48:06.986 # Sentinel ID is e7d077382711be9e8139bdcf1f8376b27d2848ef
      22393:X 22 Sep 2019 20:48:06.986 # +monitor master mymaster 192.168.175.111 6379 quorum 2
      22393:X 22 Sep 2019 20:48:11.690 # +sdown master mymaster 192.168.175.111 6379








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

          bind 127.0.0.1 192.168.175.102





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

          bind 127.0.0.1 192.168.175.103





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


[root@redis_sentinel03 ~]# sysctl -a | grep -E  'somaxconn|overcommit_memory|tcp_max_syn_backlog|file-max'
        fs.file-max = 100032   <-------
        net.core.somaxconn = 1024   <-------
        net.ipv4.tcp_max_syn_backlog = 1024   <-------
        sysctl: reading key "net.ipv6.conf.all.stable_secret"
        sysctl: reading key "net.ipv6.conf.default.stable_secret"
        sysctl: reading key "net.ipv6.conf.ens33.stable_secret"
        sysctl: reading key "net.ipv6.conf.lo.stable_secret"
        vm.overcommit_memory = 1   <-------



----------------------------------------------------------------------------------------------------

[root@redis_sentinel01 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'
[root@redis_sentinel02 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'
[root@redis_sentinel03 ~]# su -l redis -s /bin/bash -c 'redis-sentinel /app/redis/conf/sentinel.conf'

[root@redis_sentinel02 ~]# netstat -anptu | grep redis


[root@redis_sentinel02 ~]# ps aux | grep redis

[root@redis_sentinel02 ~]# cat /var/log/redis/redis-sentinel.log




----------------------------------------------------------------------------------------------------



redis-cli -h 192.168.175.101  -p 26379  SENTINEL RESET mymaster
redis-cli -h 192.168.175.102  -p 26379  SENTINEL RESET mymaster
redis-cli -h 192.168.175.103  -p 26379  SENTINEL RESET mymaster


redis-cli -h 192.168.175.101 -a redhat_sentinel -p 5000  shutdown
redis-cli -h 192.168.175.102 -a redhat_sentinel -p 5001  shutdown
redis-cli -h 192.168.175.103 -a redhat_sentinel -p 5002  shutdown




















