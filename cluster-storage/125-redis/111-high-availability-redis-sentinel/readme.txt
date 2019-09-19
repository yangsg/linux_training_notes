

https://redis.io/topics/sentinel


----------------------------------------------------------------------------------------------------

  Redis Sentinel provides high availability for Redis.

  Redis Sentinel also provides other collateral tasks such as monitoring,
  notifications and acts as a configuration provider for clients.


This is the full list of Sentinel capabilities at a macroscopical level (i.e. the big picture):

    - Monitoring. Sentinel constantly checks if your master and slave instances are working as expected.

    - Notification. Sentinel can notify the system administrator, another computer programs,
      via an API, that something is wrong with one of the monitored Redis instances.

    - Automatic failover. If a master is not working as expected, Sentinel can start a failover process
      where a slave is promoted to master, the other additional slaves are reconfigured to use
      the new master, and the applications using the Redis server informed
      about the new address to use when connecting.

    - Configuration provider. Sentinel acts as a source of authority for clients service discovery:
      clients connect to Sentinels in order to ask for the address of the current Redis master
      responsible for a given service. If a failover occurs, Sentinels will report the new address.





----------------------------------------------------------------------------------------------------
Distributed nature of Sentinel  哨兵的分布式特性


Redis Sentinel is a distributed system:

    Sentinel itself is designed to run in a configuration where there are
    multiple Sentinel processes cooperating together. The advantage of
    having multiple Sentinel processes cooperating are the following:

        Sentinel processes 协作的好处:

        1) Failure detection is performed when multiple Sentinels agree about the fact
           a given master is no longer available. This lowers the probability of false positives.
           // 减少误报

        2) Sentinel works even if not all the Sentinel processes are working, making the
           system robust against failures. There is no fun in having
           a fail over system which is itself a single point of failure, after all.
           // 更加健壮, 避免单点故障


The sum of Sentinels, Redis instances (masters and slaves) and clients connecting
to Sentinel and Redis, are also a larger distributed system with specific properties.
In this document concepts will be introduced gradually starting from
basic information needed in order to understand the basic properties of Sentinel,
to more complex information (that are optional) in order to understand how exactly Sentinel works.


----------------------------------------------------------------------------------------------------
Quick Start


Obtaining Sentinel

The current version of Sentinel is called Sentinel 2. It is a rewrite of
the initial Sentinel implementation using stronger and simpler
to predict algorithms (that are explained in this documentation).



--------------------------------------------------
Running Sentinel  运行 Sentinel

        方式1:
            redis-sentinel /path/to/sentinel.conf

        方式2: 以 Sentinel mode 运行 redis-server
            redis-server /path/to/sentinel.conf --sentinel

        Both ways work the same.

        默认 Sentinel 会 监听 tcp 的 26379 端口, 用于接收 其他 Sentinel instances 的 connections.

  However it is mandatory to use a configuration file when running Sentinel, as this file will be
  used by the system in order to save the current state that will be reloaded in case of restarts.
  Sentinel will simply refuse to start if no configuration file is given
  or if the configuration file path is not writable.

    注:  必须指定文件 /path/to/sentinel.conf,  且其 必须可写(writable),
         因为该文件会被用来 save 系统当前状态信息.  在 restarts 时 这些 状态信息会被 reloaded.


  Sentinels by default run listening for connections to TCP port 26379,
  so for Sentinels to work, port 26379 of your servers must be open to receive
  connections from the IP addresses of the other Sentinel instances.
  Otherwise Sentinels can't talk and can't agree about what to do, so failover will never be performed.








----------------------------------------------------------------------------------------------------
Fundamental things to know about Sentinel before deploying

部署 Sentinel 之前 要知道的 基础知识:

    1) You need at least three Sentinel instances for a robust deployment.
       // 对于健壮的部署, 你至少需要 3 个 Sentinel instances

    2) The three Sentinel instances should be placed into computers or
       virtual machines that are believed to fail in an independent way.
       So for example different physical servers or Virtual Machines executed on different availability zones.
      // 为保持故障独立性, The three Sentinel instances 应该被 置于
      // 不同的 physical servers 或 不同的 可用的 zones  中的 Virtual Machines 中


    3) Sentinel + Redis distributed system does not guarantee that acknowledged writes
       are retained during failures, since Redis uses asynchronous replication.
       However there are ways to deploy Sentinel that make the window to
       lose writes limited to certain moments, while there are other less secure ways to deploy it.
       // Sentinel + Redis distributed system 不保证 在故障期间 已确认的写入(acknowledged writes)被保留(retained)


    4) You need Sentinel support in your clients. Popular client libraries have Sentinel support, but not all.
       // Sentinel 还需要 clients 的支持, 流行的 client libraries 大多都支持 Sentinel, 但并非全部

    5) There is no HA setup which is safe if you don't test from time to time
       in development environments, or even better if you can, in production environments,
       if they work. You may have a misconfiguration that will become apparent
       only when it's too late (at 3am when your master stops working).
       // 最好 在开发环境中对 HA setup 进行测试

    6) Sentinel, Docker, or other forms of Network Address Translation or Port Mapping should be mixed with care:
       Docker performs port remapping, breaking Sentinel auto discovery of other Sentinel
       processes and the list of slaves for a master. Check the section about
       Sentinel and Docker later in this document for more information.
      // Sentinel, Docker, 或 other forms of Network Address Translation 或 Port Mapping 结合时要留意注意事项.



