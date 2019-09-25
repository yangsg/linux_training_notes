

https://www.memcached.org/
https://www.memcached.org/about
https://github.com/memcached/memcached/wiki
https://github.com/memcached/memcached

http://www.runoob.com/memcached/memcached-tutorial.html
https://www.cnblogs.com/loveis715/p/4681643.html


memcached 的下载页面
    https://github.com/memcached/memcached/releases
    https://www.memcached.org/downloads
    https://github.com/memcached/memcached/wiki/ReleaseNotes


memcached 依赖的 libevent 库下载页面:
    https://github.com/libevent/libevent/releases

----------------------------------------------------------------------------------------------------
Redis 和 Memcached 区别 和 比较 的网上资料

  注: 通常来说, redis 可能是更好的选择

  注: Memcached 可以缓存图片
        http://blog.chinaunix.net/uid-29380389-id-4339117.html
        https://www.iteye.com/blog/zhangjialu-vip-1167345



    中文:
        https://www.cnblogs.com/JavaBlackHole/p/7726195.html
        https://www.jianshu.com/p/3a6e099bb3eb
        http://www.sohu.com/a/234779580_130419
        https://blog.csdn.net/qq_34126805/article/details/81748107
        https://blog.csdn.net/huxianbo0807/article/details/79953766
    英文:
        https://stackoverflow.com/questions/10558465/memcached-vs-redis
        https://aws.amazon.com/cn/elasticache/redis-vs-memcached/
        https://blog.eduonix.com/web-programming-tutorials/redis-memcached-select-caching-strategy/
        https://www.linkedin.com/pulse/memcached-vs-redis-which-one-pick-ranjeet-vimal



Choosing between Redis and Memcached  https://aws.amazon.com/cn/elasticache/redis-vs-memcached/
      ---------------------------------------------------------------------------------
                                                                 Memcached    Redis
      ---------------------------------------------------------------------------------
              Sub-millisecond latency                               Yes        Yes
              Developer ease of use                                 Yes        Yes
              Data partitioning                                     Yes        Yes
              Support for a broad set of programming languages      Yes        Yes
              Advanced data structures                               -         Yes
              Multithreaded architecture                            Yes         -
              Snapshots                                              -         Yes
              Replication                                            -         Yes
              Transactions                                           -         Yes
              Pub/Sub                                                -         Yes
              Lua scripting                                          -         Yes
              Geospatial support                                     -         Yes
      ---------------------------------------------------------------------------------


      新浪基于 memcached 的二次开发产品: memcachedb  特点之一: 支持持久化
          https://baike.baidu.com/item/memcached
          https://blog.csdn.net/xinguan1267/article/details/7576982
          https://blog.csdn.net/zhu_tianwei/article/details/44860129


----------------------------------------------------------------------------------------------------


[root@memcached_server ~]# mkdir /app


// 安装基础编译构建环境
[root@memcached_server ~]# yum -y install gcc gcc-c++ autoconf automake


[root@memcached_server ~]# mkdir download
[root@memcached_server ~]# cd download/

// 安装 memcached 依赖的 libevent 库
// 参考 https://github.com/libevent/libevent
[root@memcached_server download]# wget https://github.com/libevent/libevent/releases/download/release-2.1.11-stable/libevent-2.1.11-stable.tar.gz
[root@memcached_server download]# ls
      libevent-2.1.11-stable.tar.gz
[root@memcached_server download]# tar -xvf libevent-2.1.11-stable.tar.gz
[root@memcached_server download]# cd libevent-2.1.11-stable/
[root@memcached_server libevent-2.1.11-stable]# ./configure --prefix=/app/libevent
[root@memcached_server libevent-2.1.11-stable]# make
[root@memcached_server libevent-2.1.11-stable]# make install

[root@memcached_server libevent-2.1.11-stable]# ls /app/libevent/
        bin  include  lib




// 安装 memcached
// 参考 https://github.com/memcached/memcached/wiki/Install
//      https://github.com/memcached/memcached
//      https://github.com/memcached/memcached/releases
[root@memcached_server download]# wget -O memcached-1.5.18.tar.gz  https://github.com/memcached/memcached/archive/1.5.18.tar.gz
[root@memcached_server download]# ls -1
        libevent-2.1.11-stable
        libevent-2.1.11-stable.tar.gz
        memcached-1.5.18.tar.gz  <-----

[root@memcached_server download]# tar -xvf memcached-1.5.18.tar.gz
[root@memcached_server download]# cd memcached-1.5.18/
[root@memcached_server memcached-1.5.18]# ls | grep -E -i 'configure|\.sh'
        autogen.sh  <------可以发现不存在 configure 可执行文件, 则 使用 autogen.sh 生成
        configure.ac
        version.sh

