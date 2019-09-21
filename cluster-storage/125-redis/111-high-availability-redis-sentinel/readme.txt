

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


  In this setup, the point of view Sentinels is the same as the clients: if a master
  is reachable by the majority of the clients, it is fine. C1, C2, C3 here are generic clients,
  it does not mean that C1 identifies a single client connected to Redis.
  It is more likely something like an application server, a Rails app, or something like that.

  If the box where M1 and S1 are running fails, the failover will happen without issues,
  however it is easy to see that different network partitions will result in different behaviors.
  For example Sentinel will not be able to setup if the network between the clients
  and the Redis servers will get disconnected, since the Redis master and slave will be both not available.

  Note that if C3 gets partitioned with M1 (hardly possible with the network described above,
  but more likely possible with different layouts, or because of failures at the software layer),
  we have a similar issue as described in Example 2, with the difference that here we
  have no way to break the symmetry, since there is just a slave and master, so the master
  can't stop accepting queries when it is disconnected from its slave,
  otherwise the master would never be available during slave failures.

  So this is a valid setup but the setup in the Example 2 has advantages such
  as the HA system of Redis running in the same boxes as Redis itself which
  may be simpler to manage, and the ability to put a bound on the amount
  of time a master into the minority partition can receive writes.



----------------------------------------------------------------------------------------------------
Example 4: Sentinel client side with less than three clients




----------------------------------------------------------------------------------------------------
Sentinel, Docker, NAT, and possible issues

    Docker uses a technique called port mapping: programs running inside Docker containers
    may be exposed with a different port compared to the one the program believes to be using.
    This is useful in order to run multiple containers using the same ports,
    at the same time, in the same server.

    Docker is not the only software system where this happens, there are other
    Network Address Translation setups where ports may be remapped,
    and sometimes not ports but also IP addresses.

    // 重映射 ports 和 addresses 结合 Sentinel 带来问题的两种方式:
    Remapping ports and addresses creates issues with Sentinel in two ways:

        1) Sentinel auto-discovery of other Sentinels no longer works, since it is based on
           hello messages where each Sentinel announce at which port and IP address
           they are listening for connection. However Sentinels have no way to understand
           that an address or port is remapped, so it is announcing an information
           that is not correct for other Sentinels to connect.


        2) Slaves are listed in the INFO output of a Redis master in a similar way: the address is
           detected by the master checking the remote peer of the TCP connection, while the
           port is advertised by the slave itself during the handshake,
           however the port may be wrong for the same reason as exposed in point 1.


  Since Sentinels auto detect slaves using masters INFO output information,
  the detected slaves will not be reachable, and Sentinel will never
  be able to failover the master, since there are no good slaves from
  the point of view of the system, so there is currently no way
  to monitor with Sentinel a set of master and slave instances
  deployed with Docker, unless you instruct Docker to map the port 1:1.
  // Sentinels 是使用 masters 的 INFO 输出信息来自动探测 slaves的

  For the first problem, in case you want to run a set of Sentinel instances using Docker
  with forwarded ports (or any other NAT setup where ports are remapped),
  you can use the following two Sentinel configuration directives
  in order to force Sentinel to announce a specific set of IP and port:

        sentinel announce-ip <ip>
        sentinel announce-port <port>


  Note that Docker has the ability to run in host networking mode (check the --net=host
  option for more information). This should create no issues since ports are not remapped in this setup.



----------------------------------------------------------------------------------------------------
quick start








----------------------------------------------------------------------------------------------------
Sentinel API

    Sentinel provides an API in order to inspect its state, check the health of monitored masters and slaves,
    subscribe in order to receive specific notifications, and change the Sentinel configuration at run time.

    By default Sentinel runs using TCP port 26379 (note that 6379 is the normal Redis port).
    Sentinels accept commands using the Redis protocol, so you can use redis-cli
    or any other unmodified Redis client in order to talk with Sentinel.

    It is possible to directly query a Sentinel to check what is the state of the
    monitored Redis instances from its point of view, to see what other Sentinels it knows,
    and so forth. Alternatively, using Pub/Sub, it is possible to receive push style
    notifications from Sentinels, every time some event happens, like a failover,
    or an instance entering an error condition, and so forth.


----------------------------------------------------------------------------------------------------
Sentinel commands


The following is a list of accepted commands, not covering commands
used in order to modify the Sentinel configuration, which are covered later.