----------------------------------------------------------------------------------------------------
Configuring Sentinel

    Redis 源码中 包含了 一份 sentinel.conf 样例文件

  The Redis source distribution contains a file called sentinel.conf that
  is a self-documented example configuration file you can use to configure Sentinel,
  however a typical minimal configuration file looks like the following:

      典型的 最小化的  sentinel.conf 配置如下:

          sentinel monitor mymaster 127.0.0.1 6379 2
          sentinel down-after-milliseconds mymaster 60000
          sentinel failover-timeout mymaster 180000
          sentinel parallel-syncs mymaster 1

          sentinel monitor resque 192.168.1.3 6380 4
          sentinel down-after-milliseconds resque 10000
          sentinel failover-timeout resque 180000
          sentinel parallel-syncs resque 5



  You only need to specify the masters to monitor, giving to each separated
  master (that may have any number of slaves) a different name.
  There is no need to specify slaves, which are auto-discovered.
  Sentinel will update the configuration automatically with additional information
  about slaves (in order to retain the information in case of restart).
  The configuration is also rewritten every time a slave is promoted
  to master during a failover and every time a new Sentinel is discovered.

  仅需为 monitor 指定 masters, 且给 每个 不同的 master 一个不同的 name.
  无需 指定 slaves, 其会被 自动发现(auto-discovered), Sentinel 将会使用 额外的
  slaves 相关的信息 自动更新 配置文件(以便在 restart 保留这些信息), 该配置
  在 每次 a slave 在故障转移期间 被 提升为 master 时 或 每次 一个新的 Sentinel
  被发现时 都会被 重写(rewritten).


  The example configuration above, basically monitor two sets of Redis instances,
  each composed of a master and an undefined number of slaves.
  One set of instances is called mymaster, and the other resque.

The meaning of the arguments of sentinel monitor statements is the following:

        ---------------------------------
        sentinel monitor <master-group-name> <ip> <port> <quorum>
        ---------------------------------


For the sake of clarity, let's check line by line what the configuration options mean:

    The first line is used to tell Redis to monitor a master called mymaster,
    that is at address 127.0.0.1 and port 6379, with a quorum of 2.
    Everything is pretty obvious but the quorum argument:

      - The quorum is the number of Sentinels that need to agree about the fact the master is not reachable,
        in order for really mark the slave as failing, and eventually start a fail over procedure if possible.
        // 参数 quorum 是 认定 master 不可达(not reachable) 的 Sentinels 的 数量. 这是为了真正的将 slave 标记为 failing,
        // 并 最终在 可能的情况下 启动 故障转移的 过程(procedure)


      - However the quorum is only used to detect the failure. In order to actually perform a failover,
        one of the Sentinels need to be elected leader for the failover and be authorized to proceed.
        This only happens with the vote of the majority of the Sentinel processes.
        // 可是, 参数 quorum 仅被用于 探测 故障(failure). 为了实际的执行 故障转移, Sentinels 中的 其中一个 需要被 选举
        // 成为 故障转移的 leader 并被  授权 着手执行. 这仅在 大多数(majority, 过半的) 的 Sentinel processes 投票的情况下
        // 才会发生


    例如:
    So for example if you have 5 Sentinel processes, and the quorum for
    a given master set to the value of 2, this is what happens:

      - If two Sentinels agree at the same time about the master being unreachable, one of the two will try to start a failover.
        // 如果有 2 个 Sentinels 同一时间 认定 the master 不可达(unreachable),
        // 则 2 个 Sentinels 中的 一个 会试图 启动(start) 故障转移

      - If there are at least a total of three Sentinels reachable, the failover will be authorized and will actually start.
        // 如果至少总共有三个 Sentinels 可达(reachable)，则故障转移将被授权并实际开始。


    In practical terms this means during failures Sentinel never starts a failover if
    the majority of Sentinel processes are unable to talk (aka no failover in the minority partition).
    // 实际上, 这意味着 在 故障期间, 如果 大多数(majority, 过半的) 的 Sentinel processes  不能说话(are unable to talk),
    // 则 Sentinel 永远不会执行 故障转移



