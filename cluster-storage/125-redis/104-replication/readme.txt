

https://redis.io/topics/replication


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
      // 最好开启 master 和 slaves 上的 持久化 功能(因为如果没有开启持久化功能, 则 重启 master 时 会以 an empty dataset 来启动,
      // 如果此时 the slave 尝试同步操作， 则 the slave 也会被 清空)



----------------------------------------------------------------------------------------------------

