部分 Sentinel 相关的命令:

  - PING  说明: This command simply returns PONG.
  - SENTINEL masters   说明: Show a list of monitored masters and their state.
  - SENTINEL master <master name> 说明: Show the state and info of the specified master.
  - SENTINEL slaves <master name> 说明: Show a list of slaves for this master, and their state.
  - SENTINEL sentinels <master name> 说明: Show a list of sentinel instances for this master, and their state.
  - SENTINEL get-master-addr-by-name <master name> 说明:Return the ip and port number of the master with that name.
                                                        If a failover is in progress or terminated successfully for this
                                                        master it returns the address and port of the promoted slave.

- SENTINEL reset <pattern> 说明:This command will reset all the masters with matching name.
                                The pattern argument is a glob-style pattern.
                                The reset process clears any previous state in a master (including a failover in progress),
                                and removes every slave and sentinel already discovered and associated with the master.

- SENTINEL failover <master name> 说明:Force a failover as if the master was not reachable, and without asking
                                       for agreement to other Sentinels (however a new version of the configuration will
                                       be published so that the other Sentinels will update their configurations).
                                       // 强制故障转移, 而无需征求其他 Sentinels 的同意.(但 新版本的 configuration
                                       // 依然会发布给其他的 Sentinels 并使其 更新 其 configurations)


- SENTINEL ckquorum <master name> 说明:Check if the current Sentinel configuration is able
                                       to reach the quorum needed to failover a master, and the majority needed to authorize
                                       the failover. This command should be used in monitoring systems to check if a Sentinel deployment is ok.
                                       // 检查当前 Sentinel configuration 是否能够 达到 故障转移 a master
                                       // 所需的 quorum, 以及 达到 故障转移所需的 the majority.
                                       // 该命令应该被用于  监视 systems 来 检查 a Sentinel deployment 是否 ok

- SENTINEL flushconfig  说明:Force Sentinel to rewrite its configuration on disk, including the current Sentinel state.
                             Normally Sentinel rewrites the configuration every time something changes in its state
                             (in the context of the subset of the state which is persisted on disk across restart).
                             However sometimes it is possible that the configuration file is lost because of operation
                             errors, disk failures, package upgrade scripts or configuration managers.
                             In those cases a way to to force Sentinel to rewrite the configuration file is handy.
                             This command works even if the previous configuration file is completely missing.
                             // 比如 配置文件被 无意 删除, 此时 可以使用该命令 rewrite 配置文件





----------------------------------------------------------------------------------------------------
Reconfiguring Sentinel at Runtime


  Starting with Redis version 2.8.4, Sentinel provides an API in order to add, remove, or change
  the configuration of a given master. Note that if you have multiple sentinels you should apply
  the changes to all to your instances for Redis Sentinel to work properly. This means that
  changing the configuration of a single Sentinel does not automatically propagates
  the changes to the other Sentinels in the network.
  // 从 Redis version 2.8.4 开始, Sentinel 提供了 用于 add, remove, 或 change 指定 master 的 the configuration
  // 的 API, 要特别注意的是, 如果 有多个 sentinels, 为了让 Redis Sentinel 正常工作, you should apply
  // the changes to all to your instances. 这意味着 单个 Sentinel 的 the configuration 的修改 不会 自动
  // 传播(propagates) 给 网络中的其他 Sentinels.
     (意思就是说 如果要 修改 Sentinel 的配置, 则需要手动在 所有的 Sentinel 实例上都做修改)


The following is a list of SENTINEL sub commands used in order to update the configuration of a Sentinel instance.

  - SENTINEL MONITOR <name> <ip> <port> <quorum> 说明:This command tells the Sentinel to start monitoring a new master
                                                    with the specified name, ip, port, and quorum. It is identical to
                                                    the sentinel monitor configuration directive in sentinel.conf
                                                    configuration file, with the difference that you can't use
                                                    an hostname in as ip, but you need to provide an IPv4 or IPv6 address.


  - SENTINEL REMOVE <name> 说明:is used in order to remove the specified master: the master will
                              no longer be monitored, and will totally be removed from the internal
                              state of the Sentinel, so it will no longer listed by SENTINEL masters and so forth.

  - SENTINEL SET <name> <option> <value> 说明:The SET command is very similar to the CONFIG SET command of Redis,
                                            and is used in order to change configuration parameters of a specific master.
                                            Multiple option / value pairs can be specified (or none at all).
                                            All the configuration parameters that can be configured
                                            via sentinel.conf are also configurable using the SET command.



如下是一些示例:
  The following is an example of SENTINEL SET command in order to modify
  the down-after-milliseconds configuration of a master called objects-cache:

            SENTINEL SET objects-cache-master down-after-milliseconds 1000


      As already stated, SENTINEL SET can be used to set all the configuration parameters that
      are settable in the startup configuration file. Moreover it is possible to change just
      the master quorum configuration without removing and re-adding the master
      with SENTINEL REMOVE followed by SENTINEL MONITOR, but simply using:


            SENTINEL SET objects-cache-master quorum 5

  Note that there is no equivalent GET command since SENTINEL MASTER provides
  all the configuration parameters in a simple to parse format (as a field/value pairs array).