----------------------------------------------------------------------------------------------------
Other Sentinel options


    The other options are almost always in the form:

        sentinel <option_name> <master_name> <option_value>

    And are used for the following purposes:


      - down-after-milliseconds is the time in milliseconds an instance should not be reachable
        (either does not reply to our PINGs or it is replying with an error) for a Sentinel starting to think it is down.
        // 选项 down-after-milliseconds 指定 多少毫秒(即 千分之一秒) 后还没有返回 ping 回复
        // 或 回复的是 an error, 则 Sentinel 认为 redis 宕(down) 掉了

      - parallel-syncs sets the number of slaves that can be reconfigured to use the new master after
        a failover at the same time. The lower the number, the more time it will take for the failover
        process to complete, however if the slaves are configured to serve old data, you may not want
        all the slaves to re-synchronize with the master at the same time. While the replication process
        is mostly non blocking for a slave, there is a moment when it stops to load the bulk data
        from the master. You may want to make sure only one slave at a time is
        not reachable by setting this option to the value of 1.
        // 选项 parallel-syncs 设置 在 故障转移 后 可以同时 能够被 重新配置为 使用 the new master 的 slaves 的数量.




    Additional options are described in the rest of this document and documented
    in the example sentinel.conf file shipped with the Redis distribution.

    All the configuration parameters can be modified at runtime using the SENTINEL SET command.
    See the Reconfiguring Sentinel at runtime section for more information.


    所有这些选项 都 可以在运行时 使用命令 SENTINEL SET 来配置.


----------------------------------------------------------------------------------------------------
Example Sentinel deployments


  We use ASCII art in order to show you configuration examples in a graphical format, this is what the different symbols means:

  本文档中 约定 的 一些 图示 或 符号 的 意义:

  We write inside the boxes what they are running:

        +-------------------+
        | Redis master M1   |
        | Redis Sentinel S1 |
        +-------------------+

  Different boxes are connected by lines, to show that they are able to talk:

        用 lines 连接的 不同的 boxes 表示 它们能够 通话

      +-------------+               +-------------+
      | Sentinel S1 |---------------| Sentinel S2 |
      +-------------+               +-------------+


  Network partitions are shown as interrupted lines using slashes:

      +-------------+                +-------------+
      | Sentinel S1 |------ // ------| Sentinel S2 |
      +-------------+                +-------------+





  Also note that:
    - Masters are called M1, M2, M3, ..., Mn.
    - Slaves are called R1, R2, R3, ..., Rn (R stands for replica).
    - Sentinels are called S1, S2, S3, ..., Sn.
    - Clients are called C1, C2, C3, ..., Cn.
    - When an instance changes role because of Sentinel actions, we put it inside square brackets,
      so [M1] means an instance that is now a master because of Sentinel intervention.

  Note that we will never show setups where just two Sentinels are used,
  since Sentinels always need to talk with the majority in order to start a failover.



--------------------------------------------------
Example 1(反例): just two Sentinels, DON'T DO THIS

      |------------------------------------|
      |    +----+         +----+           |
      |    | M1 |---------| R1 |           |
      |    | S1 |         | S2 |           | <----无效(not available)
      |    +----+         +----+           |
      |                                    |
      |    Configuration: quorum = 1       |
      |                                    |
      |                                    |
      |------------------------------------|

    - In this setup, if the master M1 fails, R1 will be promoted since the
      two Sentinels can reach agreement about the failure (obviously with quorum set to 1)
      and can also authorize a failover because the majority is two. So apparently
      it could superficially work, however check the next points to see why this setup is broken.

    - If the box where M1 is running stops working, also S1 stops working.
      The Sentinel running in the other box S2 will not be able to
      authorize a failover, so the system will become not available.

    Note that a majority is needed in order to order different failovers,
    and later propagate the latest configuration to all the Sentinels. Also note
    that the ability to failover in a single side of the above setup, without any agreement, would be very dangerous:

        |-----------------------------------|
        |    +----+           +------+      |
        |    | M1 |----//-----| [M1] |      |
        |    | S1 |           | S2   |      |
        |    +----+           +------+      |
        |                                   |
        |-----------------------------------|


  In the above configuration we created two masters (assuming S2 could failover without authorization)
  in a perfectly symmetrical way. Clients may write indefinitely to both sides, and there is no way
  to understand when the partition heals what configuration is the right one,
  in order to prevent a permanent split brain condition.
  So please deploy at least three Sentinels in three different boxes always.

        请总是在 3 个 不同的 boxes 中 部署 3 个 Sentinels(至少).



