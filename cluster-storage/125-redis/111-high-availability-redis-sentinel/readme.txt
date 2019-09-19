

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
         因为该文件会被用来 save 给系统当前状态信息.  在 restarts 时 这些 状态信息会被 reloaded.


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
       // Sentinel + Redis distributed system 不保证 在故障期间 以确认的写入(acknowledged writes)被保留(retained)


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



    所有这些选项 都 可以在运行时 使用命令 SENTINEL SET 来配置.


----------------------------------------------------------------------------------------------------