----------------------------------------------------------------------------------------------------
Adding or removing Sentinels   (添加 或 删除 Sentinels)

    // 添加一个新的 Sentinel
    Adding a new Sentinel to your deployment is a simple process because of the
    auto-discover mechanism implemented by Sentinel. All you need to do is to start
    the new Sentinel configured to monitor the currently active master.
    Within 10 seconds the Sentinel will acquire the list of
    other Sentinels and the set of slaves attached to the master.
    // 因为 Sentinel 实现了 auto-discover mechanism, 所以 可以简单的 add 一个 新的 Sentinel 到你的部署中.
    // 你仅需要 启动 该 被 配置为 to monitor the currently active master 的 the new Sentinel 即可.
    // 在 10 seconds 之内, 该 Sentinel 将获得 其他的 Sentinels 的 列表(list) 以及 附加(attached)到 该
    // master 的 slaves 的集合.

    If you need to add multiple Sentinels at once, it is suggested to add it one after the other,
    waiting for all the other Sentinels to already know about the first one before adding the next.
    This is useful in order to still guarantee that majority can be achieved only
    in one side of a partition, in the chance failures should happen in the process of adding new Sentinels.

    This can be easily achieved by adding every new Sentinel with a 30 seconds delay, and during absence of network partitions.

    At the end of the process it is possible to use the command SENTINEL MASTER mastername
    in order to check if all the Sentinels agree about the total number of Sentinels monitoring the master.

        最后 最好使用命令 SENTINEL MASTER mastername 确认一下


    // 移除 一个 Sentinel
    Removing a Sentinel is a bit more complex: Sentinels never forget already seen Sentinels,
    even if they are not reachable for a long time, since we don't want to dynamically
    change the majority needed to authorize a failover and the creation of a new configuration number.
    So in order to remove a Sentinel the following steps should be performed in absence of network partitions:
    // 删除一个 Sentinel 要 稍微复杂一点,
    // 为了删除一个 Sentinel 应该在没有 network partitions 的情况下 按照 如下的步骤操作:

        1) Stop the Sentinel process of the Sentinel you want to remove.
           // 停止 你想要 移除的 Sentinel 的 Sentinel process.

        2) Send a SENTINEL RESET * command to all the other Sentinel instances
          (instead of * you can use the exact master name if you want to reset just a single master).
          One after the other, waiting at least 30 seconds between instances.
          // 发送 命令  `SENTINEL RESET *` 到 所有其他的 Sentinel instances
          //(如果你想仅 reset 单个的 master 则 你可以将 '*' 替换为 精确的 master name)
          // 一个接一个地, 在设置下一个 instance 之前等待 至少 30 seconds

        3) Check that all the Sentinels agree about the number of Sentinels currently active,
           by inspecting the output of SENTINEL MASTER mastername of every Sentinel.
          // 通过观察每个 Sentinel 的 执行命令 `SENTINEL MASTER mastername` 的输出,
          // 检查所有 Sentinels 是否同意当前活动的Sentinels数量



----------------------------------------------------------------------------------------------------
Removing the old master or unreachable slaves

    Sentinels never forget about slaves of a given master, even when they are unreachable
    for a long time. This is useful, because Sentinels should be able to correctly
    reconfigure a returning slave after a network partition or a failure event.

    Moreover, after a failover, the failed over master is virtually added
    as a slave of the new master, this way it will be reconfigured
    to replicate with the new master as soon as it will be available again.

    However sometimes you want to remove a slave (that may be the
    old master) forever from the list of slaves monitored by Sentinels.

    In order to do this, you need to send a SENTINEL RESET mastername command
    to all the Sentinels: they'll refresh the list of slaves within the next 10 seconds,
    only adding the ones listed as correctly replicating from the current master INFO output.
    // 向 所有的 Sentinels 发送命令 `SENTINEL RESET mastername`, 这这些 Sentinels 会在 接下来的 10 seconds
    // 之内 刷新(refresh) slaves 的 列表(list), 仅 添加 从当前 master 的 INFO 输出 中作为 correctly replicating
    // 列出的 slaves.