--------------------------------------------------
Example 2(反例): basic setup with three boxes


This is a very simple setup, that has the advantage to be simple to tune for additional safety.
It is based on three boxes, each box running both a Redis process and a Sentinel process.

        |-----------------------------|
        |         +----+              |
        |         | M1 |              |
        |         | S1 |              |
        |         +----+              |
        |            |                |
        |  +----+    |    +----+      |
        |  | R2 |----+----| R3 |      |
        |  | S2 |         | S3 |      |
        |  +----+         +----+      |
        |                             |
        | Configuration: quorum = 2   |
        |-----------------------------|

  If the master M1 fails, S2 and S3 will agree about the failure and will
  be able to authorize a failover, making clients able to continue.

  In every Sentinel setup, being Redis asynchronously replicated, there is always
  the risk of losing some write because a given acknowledged write may not be able to
  reach the slave which is promoted to master. However in the above setup
  there is an higher risk due to clients partitioned away with an old master, like in the following picture:


        |-----------------------------------------------------|
        |             +----+                                  |
        |             | M1 |                                  |
        |             | S1 | <- C1 (writes will be lost)      |
        |             +----+                                  |
        |                |                                    |
        |                /                                    |
        |                /                                    |
        |    +------+    |    +----+                          |
        |    | [M2] |----+----| R3 |                          |
        |    | S2   |         | S3 |                          |
        |    +------+         +----+                          |
        |                                                     |
        |-----------------------------------------------------|

  In this case a network partition isolated the old master M1, so the slave R2 is promoted to master.
  However clients, like C1, that are in the same partition as the old master,
  may continue to write data to the old master. This data will be lost forever
  since when the partition will heal, the master will be reconfigured
  as a slave of the new master, discarding its data set.


  This problem can be mitigated using the following Redis replication feature,
  that allows to stop accepting writes if a master detects that
  is no longer able to transfer its writes to the specified number of slaves.
  // 使用如下的 Redis replication 特性 能 缓解 如上的 problem,
  // 此设置 允许 当 master 检测到  不再能够 向 指定数量的 slaves 传递(transfer) 其 writes 时 停止接受 writes.


      min-slaves-to-write 1   <---最少能够向 多少个 slaves 传递写入(transfer writes)
      min-slaves-max-lag 10   <---在超过 max-lag 秒 后 slave 都没有 send 异步响应
                                  (注: 无法 transfer writes 的原因: disconnected 或 slave 在 max-lag 后都没有发送异步响应)


  With the above configuration (please see the self-commented redis.conf example
  in the Redis distribution for more information) a Redis instance,
  when acting as a master, will stop accepting writes if it can't write
  to at least 1 slave. Since replication is asynchronous not being able to write
  actually means that the slave is either disconnected, or is not sending
  us asynchronous acknowledges for more than the specified max-lag number of seconds.


  Using this configuration the old Redis master M1 in the above example,
  will become unavailable after 10 seconds. When the partition heals, the Sentinel
  configuration will converge to the new one, the client C1 will
  be able to fetch a valid configuration and will continue with the new master.


  However there is no free lunch. With this refinement, if the two slaves are down,
  the master will stop accepting writes. It's a trade off.
  // 但是 没有免费的午餐, 使用这种改进, 如果 如果两个 slaves 都 down 掉了,
  // 则 the master 将 停止 accepting writes. 这是 一个 折衷.



----------------------------------------------------------------------------------------------------
Example 3: Sentinel in the client boxes

  Sometimes we have only two Redis boxes available, one for the master and one for the slave.
  The configuration in the example 2 is not viable in that case,
  so we can resort to the following, where Sentinels are placed where clients are:


        |-----------------------------------------------|
        |            +----+         +----+              |
        |            | M1 |----+----| R1 |              |
        |            |    |    |    |    |              |
        |            +----+    |    +----+              |
        |                      |                        |
        |         +------------+------------+           |
        |         |            |            |           |
        |         |            |            |           |
        |      +----+        +----+      +----+         |
        |      | C1 |        | C2 |      | C3 |         |
        |      | S1 |        | S2 |      | S3 |         |
        |      +----+        +----+      +----+         |
        |                                               |
        |      Configuration: quorum = 2                |
        |                                               |
        |                                               |
        |-----------------------------------------------|






----------------------------------------------------------------------------------------------------









