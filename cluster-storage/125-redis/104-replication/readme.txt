

https://redis.io/topics/replication


注: 强烈建议开启 master 和 slaves 上的 持久化功能(同时包括 rdb 和 aof 文件)

此处仅涉及基本的 master-slave replication, 不包括 Sentinel or Redis Cluster




This system works using three main mechanisms:

    1) When a master and a slave instances are well-connected, the master keeps the
       slave updated by sending a stream of commands to the slave, in order to
       replicate the effects on the dataset happening in the master side due to:
       client writes, keys expired or evicted, any other action changing the master dataset.

    2) When the link between the master and the slave breaks, for network issues
       or because a timeout is sensed in the master or the slave, the slave reconnects
       and attempts to proceed with a partial resynchronization: it means that it
       will try to just obtain the part of the stream of commands it missed during the disconnection.

    3) When a partial resynchronization is not possible, the slave will ask for
       a full resynchronization. This will involve a more complex process in which
       the master needs to create a snapshot of all its data, send it to the slave,
       and then continue sending the stream of commands as the dataset changes.


  Redis uses by default asynchronous replication(默认采用异步复制), which being low latency and high performance,
  is the natural replication mode for the vast majority of Redis use cases.

  Synchronous replication of certain data can be requested by the clients using the WAIT command(WAIT 命令).



关于 Redis replication 的 一些重要事实:
The following are some very important facts about Redis replication:

    - Redis uses asynchronous replication, with asynchronous slave-to-master acknowledges of the amount of data processed.
      // Redis 采用 异步复制, 以及 从 slave 到 master 的 处理的数据量 的 异步确认.
    - A master can have multiple slaves.
      // 支持 一主多从
    - Slaves are able to accept connections from other slaves. Aside from connecting a number of
      slaves to the same master, slaves can also be connected to other slaves in a cascading-like structure.
      Since Redis 4.0, all the sub-slaves will receive exactly the same replication stream from the master.
      // redis 支持 slave 的级联复制

    - Redis replication is non-blocking on the master side. This means that the master will continue
      to handle queries when one or more slaves perform the initial synchronization or a partial resynchronization.
      // Redis replication 在 master 端是 非阻塞的(non-blocking), 这意味着 the master 在 当 其 一个 或 更多个 slaves
      // 执行 the initial synchronization or a partial resynchronization 时 仍将继续 handle queries


    - Replication is also largely non-blocking on the slave side. While the slave is performing
      the initial synchronization, it can handle queries using the old version of the dataset,
      assuming you configured Redis to do so in redis.conf. Otherwise, you can configure
      Redis slaves to return an error to clients if the replication stream is down.
      However, after the initial sync, the old dataset must be deleted and the new
      one must be loaded. The slave will block incoming connections during this brief
      window (that can be as long as many seconds for very large datasets).
      Since Redis 4.0 it is possible to configure Redis so that the deletion
      of the old data set happens in a different thread, however loading
      the new initial dataset will still happen in the main thread and block the slave.
      // 在 slave 端的 replication 很大程度上也是 non-blocking 的. 当 the slave 在执行
      // the initial synchronization 时, 其 可以使用 the old version of the dataset 来
      // handle queries, 假设你在 redis.conf 配置了这样的行为. 否则, 你可以将 Redis slaves 配置为
      // 在 the replication stream 被 down 掉时 想 client 返回 一个 error. 然而, 在the initial sync 之后,
      // the old dataset 必须被删除 且 the new one 必须被加载(loaded).The slave will block incoming connections during this brief
      // window (that can be as long as many seconds for very large datasets).
      // 从 Redis 4.0 起, 可以将 Redis 配置为 在一个 不同的 线程(thread) 中来实现 the old dataset 的删除(deletion),
      // 但是, the new initial dataset 的加载仍 发生在 main thread 中 且 会 阻塞 the slave.


    - Replication can be used both for scalability, in order to have multiple slaves for
      read-only queries (for example, slow O(N) operations can be offloaded to slaves),
      or simply for improving data safety and high availability.

    - It is possible to use replication to avoid the cost of having the master writing the full dataset to disk:
      a typical technique involves configuring your master redis.conf to avoid persisting to disk at all,
      then connect a slave configured to save from time to time, or with AOF enabled.
      However this setup must be handled with care, since a restarting master will start
      with an empty dataset: if the slave tries to synchronized with it, the slave will be emptied as well.
      // 最好(强烈建议)开启 master 和 slaves 上的 持久化 功能(因为如果没有开启持久化功能, 则 重启 master 时 会以 an empty dataset 来启动,
      // 如果此时 the slave 尝试同步操作， 则 the slave 也会被 清空)