----------------------------------------------------------------------------------------------------
Pub/Sub Messages

  注意: client 可以 将 a Sentinel 当做 Redis 兼容的 Pub/Sub server 使用(但是 你不能使用 publish)
        来 SUBSCRIBE or PSUBSCRIBE to channels  并 获取 指定 events 的 通知.

  A client can use a Sentinel as it was a Redis compatible Pub/Sub server (but you can't use PUBLISH)
  in order to SUBSCRIBE or PSUBSCRIBE to channels and get notified about specific events.

  The channel name is the same as the name of the event. For instance
  the channel named +sdown will receive all the notifications related to
  instances entering an SDOWN (SDOWN means the instance is no longer reachable
  from the point of view of the Sentinel you are querying) condition.

  To get all the messages simply subscribe using PSUBSCRIBE *.

  The following is a list of channels and message formats you can receive using this API.
  The first word is the channel/event name, the rest is the format of the data.

  Note: where instance details is specified it means that the following arguments
        are provided to identify the target instance:


            <instance-type> <name> <ip> <port> @ <master-name> <master-ip> <master-port>

The part identifying the master (from the @ argument to the end) is optional
and is only specified if the instance is not a master itself.

      -   +reset-master <instance details> -- The master was reset.
      -   +slave <instance details> -- A new slave was detected and attached.
      -   +failover-state-reconf-slaves <instance details> -- Failover state changed to reconf-slaves state.
      -   +failover-detected <instance details> -- A failover started by another Sentinel or any other external entity was detected (An attached slave turned into a master).
      -   +slave-reconf-sent <instance details> -- The leader sentinel sent the SLAVEOF command to this instance in order to reconfigure it for the new slave.
      -   +slave-reconf-inprog <instance details> -- The slave being reconfigured showed to be a slave of the new master ip:port pair, but the synchronization process is not yet complete.
      -   +slave-reconf-done <instance details> -- The slave is now synchronized with the new master.
      -   -dup-sentinel <instance details> -- One or more sentinels for the specified master were removed as duplicated (this happens for instance when a Sentinel instance is restarted).
      -   +sentinel <instance details> -- A new sentinel for this master was detected and attached.
      -   +sdown <instance details> -- The specified instance is now in Subjectively Down state.
      -   -sdown <instance details> -- The specified instance is no longer in Subjectively Down state.
      -   +odown <instance details> -- The specified instance is now in Objectively Down state.
      -   -odown <instance details> -- The specified instance is no longer in Objectively Down state.
      -   +new-epoch <instance details> -- The current epoch was updated.
      -   +try-failover <instance details> -- New failover in progress, waiting to be elected by the majority.
      -   +elected-leader <instance details> -- Won the election for the specified epoch, can do the failover.
      -   +failover-state-select-slave <instance details> -- New failover state is select-slave: we are trying to find a suitable slave for promotion.
      -   no-good-slave <instance details> -- There is no good slave to promote. Currently we'll try after some time, but probably this will change and the state machine will abort the failover at all in this case.
      -   selected-slave <instance details> -- We found the specified good slave to promote.
      -   failover-state-send-slaveof-noone <instance details> -- We are trying to reconfigure the promoted slave as master, waiting for it to switch.
      -   failover-end-for-timeout <instance details> -- The failover terminated for timeout, slaves will eventually be configured to replicate with the new master anyway.
      -   failover-end <instance details> -- The failover terminated with success. All the slaves appears to be reconfigured to replicate with the new master.
      -   switch-master <master name> <oldip> <oldport> <newip> <newport> -- The master new IP and address is the specified one after a configuration change. This is the message most external users are interested in.
      -   +tilt -- Tilt mode entered.
      -   -tilt -- Tilt mode exited.





----------------------------------------------------------------------------------------------------
Handling of -BUSY state

    The -BUSY error is returned by a Redis instance when a Lua script is running
    for more time than the configured Lua script time limit. When this happens
    before triggering a fail over Redis Sentinel will try to send a
    SCRIPT KILL command, that will only succeed if the script was read-only.

  If the instance will still be in an error condition after this try, it will eventually be failed over.


----------------------------------------------------------------------------------------------------
Slaves priority    (Slaves 优先级)

      参数 slave-priority

    其可以在 Redis slave instances 执行 INFO 命令来查看, 如:

            127.0.0.1:6379> info Replication
            # Replication
            role:slave
            master_host:192.168.175.111
            master_port:6379
            master_link_status:up
            master_last_io_seconds_ago:0
            master_sync_in_progress:0
            slave_repl_offset:4866297
            slave_priority:100   <----------观察
            slave_read_only:1
            connected_slaves:0
            master_replid:3fed308fcee0cbdd60a97679e777435e9f32e165
            master_replid2:0000000000000000000000000000000000000000
            master_repl_offset:4866297
            second_repl_offset:-1
            repl_backlog_active:1
            repl_backlog_size:1048576
            repl_backlog_first_byte_offset:3817722
            repl_backlog_histlen:1048576



  Redis instances have a configuration parameter called slave-priority.
  This information is exposed by Redis slave instances in their INFO output,
  and Sentinel uses it in order to pick a slave among the ones that can be used in order to failover a master:
  // Sentinel 使用它来挑选(pick)可用于故障转移主服务器(failover a master)的 slave

      1) If the slave priority is set to 0, the slave is never promoted to master.
        // 如果 slave priority 被设置为 0, 则该 slave 永远不会被 提升为 master.

      2) Slaves with a lower priority number are preferred by Sentinel.
        // 具有更小 priority number 的 Slaves 是 Sentinel 的首选.


    For example if there is a slave S1 in the same data center of the current master,
    and another slave S2 in another data center, it is possible to set S1 with a priority
    of 10 and S2 with a priority of 100, so that if the master fails and both S1 and S2 are available, S1 will be preferred.

        //如果 S1(slave priority 为 10) 和 S2(slave priority 为 100) 都可用于 master 的故障转移, 则 S1 将被选中


    For more information about the way slaves are selected,
    please check the slave selection and priority section of this documentation.





