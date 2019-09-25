

基本指南:
    https://redis.io/topics/cluster-tutorial
更多细节:
    https://redis.io/topics/cluster-spec

其他网上资料:
    https://www.cnblogs.com/diegodu/p/9183356.html

----------------------------------------------------------------------------------------------------
Redis cluster tutorial

  Note this tutorial requires Redis version 3.0 or higher.

  If you plan to run a serious Redis Cluster deployment, the more formal specification
  is a suggested reading, even if not strictly required. However it is a good idea to
  start from this document, play with Redis Cluster some time, and only later read the specification.



----------------------------------------------------------------------------------------------------
Redis Cluster 101


    Redis Cluster provides a way to run a Redis installation
    where data is automatically sharded across multiple Redis nodes.
    // Redis Cluster 提供了 一种 安装 Redis 的方式, 其中 data 会 跨 multiple Redis nodes
    // 被自动分片(sharded)


    Redis Cluster also provides some degree of availability during partitions,
    that is in practical terms the ability to continue the operations when
    some nodes fail or are not able to communicate. However the cluster stops
    to operate in the event of larger failures (for example when the majority of masters are unavailable).
    // Redis Cluster 还 提供能 某种程度的 在 partitions 之间的可用性(availability)
    // 也就是说 提供 当 some nodes fail or are not able to communicate 时 继续工作的 能力.
    // 但是, 如果 发生 larger failures 的 事件(event), the cluster 会 停止工作
    // (for example when the majority of masters are unavailable).


    So in practical terms, what do you get with Redis Cluster?

      - The ability to automatically split your dataset among multiple nodes.

      - The ability to continue operations when a subset of the nodes are
        experiencing failures or are unable to communicate with the rest of the cluster.





----------------------------------------------------------------------------------------------------
Redis Cluster TCP ports


  Every Redis Cluster node requires two TCP connections open. The normal Redis TCP port used to serve clients,
  for example 6379, plus the port obtained by adding 10000 to the data port, so 16379 in the example.
  // 每个 Redis Cluster node 需要 打开 2 个 TCP connections,
  // The normal Redis TCP port  用于向 clients 提供服务, 例如 6379.
  // 而 额外的端口 通过在 data port  上 加上 10000 来得到, 如 16379 = 10000 + 6379


  This second high port is used for the Cluster bus, that is a node-to-node communication
  channel using a binary protocol. The Cluster bus is used by nodes for failure detection,
  configuration update, failover authorization and so forth. Clients should never
  try to communicate with the cluster bus port, but always with the normal Redis
  command port, however make sure you open both ports in your firewall,
  otherwise Redis cluster nodes will be not able to communicate.
  // 第二个 high port 被用于 Cluster 的总线(bus), 其是 使用 a binary protocol 的
  // 节点对节点的通信信道(communication channel).
  // Clients 绝不应该 试图 通过 cluster bus port 与之通信, 而应该 总是使用 the normal Redis command port,
  // 但是, 请确保 防火墙 同时 开放了 这 2 个 ports, 否则 Redis cluster nodes 无法彼此通信.


  The command port and cluster bus port offset is fixed and is always 10000.


  Note that for a Redis Cluster to work properly you need, for each node:

      1) The normal client communication port (usually 6379) used to communicate with clients to be open to all
         the clients that need to reach the cluster, plus all the other cluster nodes
         (that use the client port for keys migrations).

        // 注: the other cluster nodes 在执行 keys migrations 时也会用到 The normal client communication port (usually 6379)

      2) The cluster bus port (the client port + 10000) must be reachable from all the other cluster nodes.


  If you don't open both TCP ports, your cluster will not work as expected.

  The cluster bus uses a different, binary protocol, for node to node data exchange,
  which is more suited to exchange information between nodes using little bandwidth and processing time.




