

https://redis.io/topics/persistence
http://oldblog.antirez.com/post/redis-persistence-demystified.html


----------------------------------------------------------------------------------------------------
Redis Persistence

Redis provides a different range of persistence options:

  - The RDB persistence performs point-in-time snapshots of your dataset at specified intervals.

  - the AOF persistence logs every write operation received by the server,
    that will be played again at server startup, reconstructing the original dataset.
    Commands are logged using the same format as the Redis protocol itself,
    in an append-only fashion. Redis is able to rewrite the log on background when it gets too big.

  - If you wish, you can disable persistence at all, if you want your data to just exist as long as the server is running.

  - It is possible to combine both AOF and RDB in the same instance. Notice that, in this case,
    when Redis restarts the AOF file will be used to reconstruct
    the original dataset since it is guaranteed to be the most complete.

  可以在 相同的 instance 上 同时结合使用 AOF 和 RDB. 在这种情况下, 当重启(restarts) 时, the AOF file 将被
  用来 重新构建(reconstruct) 原先的(the original) dataset, 因为其能保证是 最多完成的.


----------------------------------------------------------------------------------------------------

RDB 和 AOF 各自的优缺点见 官网:
      https://redis.io/topics/persistence

  大概就是: RDB 更紧凑, 而 AOF 更可靠


AOF 其中的一个优点:
    Redis is able to automatically rewrite the AOF in background when it gets too big.
    The rewrite is completely safe as while Redis continues appending to the old file,
    a completely new one is produced with the minimal set of operations needed to create
    the current data set, and once this second file is ready Redis switches the two and starts appending to the new one.
    // 当 AOF 变得太大时, Redis 可以在后台 自动重写(rewrite) AOF. 使 新生成的 AOF file中的 操作的集合最小化(即合并了某些操作)



----------------------------------------------------------------------------------------------------
Ok, so what should I use?


最佳实践: 为了拥有 可与 PostgreSQL 相当 的 数据安全等级, 最好同时使用 rdb 和 aof 这两种持久化方式.

    The general indication is that you should use both persistence methods
    if you want a degree of data safety comparable to what PostgreSQL can provide you.

    If you care a lot about your data, but still can live with
    a few minutes of data loss in case of disasters, you can simply use RDB alone.

    There are many users using AOF alone, but we discourage it since to have an
    RDB snapshot from time to time is a great idea for doing database backups,
    for faster restarts, and in the event of bugs in the AOF engine.

    Note: for all these reasons we'll likely end up unifying AOF and RDB
    into a single persistence model in the future (long term plan).

    The following sections will illustrate a few more details about the two persistence models.




----------------------------------------------------------------------------------------------------
Snapshotting

      默认文件名: dump.rdb

      可以将其 配置为 在 每 N seconds 中如果至少 有 M 个 keys 修改 则自动 save,
      或 可以使用命令 SAVE 或 BGSAVE 来手动实现

    By default Redis saves snapshots of the dataset on disk, in a binary file called dump.rdb.
    You can configure Redis to have it save the dataset every N seconds
    if there are at least M changes in the dataset, or you can manually call the SAVE or BGSAVE commands.

    For example, this configuration will make Redis automatically dump
    the dataset to disk every 60 seconds if at least 1000 keys changed:

        save 60 1000

    This strategy is known as snapshotting. (快照)



    How it works (Redis 将 数据集(dataset) dump 到 磁盘的 工作方式)
        Whenever Redis needs to dump the dataset to disk, this is what happens:

        - Redis forks. We now have a child and a parent process.
          // 1) Redis forks 一个子进程

        - The child starts to write the dataset to a temporary RDB file.
          // 2) 子进程 将 dataset 写入一个临时的 RDB file

        - When the child is done writing the new RDB file, it replaces the old one.
          // 3) 当子进程写完后, 用该 新的 RDB file 替换掉旧的 RDB file.

    This method allows Redis to benefit from copy-on-write semantics.


----------------------------------------------------------------------------------------------------
Append-only file

    Snapshotting is not very durable. If your computer running Redis stops,
    your power line fails, or you accidentally kill -9 your instance,
    the latest data written on Redis will get lost. While this may not
    be a big deal for some applications, there are use cases
    for full durability, and in these cases Redis was not a viable option.


    The append-only file is an alternative, fully-durable strategy for Redis. It became available in version 1.1.

    You can turn on the AOF in your configuration file:

          appendonly yes


    From now on, every time Redis receives a command that changes the dataset (e.g. SET)
    it will append it to the AOF. When you restart Redis it will re-play the AOF to rebuild the state.


----------------------------------------------------------------------------------------------------
Log rewriting

    As you can guess, the AOF gets bigger and bigger as write operations are performed. For example,
    if you are incrementing a counter 100 times, you'll end up with a single key in your dataset
    containing the final value, but 100 entries in your AOF.
    99 of those entries are not needed to rebuild the current state.

    So Redis supports an interesting feature: it is able to rebuild the AOF in the
    background without interrupting service to clients. Whenever you issue a BGREWRITEAOF
    Redis will write the shortest sequence of commands needed to rebuild the
    current dataset in memory. If you're using the AOF with Redis 2.2 you'll
    need to run BGREWRITEAOF from time to time. Redis 2.4 is able to
    trigger log rewriting automatically (see the 2.4 example configuration file for more information).


  相关参数:
          auto-aof-rewrite-percentage 100
          auto-aof-rewrite-min-size 64mb

  127.0.0.1:6379> help BGREWRITEAOF

    BGREWRITEAOF -
    summary: Asynchronously rewrite the append-only file
    since: 1.0.0
    group: server