----------------------------------------------------------------------------------------------------
How Redis replication works

    Every Redis master has a replication ID: it is a large pseudo random string
    that marks a given story of the dataset. Each master also takes an offset
    that increments for every byte of replication stream that it is produced
    to be sent to slaves, in order to update the state of the slaves with
    the new changes modifying the dataset. The replication offset is
    incremented even if no slave is actually connected, so basically every given pair of:


        Replication ID, offset  注:  Replication ID 和 offset 共同标志了 master 上 dataset 的确切版本

      +--------+                                                                           +-------+
      | master |                                                                           | slave |
      +--------+                                                                           +-------+
          |                                                                                    |
          |----+                                                                               |
          |    |take replication ID and update offset                                          |
          |    |                                                                               |
          |<---+                                                                               |
          |                                                                                    |
          |                                                                                    |
          | send(by psync) old master replication ID and offset that slave processed so far    |
          |<-----------------------------------------------------------------------------------|
          |                                                                                    |
          |----+                                                                               |
          |    |compare with old replication ID and offset                                     |
          |    |                                                                               |
          |<---+                                                                               |
          |                                                                                    |
          |                                                                                    |
          |   if possible, perform a partial sync, else perform a full sync                    |
          |----------------------------------------------------------------------------------->|
          |                                                                                    |
          |                                                                                    |
          |                                                                                    |
          |                                                                                    |


    Identifies an exact version of the dataset of a master.

    When slaves connects to masters, they use the PSYNC command in order to
    send their old master replication ID and the offsets they processed so far.
    This way the master can send just the incremental part needed. However if
    there is not enough backlog in the master buffers, or if the slave is
    referring to an history (replication ID) which is no longer known,
    than a full resynchronization happens: in this case the slave will get a full copy of the dataset, from scratch.

This is how a full synchronization works in more details:

    The master starts a background saving process in order to produce an RDB file.
    At the same time it starts to buffer all new write commands received from the clients.
    When the background saving is complete, the master transfers the database file to the slave,
    which saves it on disk, and then loads it into memory. The master will then send all
    buffered commands to the slave. This is done as a stream of commands
    and is in the same format of the Redis protocol itself.

    // The master 启动一个 后台 saving process 来生成 an RDB file.
    // 与此同时, 它 还会开始缓存(buffer) 所有从 clients 接受到的 new write commands.
    // 当 the background saving 完成(complete), the master transfers the database file to the slave,
    // which saves it on disk, and then loads it into memory. The master 然后将 所有缓存的commands
    // 发送到 the slave. 这是以 命令流(a stream of commands) 的方式完成的 且 格式与 Redis protocol 本身
    // 的格式相同.

    You can try it yourself via telnet. Connect to the Redis port while the server
    is doing some work and issue the SYNC command. You'll see a bulk transfer
    and then every command received by the master will be re-issued in the telnet session.
    Actually SYNC is an old protocol no longer used by newer Redis instances,
    but is still there for backward compatibility:
    it does not allow partial resynchronizations, so now PSYNC is used instead.

    As already said, slaves are able to automatically reconnect when the master-slave
    link goes down for some reason. If the master receives multiple concurrent
    slave synchronization requests, it performs a single background save in order to serve all of them.