----------------------------------------------------------------------------------------------------
Sentinel and Redis authentication  (Sentinel 和 Redis 的认证)

  When the master is configured to require a password from clients, as a security measure,
  slaves need to also be aware of this password in order to authenticate with the master
  and create the master-slave connection used for the asynchronous replication protocol.

  This is achieved using the following configuration directives:

    - requirepass in the master, in order to set the authentication password,
      and to make sure the instance will not process requests for non authenticated clients.
      // 在 master 端 使用 requirepass 设置 认证 password, 其实不会处理 未经认证的 clients 的 请求

    - masterauth in the slaves in order for the slaves to authenticate
      with the master in order to correctly replicate data from it.
      // 在 slaves 端 使用 masterauth 提供 认证 password, 使 slaves 通过 master 的认证 而 能从 master 哪里正确复制数据


  When Sentinel is used, there is not a single master, since after a failover slaves may play
  the role of masters, and old masters can be reconfigured in order to act as slaves,
  so what you want to do is to set the above directives in all your instances, both masters and slaves.
  // 当使用 Sentinel 时, 没有固定唯一的 master, 因为 master 和 slaves 之间的角色 是随着 故障转移 可以转换的,
  // 因此 你要 做的 就是 同时在 master 和 slaves 端 上 设置 如上的 directives(即 requirepass 和 masterauth 指令)

  This is also usually a sane setup since you don't want to protect
  data only in the master, having the same data accessible in the slaves.

  However, in the uncommon case where you need a slave that is accessible without authentication,
  you can still do it by setting up a slave priority of zero, to prevent this slave
  from being promoted to master, and configuring in this slave only the masterauth directive,
  without using the requirepass directive, so that data will be readable by unauthenticated clients.
  // 但是， 在某些 你 需要 无需认证也能访问 a slave  的 情况下, 你 仍让可以通过 将 a slave priority
  // 设置为 0 以 阻止 该 slave 被 提升为 master, 并 仅使用  masterauth 指令 来配置该 slave 而
  // 无需使用 requirepass 指令来实现. 因此 其上的 data 经 可以通过 未经认证 的 clients 来读取.

  In order for sentinels to connect to Redis server instances when they are
  configured with requirepass, the Sentinel configuration must
  include the sentinel auth-pass directive, in the format:
  // 可以在 Sentinel 的配置中包含 sentinel auth-pass  指令 来使 该 Sentinel
  // 能够 连接到 使用 指令 requirepass 设置了 password 的 Redis server instances,
  // 格式如下:

      sentinel auth-pass <master-group-name> <pass>





----------------------------------------------------------------------------------------------------
Configuring Sentinel instances with authentication

  You can also configure the Sentinel instance itself in order to require client
  authentication via the AUTH command, however this feature is
  only available starting with Redis 5.0.1.
  // 你也可以 为 Sentinel instance 本身 配置 认证 password 使 client 要求 通过 AUTH 来认证.
  // 但是 该特性 从 Redis 5.0.1 版本开始才有效.


  In order to do so, just add the following configuration directive to all your Sentinel instances:
  // 要实现此目的, 仅 将 如下的 requirepass 配置指令 加到 所有的 Sentinel instances 即可:

          requirepass "your_password_here"


  When configured this way, Sentinels will do two things:

    1) A password will be required from clients in order to send commands to Sentinels.
       This is obvious since this is how such configuration directive works in Redis in general.
       // 认证 clients

    2) Moreover the same password configured to access the local Sentinel, will be used by this
       Sentinel instance in order to authenticate to all the other Sentinel instances it connects to.
      // 此外, Sentinel instance 还会 使用该密码 来认证 前来 连接的 所有其他 的 Sentinel instances.


  This means that you will have to configure the same requirepass password in all the Sentinel instances.
  This way every Sentinel can talk with every other Sentinel without any need to configure
  for each Sentinel the password to access all the other Sentinels, that would be very impractical.
  // 这意味着 你 必须 在所有的 Sentinel instances 中 包含 相同的  requirepass password 配置.


  Before using this configuration make sure your client library is able to send the AUTH command to Sentinel instances.




