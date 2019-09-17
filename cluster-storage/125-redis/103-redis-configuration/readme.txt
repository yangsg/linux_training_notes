
https://redis.io/topics/config


----------------------------------------------------------------------------------------------------
尽管 redis 能够不 使用 a configuration file 而仅使用 a built-in default configuration 来启动,
但 建议 这种方式 仅限于 testing 和 development 的目的 而使用.

更恰当的方式  是 为 redis 提供名为 redis.conf 的配置文件, 该文件中包含了 redis 的配置指令(directives)

其语法格式如下:
      keyword argument1 argument2 ... argumentN
如:
      slaveof 127.0.0.1 6380
      requirepass "hello world"



各 redis 版本 自带的 redis.conf 样例文件如下:

The self documented redis.conf for Redis 4.0.   https://raw.githubusercontent.com/antirez/redis/4.0/redis.conf
The self documented redis.conf for Redis 3.2.   https://raw.githubusercontent.com/antirez/redis/3.2/redis.conf
The self documented redis.conf for Redis 3.0.   https://raw.githubusercontent.com/antirez/redis/3.0/redis.conf


----------------------------------------------------------------------------------------------------
Passing arguments via the command line

    通常 用于 测试 场景

例如:
      ./redis-server --port 6380 --slaveof 127.0.0.1 6379


  The format of the arguments passed via the command line is exactly the same as the
  one used in the redis.conf file, with the exception that the keyword is prefixed with --.

  Note that internally this generates an in-memory temporary config file (possibly concatenating
  the config file passed by the user if any) where arguments are translated into the format of redis.conf.

----------------------------------------------------------------------------------------------------
Changing Redis configuration while the server is running


It is possible to reconfigure Redis on the fly without stopping and restarting the service,
or querying the current configuration programmatically using the special commands CONFIG SET and CONFIG GET


    CONFIG SET
          https://redis.io/commands/config-set

    CONFIG GET
          https://redis.io/commands/config-get



注: 并非所有的 configuration directives 都支持这种在线 reconfigure 的方式, 但是大多数都是支持的
注：这种方式修改仅为临时修改, 重启 redis 后 其仍然会去使用 old configuration


如果想要持久化的修改配置, 你可以 直接手动修改文件 redis.conf,
或者使用 命令 CONFIG REWRITE, which will automatically scan your redis.conf file
and update the fields which don't match the current configuration value.
Fields non existing but set to the default value are not added.
Comments inside your configuration file are retained.


[root@redis_server ~]# redis-cli

      127.0.0.1:6379> help CONFIG SET

        CONFIG SET parameter value
        summary: Set a configuration parameter to the given value
        since: 2.0.0
        group: server

      127.0.0.1:6379> help CONFIG GET

        CONFIG GET parameter
        summary: Get the value of a configuration parameter
        since: 2.0.0
        group: server

      127.0.0.1:6379> CONFIG GET maxmemory
      1) "maxmemory"
      2) "0"      <-----观察一下默认的 maxmemory  设置

      127.0.0.1:6379> CONFIG GET maxmemory-policy
      1) "maxmemory-policy"
      2) "noeviction"  <-----观察一下默认的 maxmemory-policy 设置

      127.0.0.1:6379> CONFIG SET maxmemory 1024mb
      OK
      127.0.0.1:6379> CONFIG GET maxmemory
      1) "maxmemory"
      2) "1073741824"

      127.0.0.1:6379> CONFIG SET maxmemory-policy allkeys-lru
      OK
      127.0.0.1:6379> CONFIG GET maxmemory-policy
      1) "maxmemory-policy"
      2) "allkeys-lru"




----------------------------------------------------------------------------------------------------
https://redis.io/topics/lru-cache