// 生成 可执行文件 configure
[root@memcached_server memcached-1.5.18]# ./autogen.sh

// 查看一下 configure 相关的 options
[root@memcached_server memcached-1.5.18]# ./configure --help
[root@memcached_server memcached-1.5.18]# ./configure --prefix=/app/memcached  --with-libevent=/app/libevent/
[root@memcached_server memcached-1.5.18]# make
[root@memcached_server memcached-1.5.18]# make install


[root@memcached_server memcached-1.5.18]# tree /app/memcached/
      /app/memcached/
      ├── bin
      │   └── memcached
      ├── include
      │   └── memcached
      │       └── protocol_binary.h
      └── share
          └── man
              └── man1
                  └── memcached.1

// 观察一下 memcached 可用的 某项 options 及其 default value
[root@memcached_server memcached-1.5.18]# /app/memcached/bin/memcached --help
      memcached UNKNOWN
      -p, --port=<num>          TCP port to listen on (default: 11211)   <--------------------
      -U, --udp-port=<num>      UDP port to listen on (default: 0, off)
      -s, --unix-socket=<file>  UNIX socket to listen on (disables network support)
      -A, --enable-shutdown     enable ascii "shutdown" command
      -a, --unix-mask=<mask>    access mask for UNIX socket, in octal (default: 0700)
      -l, --listen=<addr>       interface to listen on (default: INADDR_ANY)  <--------------------
      -d, --daemon              run as a daemon  <--------------------
      -r, --enable-coredumps    maximize core file limit
      -u, --user=<user>         assume identity of <username> (only when run as root)  <--------------------
      -m, --memory-limit=<num>  item memory in megabytes (default: 64 MB)   <--------------------
      -M, --disable-evictions   return error on memory exhausted instead of evicting
      -c, --conn-limit=<num>    max simultaneous connections (default: 1024)  <--------------------
      -k, --lock-memory         lock down all paged memory
      -v, --verbose             verbose (print errors/warnings while in event loop)
      -vv                       very verbose (also print client commands/responses)
      -vvv                      extremely verbose (internal state transitions)
      -h, --help                print this help and exit
      -i, --license             print memcached and libevent license
      -V, --version             print version and exit
      -P, --pidfile=<file>      save PID in <file>, only used with -d option  <--------------------
      -f, --slab-growth-factor=<num> chunk size growth factor (default: 1.25) <--------------------
      -n, --slab-min-size=<bytes> min space used for key+value+flags (default: 48) <--------------------
      -L, --enable-largepages  try to use large memory pages (if available)
      -D <char>     Use <char> as the delimiter between key prefixes and IDs.
                    This is used for per-prefix stats reporting. The default is
                    ":" (colon). If this option is specified, stats collection
                    is turned on automatically; if not, then it may be turned on
                    by sending the "stats detail on" command to the server.
      -t, --threads=<num>       number of threads to use (default: 4)  <--------------------
      -R, --max-reqs-per-event  maximum number of requests per event, limits the
                                requests processed per connection to prevent
                                starvation (default: 20)
      -C, --disable-cas         disable use of CAS
      -b, --listen-backlog=<num> set the backlog queue limit (default: 1024)  <--------------------
      -B, --protocol=<name>     protocol - one of ascii, binary, or auto (default)
      -I, --max-item-size=<num> adjusts max item size
                                (default: 1mb, min: 1k, max: 1024m)
      -F, --disable-flush-all   disable flush_all command
      -X, --disable-dumping     disable stats cachedump and lru_crawler metadump
      -Y, --auth-file=<file>    (EXPERIMENTAL) enable ASCII protocol authentication. format:
                                user:pass\nuser2:pass2\n
      -e, --memory-file=<file>  (EXPERIMENTAL) mmap a file for item memory.
                                use only in ram disks or persistent memory mounts!
                                enables restartable cache (stop with SIGUSR1)
      -o, --extended            comma separated list of extended options
                                most options have a 'no_' prefix to disable
         - maxconns_fast:       immediately close new connections after limit
         - hashpower:           an integer multiplier for how large the hash
                                table should be. normally grows at runtime.
                                set based on "STAT hash_power_level"
         - tail_repair_time:    time in seconds for how long to wait before
                                forcefully killing LRU tail item.
                                disabled by default; very dangerous option.
         - hash_algorithm:      the hash table algorithm
                                default is murmur3 hash. options: jenkins, murmur3
         - lru_crawler:         enable LRU Crawler background thread
         - lru_crawler_sleep:   microseconds to sleep between items
                                default is 100.
         - lru_crawler_tocrawl: max items to crawl per slab per run
                                default is 0 (unlimited)
         - lru_maintainer:      enable new LRU system + background thread
         - hot_lru_pct:         pct of slab memory to reserve for hot lru.
                                (requires lru_maintainer)
         - warm_lru_pct:        pct of slab memory to reserve for warm lru.
                                (requires lru_maintainer)
         - hot_max_factor:      items idle > cold lru age * drop from hot lru.
         - warm_max_factor:     items idle > cold lru age * this drop from warm.
         - temporary_ttl:       TTL's below get separate LRU, can't be evicted.
                                (requires lru_maintainer)
         - idle_timeout:        timeout for idle connections
         - slab_chunk_max:      (EXPERIMENTAL) maximum slab size. use extreme care.
         - watcher_logbuf_size: size in kilobytes of per-watcher write buffer.
         - worker_logbuf_size:  size in kilobytes of per-worker-thread buffer
                                read by background thread, then written to watchers.
         - track_sizes:         enable dynamic reports for 'stats sizes' command.
         - no_hashexpand:       disables hash table expansion (dangerous)
         - modern:              enables options which will be default in future.
                   currently: nothing
         - no_modern:           uses defaults of previous major version (1.4.x)