----------------------------------------------------------------------------------------------------
Sentinel clients implementation

  // Sentinel 需要 明确的 client 支持

  Sentinel requires explicit client support, unless the system is configured to
  execute a script that performs a transparent redirection of all the requests
  to the new master instance (virtual IP or other similar systems).
  The topic of client libraries implementation is covered in the document Sentinel clients guidelines.

                                                https://redis.io/topics/sentinel-clients





----------------------------------------------------------------------------------------------------
More advanced concepts   (更多高级概念)

    In the following sections we'll cover a few details about how Sentinel work,
    without to resorting to implementation details and algorithms
    that will be covered in the final part of this document.


----------------------------------------------------------------------------------------------------
SDOWN and ODOWN failure state

  Redis Sentinel has two different concepts of being down, one is called
  a Subjectively Down condition (SDOWN) and is a down condition that is
  local to a given Sentinel instance. Another is called Objectively Down condition (ODOWN)
  and is reached when enough Sentinels (at least the number configured
  as the quorum parameter of the monitored master) have an SDOWN condition,
  and get feedback from other Sentinels using the SENTINEL is-master-down-by-addr command.

  相关命令: SENTINEL is-master-down-by-addr

    SDOWN: Subjectively Down  主观 down
    ODOWN: Objectively Down   客观 down, 会触发 故障转移

      注: ODOWN condition 仅 应用在 masters 上

  From the point of view of a Sentinel an SDOWN condition is reached when it
  does not receive a valid reply to PING requests for the number of seconds
  specified in the configuration as is-master-down-after-milliseconds parameter.

  相关参数: is-master-down-after-milliseconds


  An acceptable reply to PING is one of the following:

        - PING replied with +PONG.
        - PING replied with -LOADING error.
        - PING replied with -MASTERDOWN error.

  Any other reply (or no reply at all) is considered non valid. However note that a
  logical master that advertises itself as a slave in the INFO output is considered to be down.

  Note that SDOWN requires that no acceptable reply is received for the whole interval configured,
  so for instance if the interval is 30000 milliseconds (30 seconds) and
  we receive an acceptable ping reply every 29 seconds, the instance is considered to be working.

  SDOWN is not enough to trigger a failover: it only means a single Sentinel
  believes a Redis instance is not available. To trigger a failover, the ODOWN state must be reached.


  To switch from SDOWN to ODOWN no strong consensus algorithm is used, but just a form of gossip:
  if a given Sentinel gets reports that a master is not working from enough Sentinels
  in a given time range, the SDOWN is promoted to ODOWN.
  If this acknowledge is later missing, the flag is cleared.

  A more strict authorization that uses an actual majority is required in order to
  really start the failover, but no failover can be triggered without reaching the ODOWN state

  // ODOWN condition 仅 应用在 masters 上
  The ODOWN condition only applies to masters. For other kind of instances Sentinel doesn't
  require to act, so the ODOWN state is never reached for slaves and other sentinels, but only SDOWN is.

  However SDOWN has also semantic implications. For example a slave
  in SDOWN state is not selected to be promoted by a Sentinel performing a failover.
  // 但是, SDOWN 也具有 语义含义, 例如 处于 SDOWN state 的 a slave 不会被 a Sentinel 选择并提升(为 master)
  // 来执行故障转移.