----------------------------------------------------------------------------------------------------
Replication ID explained

    In the previous section we said that if two instances have the same replication ID and replication offset,
    they have exactly the same data. However it is useful to understand what exctly is the replication ID,
    and why instances have actually two replication IDs the main ID and the secondary ID.

    // 每次 redis 实例 作为 a master 从无到有, 从头开始(from scratch) 重新启动 或 a slave 被提升为 master 时,
    // 都会为该实例生成一个 新的 复制 ID(a new replication ID)
    A replication ID basically marks a given history of the data set. Every time an instance
    restarts from scratch as a master, or a slave is promoted to master, a new replication ID
    is generated for this instance. The slaves connected to a master will inherit its
    replication ID after the handshake. So two instances with the same ID are related
    by the fact that they hold the same data, but potentially at a different time.
    It is the offset that works as a logical time to understand,
    for a given history (replication ID) who holds the most updated data set.

    For instance if two instances A and B have the same replication ID, but one with offset 1000
    and one with offset 1023, it means that the first lacks certain commands applied to the data set.
    It also means that A, by applying just a few commands, may reach exactly the same state of B.

    The reason why Redis instances have two replication IDs is because of slaves that
    are promoted to masters. After a failover, the promoted slave requires to still
    remember what was its past replication ID, because such replication ID was
    the one of the former master. In this way, when other slaves will synchronize
    with the new master, they will try to perform a partial resynchronization
    using the old master replication ID. This will work as expected, because
    when the slave is promoted to master it sets its secondary ID to its main ID,
    remembering what was the offset when this ID switch happend. Later it will
    select a new random replication ID, because a new history begins. When handling
    the new slaves connecting, the master will match their IDs and offsets
    both with the current ID and the secondary ID (up to a given offset, for safety).
    In short this means that after a failover, slaves connecting to
    the new promoted master don't have to perform a full sync.

    In case you wonder why a slave promoted to master needs to change its replication ID after a failover:
    it is possible that the old master is still working as a master because of some network partition:
    retaining the same replication ID would violate the fact that the
    same ID and same offset of any two random instances mean they have the same data set.









----------------------------------------------------------------------------------------------------
Configuration

在 slave 的配置文件中配置, 如:

    slaveof 192.168.1.1 6379

当然, 也可以使用 SLAVEOF 命令来配置


与 replication 相关的其他参数(parameters)或选项:
    repl-backlog-size

    repl-diskless-sync
    repl-diskless-sync-delay



----------------------------------------------------------------------------------------------------
Read-only slave

      Since Redis 2.6, slaves support a read-only mode that is enabled by default.


    slave-read-only


DEBUG or CONFIG
rename-command

    Redis 4.0 RC3 and greater versions totally solve this problem and now writable slaves
    are able to evict keys with TTL as masters do, with the exceptions of keys
    written in DB numbers greater than 63 (but by default Redis instances only have 16 databases).


Also note that since Redis 4.0 slave writes are only local, and are not propagated
to sub-slaves attached to the instance. Sub slaves instead will always receive
the replication stream identical to the one sent by the top-level master
to the intermediate slaves. So for example in the following setup:

      A ---> B ---> C  即如果 slave B 可写,其也仅是 local 的.其写入的修改无法传播给
                       作为 sub-slaves 的 C. C 仅能看到 作为 top-level master 的 A 的 dataset.

Even if B is writable, C will not see B writes and will
instead have identical dataset as the master instance A.



----------------------------------------------------------------------------------------------------
Setting a slave to authenticate to a master


如果 master 通过 requirepass 设置了 password, 则 slave 需要使用 此 password 来执行所有的 同步操作.


临时设置:
    config set masterauth <password>

在 config file 中 永久(持久化)设置:
    masterauth <password>


----------------------------------------------------------------------------------------------------
Allow writes only with N attached replicas

    min-slaves-to-write <number of slaves>
    min-slaves-max-lag <number of seconds>


----------------------------------------------------------------------------------------------------
How Redis replication deals with expires on keys


----------------------------------------------------------------------------------------------------
Configuring replication in Docker and NAT

    slave-announce-ip 5.5.5.5
    slave-announce-port 1234

redis 5.0.5 版本中使用:
    replica-announce-ip 5.5.5.5
    replica-announce-port 1234


相关命令: info 和 role


----------------------------------------------------------------------------------------------------
The INFO and ROLE command

INFO replication


----------------------------------------------------------------------------------------------------
Partial resynchronizations after restarts and failovers


    Since Redis 4.0, when an instance is promoted to master after a failover,
    it will be still able to perform a partial resynchronization with the slaves of the old master.
    To do so, the slave remembers the old replication ID and offset of its former master,
    so can provide part of the backlog to the connecting slaves even if they ask for the old replication ID.

    However the new replication ID of the promoted slave will be different,
    since it constitutes a different history of the data set. For example,
    the master can return available and can continue accepting writes for some time,
    so using the same replication ID in the promoted slave would violate
    the rule that a of replication ID and offset pair identifies only a single data set.

    Moreover slaves when powered off gently and restarted, are able to store
    in the RDB file the information needed in order to resynchronize with their master.
    This is useful in case of upgrades. When this is needed,
    it is better to use the SHUTDOWN command in order to perform a save & quit operation on the slave.

    It is not possilbe to partially resynchronize a slave that restarted via the AOF file.
    However the instance may be turned to RDB persistence before shutting down it,
    than can be restarted, and finally AOF can be enabled again.