[root@memcached_server ~]# useradd -M -s /sbin/nologin  memcached
[root@memcached_server ~]# /app/memcached/bin/memcached -l 192.168.175.130 -p 11211 -u memcached -m 800M -n 50 -f 2 -vv

        slab class   1: chunk size       104 perslab   10082
        slab class   2: chunk size       208 perslab    5041
        slab class   3: chunk size       416 perslab    2520
        slab class   4: chunk size       832 perslab    1260
        slab class   5: chunk size      1664 perslab     630
        slab class   6: chunk size      3328 perslab     315
        slab class   7: chunk size      6656 perslab     157
        slab class   8: chunk size     13312 perslab      78
        slab class   9: chunk size     26624 perslab      39
        slab class  10: chunk size     53248 perslab      19
        slab class  11: chunk size    106496 perslab       9
        slab class  12: chunk size    212992 perslab       4
        slab class  13: chunk size    524288 perslab       2
        <26 server listening (auto-negotiate)



[root@memcached_server ~]# netstat -anptu | grep memcached
      tcp        0      0 192.168.175.130:11211   0.0.0.0:*               LISTEN      28431/memcached


[root@memcached_server ~]# ps aux | grep memcached
      memcach+  28431  0.0  0.1 413924  1348 pts/1    Sl+  17:53   0:00 /app/memcached/bin/memcached -l 192.168.175.130 -p 11211 -u memcached -m 800M -n 50 -f 2 -vv




----------------------------------------------------------------------------------------------------
测试:

----------------------------------------
// 使用 telnet 测试
[root@memcached_server ~]# yum -y install telnet

[root@memcached_server ~]# telnet 192.168.175.130 11211
      Trying 192.168.175.130...
      Connected to 192.168.175.130.
      Escape character is '^]'.
      set name 0 20 6   <===========输入
      martin            <===========输入
      STORED
      get name          <===========输入
      VALUE name 0 6
      martin
      END
      set name 0 10 6   <===========输入
      martin            <===========输入
      STORED
      get name          <===========输入
      END
      quit              <===========输入(退出)
      Connection closed by foreign host.


----------------------------------------
php连接memcachced

[root@memcached_server ~]# yum install -y httpd php php-gd gd php-mysql mariadb-server php-pecl-memcache

[root@memcached_server ~]# php -m | grep memca
    memcache

[root@memcached_server ~]# vim /var/www/html/test_memcached.php

      <?php
        $memcache_obj = memcache_connect('192.168.175.130', 11211);
        $memcache_obj->add("name", "test");
        echo $memcache_obj->get("name");
      ?>


// 演示一下直接在 命令行 上 执行 php 脚本
[root@memcached_server ~]# php -f /var/www/html/test_memcached.php
      test


注: 如果仅想在 command line 中执行 最基本的(即没有使用特殊的 module) php 代码, 在centos7 中仅安装  php-cli package 就可以了
      https://www.php.net/manual/en/features.commandline.php



----------------------------------------------------------------------------------------------------
网上资料:

  java 连接 memcached 的方式见:
      https://www.runoob.com/memcached/java-memcached.html


  https://www.php.net/manual/zh/book.memcache.php