----------------------------------------------------------------------------------------------------
Sentinels and Slaves auto discovery

  Sentinels stay connected with other Sentinels in order to reciprocally check the availability
  of each other, and to exchange messages. However you don't need to configure a list
  of other Sentinel addresses in every Sentinel instance you run, as Sentinel uses
  the Redis instances Pub/Sub capabilities in order to discover the
  other Sentinels that are monitoring the same masters and slaves.

  // Sentinels 会保持 与 其他 Sentinels 的 连接 以 相互检查(check) 彼此之间的 可用性(availability).
  // 但是, 你无需在 你运行的 每个 Sentinel instance 中 配置 other Sentinel 的 列表(list),
  // 因为 Sentinel 是 使用 Redis instances 的 Pub/Sub 功能 来 发现(discover) 监视(monitoring)
  // 相同 masters 和 slaves 的 其他 Sentinels 的


  This feature is implemented by sending hello messages into the channel named __sentinel__:hello.
  // 该特性是 通过 向 name 为 __sentinel__:hello 的信道 发送 hello 消息(messages) 来实现的


  Similarly you don't need to configure what is the list of the slaves attached
  to a master, as Sentinel will auto discover this list querying Redis.
  // 类似的, 你无需 配置 附加到 a master 的 the slaves 列表(list),
  // 因为 Sentinel 将自动通过查询 Redis 来 discover 该列表(list)

      // 工作细节如下:

      - Every Sentinel publishes a message to every monitored master and slave Pub/Sub channel __sentinel__:hello,
        every two seconds, announcing its presence with ip, port, runid.

      - Every Sentinel is subscribed to the Pub/Sub channel __sentinel__:hello of every master and slave,
        looking for unknown sentinels. When new sentinels are detected, they are added as sentinels of this master.

      - Hello messages also include the full current configuration of the master.
        If the receiving Sentinel has a configuration for a given master which
        is older than the one received, it updates to the new configuration immediately.

      - Before adding a new sentinel to a master a Sentinel always checks if there
        is already a sentinel with the same runid or the same address (ip and port pair).
        In that case all the matching sentinels are removed, and the new added.








----------------------------------------------------------------------------------------------------
Sentinel reconfiguration of instances outside the failover procedure

  Even when no failover is in progress, Sentinels will always try
  to set the current configuration on monitored instances. Specifically:
  // 即使没有 进行故障转移, Sentinels 也会 始终尝试在 monitored instances 上设置 the current configuration, 特别地:

      - Slaves (according to the current configuration) that claim to be masters,
        will be configured as slaves to replicate with the current master.
        // 声称是 masters 的 Slaves(根据当前的配置),将被配置为 从 the current master 复制的 slaves.
           (注：如上这句话意思是: 某些 redis instance 根据 当前的 configuration
                其应该是作为 slaves, 但其却声称自己是 masters, 则其会被配置为 the current master 的 slaves
                以使其 与  the current configuration 保持一致)

      - Slaves connected to a wrong master, will be reconfigured to replicate with the right master.
        // 连接到 一个错误 master 的 slaves, 将被重新配置为 从 正确的 master 进行复制.



  For Sentinels to reconfigure slaves, the wrong configuration must be
  observed for some time, that is greater than the period used to broadcast new configurations.
  // 为了使 Sentinels 重新配置(reconfigure) slaves, 必须在 一段时间内 观察到 the wrong configuration,
  // 该时间 大于 被用于 broadcast new configurations 的 时间.

  This prevents Sentinels with a stale configuration (for example because they just rejoined from a partition)
  will try to change the slaves configuration before receiving an update.



  Also note how the semantics of always trying to impose the current
  configuration makes the failover more resistant to partitions:

    - Masters failed over are reconfigured as slaves when they return available.
    - Slaves partitioned away during a partition are reconfigured once reachable.

  The important lesson to remember about this section is: Sentinel is a system where each
  process will always try to impose the last logical configuration to the set of monitored instances.
  // 关于 section 需要记住的重要的一课(学到的东西)是: Sentinel 是 一个 其 每个 process 将始终 试图 把
  // the last logical configuration 强加(impose) 到  the set of monitored instances 的系统(system).




----------------------------------------------------------------------------------------------------
Slave selection and priority

When a Sentinel instance is ready to perform a failover, since the master
is in ODOWN state and the Sentinel received the authorization to failover
from the majority of the Sentinel instances known, a suitable slave needs to be selected.

