

127.0.0.1:6379> help     <===查看帮助
        redis-cli 5.0.5
        To get help about Redis commands type:
              "help @<group>" to get a list of commands in <group>
              "help <command>" for help on <command>
              "help <tab>" to get a list of possible help topics
              "quit" to exit

        To set redis-cli preferences:
              ":set hints" enable online hints
              ":set nohints" disable online hints
        Set your preferences in ~/.redisclirc

127.0.0.1:6379> help auth   <====查看指令 auth 的帮助

        AUTH password
        summary: Authenticate to the server
        since: 1.0.0
        group: connection




// 认证 (需要在 requirepass Redis server 的配置文件中使用 requirepass directive)
127.0.0.1:6379> auth redhat
OK

127.0.0.1:6379> echo 'hello world'
"hello world"

// This command is often used to test if a connection is still alive, or to measure latency.
127.0.0.1:6379> ping
PONG
127.0.0.1:6379> ping "hello world"
"hello world"


// Ask the server to close the connection.
127.0.0.1:6379> ping "hello world"
"hello world"



// 关于 redis 中的 逻辑数据库 或 名字空间
// https://redis.io/commands/select
// Select the Redis logical database having the specified zero-based numeric index. New connections always use the database 0.
// Redis different selectable databases are a form of namespacing: all the databases
// are anyway persisted together in the same RDB / AOF file. However different databases can
// have keys having the same name, and there are commands available like
// FLUSHDB, SWAPDB or RANDOMKEY that work on specific databases.
// 当使用 Redis Cluster 是, 命令 SELECT 不能被使用, 因为 Redis Cluster 仅支持 database zero (即 index 为 0 的数据库/名字空间)
// When using Redis Cluster, the SELECT command cannot be used, since Redis Cluster only supports database zero.

127.0.0.1:6379> select 2     <=====选择 index 为 2 的 database
OK
127.0.0.1:6379[2]> select 0  <=====选择 index 为 0 的 database(注:通过命令提示符, 可以知道当前所处的database)
OK
127.0.0.1:6379>



127.0.0.1:6379> client list  <====获取 client connections 列表
id=4 addr=127.0.0.1:48326 fd=7 name= age=379 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=26 qbuf-free=32742 obl=0 oll=0 omem=0 events=r cmd=client








