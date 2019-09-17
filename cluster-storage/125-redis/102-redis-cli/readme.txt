
https://redis.io/topics/rediscli


redis-cli 执行模式:
    交互模式
    非交互模式
    其他特殊模式


REPL: Read Eval Print Loop


// 以非交互模式执行
[root@redis_server ~]# redis-cli  incr mycounter
(integer) 1  <----观察

  注: 如果 stdout 是 tty, 则 redis-cli 默认会输出 对 humans 来说可读性更好的 返回信息,
      否则自动 启用 raw output mode, 如下:

[root@redis_server ~]# redis-cli incr mycounter | cat
2 <----观察(这里因为 stdout 并非 tty, 所以以 raw output mode 方式输出)


[root@redis_server ~]# redis-cli --raw incr mycounter  #使用 选项 --raw 强制启用 raw output
3


[root@redis_server ~]# redis-cli --no-raw incr mycounter | cat  #使用 选项 --no-raw 强制启用 human readable output
(integer) 4


[root@redis_server ~]# redis-cli   #默认等价于 `redis-cli -h 127.0.0.1 -p 6379`

                            -h port|hostname
                            -p port


[root@redis_server ~]# redis-cli -a redhat ping  # 使用 -a 指定 password
Warning: Using a password with '-a' or '-u' option on the command line interface may not be safe.
PONG


// 使用选项 -n 可以指定 database number(即表示 namespace 的 index number)
[root@redis_server ~]# redis-cli flushall   #-n <db>            Database number. the default number 为 zero
1298:M 16 Sep 2019 22:33:00.756 * DB saved on disk
OK

[root@redis_server ~]# redis-cli -n 1 incr a
(integer) 1
[root@redis_server ~]# redis-cli -n 1 incr a
(integer) 2
[root@redis_server ~]# redis-cli -n 2 incr a
(integer) 1


// Some or all of this information can also be provided by using the -u <uri> option and a valid URI:
[root@redis_server ~]# redis-cli -u redis://127.0.0.1:6379/0 ping
PONG

// 此例 将 文件 /etc/services 的内容 作为 foo(key) 的 value
[root@redis_server ~]# redis-cli -x set foo < /etc/services  #-x    Read last argument from STDIN.
OK

[root@redis_server ~]# redis-cli getrange foo 0 50   #GETRANGE语法: GETRANGE key start end, 作用: 获取 substring
"# /etc/services:\n# $Id: services,v 1.55 2013/04/14 "



----------------------------------------------------------------------------------------------------
[root@redis_server ~]# vim /tmp/commands.txt
set foo 100
incr foo
append foo xxx
get foo

// feed redis-cli a sequence of commands written in a text file
[root@redis_server ~]# cat /tmp/commands.txt | redis-cli
OK
(integer) 101
(integer) 6
"101xxx"


// 如果需要, 在 file 中 strings 可以 被 引号 引起来
[root@redis_server ~]# vim /tmp/commands.txt
set foo "This is a single argument"
strlen foo

[root@redis_server ~]# cat /tmp/commands.txt | redis-cli
OK
(integer) 25

----------------------------------------------------------------------------------------------------
Continuously run the same command  连续执行相同的命令

        -r <repeat>        Execute specified command N times.
        -i <interval>      When -r is used, waits <interval> seconds per command.
                           It is possible to specify sub-second times like -i 0.1.



[root@redis_server ~]# redis-cli -r 5 incr foo   #-r <repeat>        Execute specified command N times.
(integer) 1
(integer) 2
(integer) 3
(integer) 4
(integer) 5


// Bug:
//    https://github.com/antirez/redis/issues/6117
//    https://github.com/antirez/redis/pull/5743
// To run the same command forever, use -1 as count. So, in order
// to monitor over time the RSS memory size it's possible to use a command like the following:
[root@redis_server ~]# redis-cli -r -1 -i 1 INFO | grep rss_human   #注: 失败,使用 -r -1 的方式在 redis 5.0.5 版本中存在 bug
失败

----------------------------------------------------------------------------------------------------
Redis Mass Insertion
      https://redis.io/topics/mass-insert

[root@redis_server ~]# for ((i=0; i<99999; i++));
> do
>   echo SET Key${i} Value${i} >> /tmp/data.txt
> done