The slave selection process evaluates the following information about slaves:
//  选择 The slave 的过程 会评估 与 slaves 相关的 如下信息:

        1) Disconnection time from the master.
        2) Slave priority.
        3) Replication offset processed.
        4) Run ID.


  // 故障转移时 挑选 slave 时 会被 跳过(即 不考虑)的情况:
  A slave that is found to be disconnected from the master for more than ten times
  the configured master timeout (down-after-milliseconds option), plus the time the
  master is also not available from the point of view of the Sentinel doing the failover,
  is considered to be not suitable for the failover and is skipped.

  In more rigorous terms, a slave whose the INFO output suggests to be disconnected from the master for more than:

        (down-after-milliseconds * 10) + milliseconds_since_master_is_in_SDOWN_state

  Is considered to be unreliable and is disregarded entirely.


  The slave selection only considers the slaves that passed the above test,
  and sorts it based on the above criteria, in the following order.
  // The slave 的选择过程仅考虑 那些通过 如上的 测试(test) 的 slaves, 并
  // 并根据上述标准(criteria)按照以下顺序对其进行排序

      1) The slaves are sorted by slave-priority as configured in the redis.conf file of
         the Redis instance. A lower priority will be preferred.
         // slave-priority 数字越小, 则会优先选择
         // 但是要注意的是: 其 slave-priority 为 特殊值 0 时, 表示该 slave 永远不参与 new master 的竞选

      2) If the priority is the same, the replication offset processed by the slave is checked,
         and the slave that received more data from the master is selected.
        // slave-priority 一样的情况下, 选择处理的 复制 offset 最大的, 即复制同步 data 最多的那个 slave 会被选中.

      3) If multiple slaves have the same priority and processed the same data from the master,
         a further check is performed, selecting the slave with the lexicographically
         smaller run ID. Having a lower run ID is not a real advantage for a slave,
         but is useful in order to make the process of slave selection more deterministic,
         instead of resorting to select a random slave.
        // 如果其他 情况(条件) 都一样, 则 按字典顺序 最小的 run ID 的 slave 会被选择.

  Redis masters (that may be turned into slaves after a failover), and slaves, all must be configured
  with a slave-priority if there are machines to be strongly preferred. Otherwise
  all the instances can run with the default run ID (which is the suggested setup,
  since it is far more interesting to select the slave by replication offset).

  A Redis instance can be configured with a special slave-priority of zero in order
  to be never selected by Sentinels as the new master. However a slave configured
  in this way will still be reconfigured by Sentinels in order to replicate with
  he new master after a failover, the only difference is that it will never become a master itself.
  // 但是要注意的是: 其 slave-priority 为 特殊值 0 时, 表示该 slave 永远不参与 new master 的竞选


----------------------------------------------------------------------------------------------------
Algorithms and internals

  In the following sections we will explore the details of Sentinel behavior.
  It is not strictly needed for users to be aware of all the details,
  but a deep understanding of Sentinel may help to deploy and operate Sentinel in a more effective way.


----------------------------------------------------------------------------------------------------
Quorum

  注: 故障转移的 实际执行不仅需要满足 quorum 条件(quorum条件仅触发 trigger 故障转移), 还要满足
      at least a majority of Sentinels must authorize the Sentinel to failover(即故障转移
      需要得到至少 大多数/过半的 Sentinels 成员的 授权authorize 才可实际执行).

    The previous sections showed that every master monitored by Sentinel is
    associated to a configured quorum. It specifies the number of Sentinel processes
    that need to agree about the unreachability or error condition of the master in order to trigger a failover.

    However, after the failover is triggered, in order for the failover to actually be performed,
    at least a majority of Sentinels must authorize the Sentinel to failover.
    Sentinel never performs a failover in the partition where a minority of Sentinels exist.


  Let's try to make things a bit more clear:

  Quorum: the number of Sentinel processes that need to detect an error
  condition in order for a master to be flagged as ODOWN.

        - Quorum: the number of Sentinel processes that need to detect an error condition in order for a master to be flagged as ODOWN.
        - The failover is triggered by the ODOWN state.
        - Once the failover is triggered, the Sentinel trying to failover is required to ask for authorization
          to a majority of Sentinels (or more than the majority if the quorum
          is set to a number greater than the majority).


  The difference may seem subtle but is actually quite simple to understand and use. For example if
  you have 5 Sentinel instances, and the quorum is set to 2, a failover will be triggered as soon as 2
  Sentinels believe that the master is not reachable, however one of the two Sentinels
  will be able to failover only if it gets authorization at least from 3 Sentinels.

  If instead the quorum is configured to 5, all the Sentinels must agree
  about the master error condition, and the authorization from all Sentinels is required in order to failover.

  This means that the quorum can be used to tune Sentinel in two ways:

      1) If a the quorum is set to a value smaller than the majority of Sentinels we deploy,
         we are basically making Sentinel more sensible to master failures,
         triggering a failover as soon as even just a minority of
         Sentinels is no longer able to talk with the master.

      2) If a quorum is set to a value greater than the majority of Sentinels,
         we are making Sentinel able to failover only when there are a very
         large number (larger than majority) of well connected Sentinels which agree about the master being down.




----------------------------------------------------------------------------------------------------
Configuration epochs


----------------------------------------------------------------------------------------------------
Configuration propagation


----------------------------------------------------------------------------------------------------
Consistency under partitions


----------------------------------------------------------------------------------------------------
Sentinel persistent state


----------------------------------------------------------------------------------------------------
TILT mode


----------------------------------------------------------------------------------------------------