----------------------------------------------------------------------------------------------------
How durable is the append only file?

      推荐的策略(也是默认的策略), 即每条一次: appendfsync everysec

You can configure how many times Redis will fsync data on disk. There are three options:

    - appendfsync always: fsync every time a new command is appended to the AOF. Very very slow, very safe.
    - appendfsync everysec: fsync every second. Fast enough (in 2.4 likely to be as fast as snapshotting),
      and you can lose 1 second of data if there is a disaster.
    - appendfsync no: Never fsync, just put your data in the hands of the Operating System.
      The faster and less safe method. Normally Linux will flush data every 30 seconds
      with this configuration, but it's up to the kernel exact tuning.

  The suggested (and default) policy is to fsync every second. It is both very fast and pretty safe.
  The always policy is very slow in practice, but it supports group commit,
  so if there are multiple parallel writes Redis will try to perform a single fsync operation.


----------------------------------------------------------------------------------------------------
What should I do if my AOF gets truncated?

    It is possible that the server crashed while writing the AOF file, or that the volume
    where the AOF file is stored is store was full. When this happens the AOF still
    contains consistent data representing a given point-in-time version of the dataset
    (that may be old up to one second with the default AOF fsync policy),
    but the last command in the AOF could be truncated. The latest major versions
    of Redis will be able to load the AOF anyway, just discarding the last
    non well formed command in the file. In this case the server will emit a log like the following:

    在 最新主版本的 Redis 中,
    如果 AOF file 中 the last command 被截断(如 server 崩溃造成) 而导致 该命令格式不正确,
    则 默认 Redis 仍 能够 加载(load) AOF file, 并 仅仅 抛弃 该 最后 格式不正确的 command.
    在这种情况下, the server 会 发出 如下的 日志记录:

        * Reading RDB preamble from AOF file...
        * Reading the remaining AOF tail...
        # !!! Warning: short read while loading the AOF file !!!
        # !!! Truncating the AOF at offset 439 !!!
        # AOF loaded anyway because aof-load-truncated is enabled

    相关的配置:
        aof-load-truncated yes

You can change the default configuration to force Redis to stop in such cases if you want,
but the default configuration is to continue regardless the fact the last command
in the file is not well-formed, in order to guarantee availabiltiy after a restart.

    // 如下为 老版本 的 Redis 中的解决步骤:
    Older versions of Redis may not recover, and may require the following steps:

          Make a backup copy of your AOF file.
          Fix the original file using the redis-check-aof tool that ships with Redis:

          $ redis-check-aof --fix

          Optionally use diff -u to check what is the difference between two files.

          Restart the server with the fixed file.


----------------------------------------------------------------------------------------------------
What should I do if my AOF gets corrupted?

大体的解决思路就是:
   执行命令 redis-check-aof (注: 不要带选项 --fix), 理解分析问题, 跳到 file 指定的 offset 位置,
   看能否手动修复(注: AOF 使用与 Redis protocol 相同的 format). 如果无法手动修复, 则可以让
   该 工具 为我们解决该问题, 但是在这种情况下, 从 file 中 invalid 的 部分到 文件结尾的 所有AOF portion
   可能会被丢弃, 这将导致 数据丢失.


If the AOF file is not just truncated, but corrupted with invalid byte sequences in the middle,
things are more complex. Redis will complain at startup and will abort:

      * Reading the remaining AOF tail...
      # Bad file format reading the append only file: make a backup of your AOF file, then use ./redis-check-aof --fix <filename>


The best thing to do is to run the redis-check-aof utility, initially without the --fix option,
then understand the problem, jump at the given offset in the file, and see if it is possible
to manually repair the file: the AOF uses the same format of the Redis protocol and
is quite simple to fix manually. Otherwise it is possible to let the utility fix the file for us,
but in that case all the AOF portion from the invalid part to the end of the file
may be discareded, leading to a massive amount of data lost if the
corruption happen to be in the initial part of the file.

How it works

Log rewriting uses the same copy-on-write trick already in use for snapshotting. This is how it works:

    - Redis forks, so now we have a child and a parent process.

    - The child starts writing the new AOF in a temporary file.

    - The parent accumulates all the new changes in an in-memory buffer (but at the same time
      it writes the new changes in the old append-only file, so if the rewriting fails, we are safe).

    - When the child is done rewriting the file, the parent gets a signal, and appends
      the in-memory buffer at the end of the file generated by the child.

    - Profit! Now Redis atomically renames the old file into the new one,
      and starts appending new data into the new file.


----------------------------------------------------------------------------------------------------
Interactions between AOF and RDB persistence


    Redis >= 2.4 makes sure to avoid triggering an AOF rewrite when an RDB snapshotting
    operation is already in progress, or allowing a BGSAVE while the AOF rewrite is in progress.
    This prevents two Redis background processes from doing heavy disk I/O at the same time.

    When snapshotting is in progress and the user explicitly requests a log rewrite operation
    using BGREWRITEAOF the server will reply with an OK status code telling the user
    the operation is scheduled, and the rewrite will start once the snapshotting is completed.

    In the case both AOF and RDB persistence are enabled and Redis restarts the AOF file will be used
    to reconstruct the original dataset since it is guaranteed to be the most complete.






----------------------------------------------------------------------------------------------------