[root@redis_server ~]# head  -n 5 /tmp/data.txt
SET Key0 Value0
SET Key1 Value1
SET Key2 Value2
SET Key3 Value3
SET Key4 Value4

[root@redis_server ~]# cat /tmp/data.txt | redis-cli --pipe  #可以通过 pipe mode  执行 mass insertion
All data transferred. Waiting for the last reply...
Last reply received from server.
errors: 0, replies: 99999



----------------------------------------------------------------------------------------------------
CSV: Comma Separated Values

[root@redis_server ~]# redis-cli lpush mylist a b c d
(integer) 4
[root@redis_server ~]# redis-cli --csv lrange mylist 0 -1
"d","c","b","a"





----------------------------------------------------------------------------------------------------
Running Lua scripts

[root@redis_server ~]# vim /tmp/script.lua
return redis.call('set',KEYS[1],ARGV[1])


[root@redis_server ~]# redis-cli --eval /tmp/script.lua foo , bar
OK


    对于 更复杂的 工作, Lua debugger 是更适合的选择


----------------------------------------------------------------------------------------------------
Interactive mode (交互模式)

// 最简单的方式进入交互模式
[root@redis_server ~]# redis-cli
127.0.0.1:6379>   <-----观察提示符, 其默认 select 的 database number 为 0

127.0.0.1:6379> select 2
OK
127.0.0.1:6379[2]> dbsize  <----观察, 命令提示符中的 '[2]' 表示 当前处于 index 为 2 的 database(namespace) 上
(integer) 0
127.0.0.1:6379[2]> select 0
OK
127.0.0.1:6379> dbsize
(integer) 100001



----------------------------------------------------------------------------------------------------
Handling connections and reconnections

// 在交互模式中 可使用 命令 connect 连接到 其他 redis 实例
127.0.0.1:6379> connect 192.168.175.139 6379
192.168.175.139:6379> ping
PONG


// 连接到 不可达的 redis 实例 时, redis-cli 会 进入 disconnected mode 且 在执行每个 新命令时 都会尝试 reconnect
127.0.0.1:6379> connect 127.0.0.1 9999
Could not connect to Redis at 127.0.0.1:9999: Connection refused
not connected> ping
Could not connect to Redis at 127.0.0.1:9999: Connection refused
not connected>


// When a reconnection is performed, redis-cli automatically re-select
// the last database number selected. However, all the other state about
// the connection is lost, such as the state of a transaction if we were in the middle of it:
[root@redis_server ~]# redis-cli
127.0.0.1:6379> multi
OK
127.0.0.1:6379> ping
QUEUED

( here the server is manually restarted )


127.0.0.1:6379> exec
(error) ERR EXEC without MULTI
127.0.0.1:6379>


----------------------------------------------------------------------------------------------------
Editing, history and completion

//通过环境变量 REDISCLI_HISTFILE 可以设置 redis 的 history file 的 path.
// 或将其 值 设为 /dev/null 来禁用(disable) history
[root@redis_server ~]# head -n 10 .rediscli_history
        exit
        set name tom
        get name
        exit
        echo 'hello world'
        ping
        ping "hello world"
        quit
        CLIENT LIST
        client list



// 注: 使用 tab 键 可以实现 命令补全


----------------------------------------------------------------------------------------------------
Running the same command N times

// It's possible to run the same command multiple times by prefixing the command name by a number:
// 本例 通过 前缀 一个 number 5 来对 mycounter 执行 5 次加 1 操作
127.0.0.1:6379> 5 incr mycounter
(integer) 1
(integer) 2
(integer) 3
(integer) 4
(integer) 5



----------------------------------------------------------------------------------------------------
Showing help about Redis commands  显示 Redis commands 的 帮助(help)  信息

help @<category> shows all the commands about a given category. The categories are:
                   @generic, @list, @set, @sorted_set, @hash, @pubsub, @transactions,
                   @connection, @server, @scripting, @hyperloglog.

help <commandname> shows specific help for the command given as argument.

注: help 也支持 tab 键 补全

----------------------------------------------------------------------------------------------------
Clearing the terminal screen

127.0.0.1:6379> clear  <-----清理终端屏幕 (注: 快捷键 ctrl + l)