----------------------------------------------------------------------------------------------------
Redis Cluster and Docker

  Currently Redis Cluster does not support NATted environments and
  in general environments where IP addresses or TCP ports are remapped.
  // 当前的 Currently Redis Cluster 不支持  NATted 环境, 也不支持  IP 或 TCP ports 被重映射(remapped) 的一般环境.


  Docker uses a technique called port mapping: programs running inside
  Docker containers may be exposed with a different port compared to
  the one the program believes to be using. This is useful in order
  to run multiple containers using the same ports, at the same time, in the same server.

  In order to make Docker compatible with Redis Cluster you need to use the host networking mode of Docker.
  Please check the --net=host option in the Docker documentation for more information.
  // 为使 Docker 兼容于 Redis Cluster, 请使用 Docker 的 host networking mode. 参考 Docker 的选项 --net=host


----------------------------------------------------------------------------------------------------
Redis Cluster data sharding

  Redis Cluster does not use consistent hashing, but a different form of sharding
  where every key is conceptually part of what we call an hash slot.
  // Redis Cluster 没有使用 一致性哈希(consistent hashing), 而是 使用一种不同实行的分片(sharding),
  // 其中每个键(key)从概念上讲都是我们称为哈希槽的一部分。

  There are 16384 hash slots in Redis Cluster, and to compute what is the
  hash slot of a given key, we simply take the CRC16 of the key modulo 16384.
  // Redis Cluster 存在 16384 个 hash slots, 且 为 计算 给定 key 的 hash slot,
  // 仅需简单采用算法 CRC16(key) mod 16384 即可.

    哈希槽
        https://www.jianshu.com/p/fa623e59fdcf

  Every node in a Redis Cluster is responsible for a subset of the hash slots,
  so for example you may have a cluster with 3 nodes, where:
  // Redis Cluster 中的  每个 节点(node) 负责 hash slots 的一个子集(subset)
  // 例如, 假设 cluster 中 有 3 个 nodes, 其中:

      Node A contains hash slots from 0 to 5500.
      Node B contains hash slots from 5501 to 11000.
      Node C contains hash slots from 11001 to 16383.

  This allows to add and remove nodes in the cluster easily. For example if I want to add a new node D,
  I need to move some hash slot from nodes A, B, C to D. Similarly if I want to remove node A from
  the cluster I can just move the hash slots served by A to B and C.
  When the node A will be empty I can remove it from the cluster completely.

  Because moving hash slots from a node to another does not require to stop operations,
  adding and removing nodes, or changing the percentage of hash slots hold by nodes,
  does not require any downtime.


  Redis Cluster supports multiple key operations as long as all the keys involved into
  a single command execution (or whole transaction, or Lua script execution) all belong to
  the same hash slot. The user can force multiple keys to be part of the same
  hash slot by using a concept called hash tags.

  Hash tags are documented in the Redis Cluster specification, but the gist is that if there
  is a substring between {} brackets in a key, only what is inside the string is hashed,
  so for example this{foo}key and another{foo}key are guaranteed to be in the same hash slot,
  and can be used together in a command with multiple keys as arguments.






----------------------------------------------------------------------------------------------------
Redis Cluster master-slave model

    master nodes:  A   +   B   +   C
                   Λ       Λ       Λ  (如果 master 挂了, slave 被提升为 master 顶上, 则 Cluster 可以继续)
                   |       |       |
                   |       |       |
                   |       |       |
    slave  nodes:  A1  +   B1  +   C1



  In order to remain available when a subset of master nodes are failing or are
  not able to communicate with the majority of nodes, Redis Cluster uses
  a master-slave model where every hash slot has from 1 (the master itself)
  to N replicas (N-1 additional slaves nodes).


  In our example cluster with nodes A, B, C, if node B fails the cluster is not able to continue,
  since we no longer have a way to serve hash slots in the range 5501-11000.


  However when the cluster is created (or at a later time) we add a slave node to every master,
  so that the final cluster is composed of A, B, C that are masters nodes,
  and A1, B1, C1 that are slaves nodes, the system is able to continue if node B fails.

  Node B1 replicates B, and B fails, the cluster will promote
  node B1 as the new master and will continue to operate correctly.

  However note that if nodes B and B1 fail at the same time
  Redis Cluster is not able to continue to operate.

----------------------------------------------------------------------------------------------------
Redis Cluster consistency guarantees



TODO: 继续完成该 redis cluster 的学习 和 笔记




