----------------------------------------------------------------------------------------------------
Special modes of operation

  However the CLI performs other auxiliary tasks related to Redis that are explained in the next sections:

      - Monitoring tool to show continuous stats about a Redis server.
      - Scanning a Redis database for very large keys.
      - Key space scanner with pattern matching.
      - Acting as a Pub/Sub client to subscribe to channels.
      - Monitoring the commands executed into a Redis instance.
      - Checking the latency of a Redis server in different ways.
      - Checking the scheduler latency of the local computer.
      - Transferring RDB backups from a remote Redis server locally.
      - Acting as a Redis slave for showing what a slave receives.
      - Simulating LRU workloads for showing stats about keys hits.
      - A client for the Lua debugger.


----------------------------------------------------------------------------------------------------
Continuous stats mode

[root@redis_server ~]# redis-cli --stat   # 以 连续的 stats mode 实时 监视(monitor) Redis instances (默认每秒一次)
      ------- data ------ --------------------- load -------------------- - child -
      keys       mem      clients blocked requests            connections
      5          1.59M    2       0       32 (+0)             3
      5          1.59M    2       0       33 (+1)             3
      5          1.59M    2       0       34 (+1)             3
      5          1.59M    2       0       35 (+1)             3
      5          1.59M    2       0       36 (+1)             3
      5          1.59M    2       0       37 (+1)             3

[root@redis_server ~]# redis-cli -i 2 --stat   #  -i <interval>  本例中频率为每2秒一次
      ------- data ------ --------------------- load -------------------- - child -
      keys       mem      clients blocked requests            connections
      5          1.59M    2       0       38 (+0)             4
      5          1.59M    2       0       39 (+1)             4
      5          1.59M    2       0       40 (+1)             4



----------------------------------------------------------------------------------------------------
Scanning for big keys

    In this special mode, redis-cli works as a key space analyzer.

[root@redis_server ~]# redis-cli --bigkeys

          # Scanning the entire keyspace to find biggest keys as well as
          # average sizes per key type.  You can use -i 0.1 to sleep 0.1 sec
          # per 100 SCAN commands (not usually needed).

          [00.00%] Biggest string found so far 'mycounter' with 1 bytes
          [00.00%] Biggest string found so far 'foo' with 670293 bytes

          -------- summary -------

          Sampled 3 keys in the keyspace!
          Total key length in bytes is 16 (avg len 5.33)

          Biggest string found 'foo' has 670293 bytes

          0 lists with 0 items (00.00% of keys, avg size 0.00)
          0 hashs with 0 fields (00.00% of keys, avg size 0.00)
          3 strings with 670297 bytes (100.00% of keys, avg size 223432.33)
          0 streams with 0 entries (00.00% of keys, avg size 0.00)
          0 sets with 0 members (00.00% of keys, avg size 0.00)
          0 zsets with 0 members (00.00% of keys, avg size 0.00)

127.0.0.1:6379> help SCAN

      SCAN cursor [MATCH pattern] [COUNT count]
      summary: Incrementally iterate the keys space
      since: 2.8.0
      group: generic

  The program uses the SCAN command, so it can be executed against a busy server without impacting the operations,
  however the -i option can be used in order to throttle the scanning process of the specified fraction
  of second for each 100 keys requested. For example, -i 0.1 will slow down the program execution a lot,
  but will also reduce the load on the server to a tiny amount.




----------------------------------------------------------------------------------------------------
Getting a list of keys

      --scan             List all keys using the SCAN command.

  It is also possible to scan the key space, again in a way that does not block the Redis server
  (which does happen when you use a command like KEYS *), and print all the key names,
  or filter them for specific patterns. This mode, like the --bigkeys option,
  uses the SCAN command, so keys may be reported multiple times if the dataset is changing,
  but no key would ever be missing, if that key was present since the start of the iteration.
  Because of the command that it uses this option is called --scan.


[root@redis_server ~]# redis-cli --scan | head -10
mycounter
foo
name

[root@redis_server ~]# redis-cli --scan --pattern '*o*'
mycounter
foo

[root@redis_server ~]# redis-cli --scan --pattern '*o*' | wc -l
2



----------------------------------------------------------------------------------------------------
Pub/sub mode  发布/订阅 模式

注: 发布, 订阅 相关的命令 在 交互模式 或 非交互模式下 都可以执行

// 查看一下相关命令
127.0.0.1:6379> help @pubsub

        PSUBSCRIBE pattern [pattern ...]
        summary: Listen for messages published to channels matching the given patterns
        since: 2.0.0

        PUBLISH channel message
        summary: Post a message to a channel
        since: 2.0.0

        PUBSUB subcommand [argument [argument ...]]
        summary: Inspect the state of the Pub/Sub subsystem
        since: 2.8.0

        PUNSUBSCRIBE [pattern [pattern ...]]
        summary: Stop listening for messages posted to channels matching the given patterns
        since: 2.0.0

        SUBSCRIBE channel [channel ...]
        summary: Listen for messages published to the given channels
        since: 2.0.0

        UNSUBSCRIBE [channel [channel ...]]
        summary: Stop listening for messages posted to the given channels
        since: 2.0.0


[root@redis_server ~]# redis-cli psubscribe '*'   #订阅所有频道(channels) 的 messages
Reading messages... (press Ctrl-C to quit)  <----观察
1) "psubscribe"
2) "*"
3) (integer) 1
1) "pmessage"  <----注: 该行及如下几行为 如下的 PUBLISH 命令发布消息后产生的变化信息
2) "*"         <----
3) "mychannel" <----
4) "mymessage" <----

[root@redis_server ~]# redis-cli PUBLISH mychannel mymessage  #向频道(channels) 'mychannel' 发送 消息(message) 'mymessage'
(integer) 1




----------------------------------------------------------------------------------------------------
Monitoring commands executed in Redis


[root@redis_server ~]# redis-cli monitor  #It will print all the commands received by a Redis instance
OK
1568702240.837898 [0 127.0.0.1:55660] "ping"



[root@redis_server ~]# redis-cli monitor | grep -i set   #注: 还可以将 monitor 与 pipe(管道) 结合使用
      1568702417.931401 [0 127.0.0.1:55684] "set" "name" "Tom"
      1381:M 17 Sep 2019 14:40:17.966 * 1 changes in 900 seconds. Saving...
      1381:M 17 Sep 2019 14:40:17.967 * Background saving started by pid 1493
      1493:C 17 Sep 2019 14:40:17.971 * DB saved on disk
      1493:C 17 Sep 2019 14:40:17.972 * RDB: 0 MB of memory used by copy-on-write
      1381:M 17 Sep 2019 14:40:18.068 * Background saving terminated with success



----------------------------------------------------------------------------------------------------
Monitoring the latency of Redis instances  监视延迟


// The basic latency checking tool is the --latency option. Using this option
// the CLI runs a loop where the PING command is sent to the Redis instance,
// and the time to get a reply is measured. This happens 100 times per second,
// and stats are updated in a real time in the console:
[root@redis_server ~]# redis-cli --latency
      min: 0, max: 2, avg: 0.18 (911 samples)^C


  Usually, the average latency of a very fast instance tends to be overestimated a bit because of
  the latency due to the kernel scheduler of the system running redis-cli itself, so the average
  latency of 0.19 above may easily be 0.01 or less. However this is usually not a big problem,
  since we are interested in events of a few millisecond or more.


[root@redis_server ~]# redis-cli --latency-history   #it works exactly like --latency, but every 15 seconds (by default) a new sampling session is started from scratch
    min: 0, max: 3, avg: 0.19 (1259 samples) -- 15.01 seconds range
    min: 0, max: 2, avg: 0.20 (1225 samples) -- 15.01 seconds range
    min: 0, max: 1, avg: 0.17 (665 samples)^C


[root@redis_server ~]# redis-cli -i 2 --latency-history  #还可以通过 -i <interval> 指定 session 时长
    min: 0, max: 2, avg: 0.22 (172 samples) -- 2.01 seconds range
    min: 0, max: 1, avg: 0.17 (173 samples) -- 2.01 seconds range
    min: 0, max: 1, avg: 0.15 (183 samples) -- 2.01 seconds range
    min: 0, max: 1, avg: 0.18 (34 samples)^C










----------------------------------------------------------------------------------------------------




