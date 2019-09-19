

https://redis.io/topics/clients


----------------------------------------------------------------------------------------------------
How client connections are accepted


  Redis accepts clients connections on the configured listening TCP port and on the
  Unix socket if enabled. When a new client connection is accepted
  the following operations are performed:

    // redis 接受 一个 新的 client connection 后的执行操作:

      - The client socket is put in non-blocking state since Redis uses multiplexing and non-blocking I/O.
      - The TCP_NODELAY option is set in order to ensure that we don't have delays in our connection.
      - A readable file event is created so that Redis is able to collect the client queries
        as soon as new data is available to be read on the socket.


  // 检查 配置指令 maxclients 的限制
  After the client is initialized, Redis checks if we are already at the limit of the number
  of clients that it is possible to handle simultaneously (this is configured using
  the maxclients configuration directive, see the next section of this document for further information).


  // 如果因为 maxclients 的限制而无法接受 the current client, redis 则会向 client 端返回 an error 使其知道
  // 该情况并 立刻 close 该 connection.
  In case it can't accept the current client because the maximum number of clients was already accepted,
  Redis tries to send an error to the client in order to make it aware of this condition,
  and closes the connection immediately. The error message will be able to reach the client
  even if the connection is closed immediately by Redis because the new socket output
  buffer is usually big enough to contain the error, so the kernel will
  handle the transmission of the error.


----------------------------------------------------------------------------------------------------
In what order clients are served

  The order is determined by a combination of the client socket file descriptor
  number and order in which the kernel reports events, so the order is to be considered as unspecified.


  However Redis does the following two things when serving clients:

  - It only performs a single read() system call every time there is something new to
    read from the client socket, in order to ensure that if we have multiple clients connected,
    and a few are very demanding clients sending queries at an high rate,
    other clients are not penalized and will not experience a bad latency figure.

  - However once new data is read from a client, all the queries contained in
    the current buffers are processed sequentially. This improves locality
    and does not need iterating a second time to see if there are clients that need some processing time.


----------------------------------------------------------------------------------------------------
Maximum number of clients


      maxclients 10000

  注: maxclients 还会受到 操作系统的 限制. 所以 操作系统允许打开的 file descriptors 的 maximum number 不应小于
      maximum number + 32 (注: 其中 32 是 保留给 Redis 内部使用的 file descriptors 的 number)

  相关的系统设置:
          ulimit -Sn 100000 # This will only work if hard limit is big enough.
          sysctl -w fs.file-max=100000



  In Redis 2.4 there was a hard-coded limit for the maximum number of clients that could be handled simultaneously.

  In Redis 2.6 this limit is dynamic: by default it is set to 10000 clients,
  unless otherwise stated by the maxclients directive in Redis.conf.

  However, Redis checks with the kernel what is the maximum number of file descriptors that
  we are able to open (the soft limit is checked). If the limit is smaller than the maximum number
  of clients we want to handle, plus 32 (that is the number of file descriptors
  Redis reserves for internal uses), then the number of maximum clients
  is modified by Redis to match the amount of clients we are really
  able to handle under the current operating system limit.

  When the configured number of maximum clients can not be honored,
  the condition is logged at startup as in the following example:

   查看日志:
    ------------------------
    $ ./redis-server --maxclients 100000
    [41422] 23 Jan 11:28:33.179 # Unable to set the max number of files limit to 100032 (Invalid argument), setting the max clients configuration to 10112.
    ------------------------


  When Redis is configured in order to handle a specific number of clients it is a good idea
  to make sure that the operating system limit to the maximum number of file descriptors per process is also set accordingly.

  Under Linux these limits can be set both in the current session and as a system-wide setting with the following commands:

        ulimit -Sn 100000 # This will only work if hard limit is big enough.
        sysctl -w fs.file-max=100000


----------------------------------------------------------------------------------------------------
Output buffers limits


  默认情况下, redis 为不同类型的 clients 设置了不同的 output buffer size 的限制,
  当达到该限制时, client 的 connection 会被 closed 掉 且该 event 会被记录到 redis 的 log file中.

  这些限制即可以通过 命令 CONFIG SET 临时修改, 也可以 通过修改配置文件 redis.conf 来 持久配置


      Redis needs to handle a variable-length output buffer for every client, since
      a command can produce a big amount of data that needs to be transferred to the client.

      However it is possible that a client sends more commands producing more output to
      serve at a faster rate at which Redis can send the existing output to the client.
      This is especially true with Pub/Sub clients in case a client is not able to process new messages fast enough.

      Both the conditions will cause the client output buffer to grow and consume more and more memory.
      For this reason by default Redis sets limits to the output buffer size for different
      kind of clients. When the limit is reached the client connection is closed and the event logged in the Redis log file.


  // Redis 使用两种 limit: hard limit 和 soft limit
  There are two kind of limits Redis uses:

    - The hard limit is a fixed limit that when reached will make Redis closing the client connection as soon as possible.
      // hard limit 是一个固定的 limit, 达到该限制是就立即关闭 the client connection.

    - The soft limit instead is a limit that depends on the time, for instance a soft limit of 32 megabytes
      per 10 seconds means that if the client has an output buffer bigger than 32 megabytes for,
      continuously, 10 seconds, the connection gets closed.
      // soft limit 会 依赖于 时间. 如 a soft limit of 32 megabytes per 10 seconds 意味着
      // 连续 10 秒的时间 client 的 an output buffer 都大于 32 megabytes, 则该 connection 会被 closed 掉.


  // 不同  类型的 clients 具有不同的 默认 limits
  Different kind of clients have different default limits:

    - Normal clients have a default limit of 0, that means, no limit at all, because most normal
      clients use blocking implementations sending a single command and waiting for
      the reply to be completely read before sending the next command,
      so it is always not desirable to close the connection in case of a normal client.
      // Normal clients 的 默认 limit 为 0, 其意味着 没有限制(no limit)

    - Pub/Sub clients have a default hard limit of 32 megabytes and a soft limit of 8 megabytes per 60 seconds.
      // Pub/Sub clients 存在 默认的 32 megabytes 的 hard limit 和 8 megabytes per 60 seconds 的 soft limit

    - Slaves have a default hard limit of 256 megabytes and a soft limit of 64 megabyte per 60 second.
      // Slaves 存在 默认的 256 megabytes 的 hard limit 和 64 megabyte per 60 second 的 soft limit

It is possible to change the limit at runtime using the CONFIG SET command
or in a permanent way using the Redis configuration file redis.conf.
See the example redis.conf in the Redis distribution for more information about how to set the limit.







----------------------------------------------------------------------------------------------------
Query buffer hard limit

    query buffer limit 为 1G, 不可配置

      Every client is also subject to a query buffer limit. This is a non-configurable
      hard limit that will close the connection when the client query buffer
      (that is the buffer we use to accumulate commands from the client) reaches 1 GB,
      and is actually only an extreme limit to avoid a server crash in case of client or server software bugs.



----------------------------------------------------------------------------------------------------
Client timeouts

  如果 你愿意，你可以 为配置 normal clients 配置 timeout 时间,
  当 client 的 connection 空闲(idle) 超过指定的 seconds 之后, 该 connection 被 closed 掉.
  默认行为是 the connection will remain open forever.

  可以通过配置文件 redis.conf 或 命令 CONFIG SET timeout <value> 来配置


    By default recent versions of Redis don't close the connection with
    the client if the client is idle for many seconds: the connection will remain open forever.

    However if you don't like this behavior, you can configure a timeout,
    so that if the client is idle for more than the specified number of seconds,
    the client connection will be closed.

    You can configure this limit via redis.conf or simply using CONFIG SET timeout <value>.

    Note that the timeout only applies to normal clients and it does not apply to Pub/Sub clients,
    since a Pub/Sub connection is a push style connection so a client that is idle is the norm.
    // the timeout 仅会 应用于 normal clients 而 不会 应用于 Pub/Sub clients

    Even if by default connections are not subject to timeout, there are two conditions when it makes sense to set a timeout:

        - Mission critical applications where a bug in the client software may saturate
          the Redis server with idle connections, causing service disruption.

        - As a debugging mechanism in order to be able to connect with the server if a
          bug in the client software saturates the server with idle connections,
          making it impossible to interact with the server.

    // 注: Timeouts 并不一定很 精确(precise)
    Timeouts are not to be considered very precise: Redis avoids to set timer events
    or to run O(N) algorithms in order to check idle clients, so the check is performed
    incrementally from time to time. This means that it is possible that while the
    timeout is set to 10 seconds, the client connection will be closed,
    for instance, after 12 seconds if many clients are connected at the same time.




----------------------------------------------------------------------------------------------------
CLIENT command

    The Redis client command allows to inspect the state of every connected client,
    to kill a specific client, to set names to connections.
    It is a very powerful debugging tool if you use Redis at scale.

    CLIENT LIST is used in order to obtain a list of connected clients and their state:


        redis 127.0.0.1:6379> client list
        addr=127.0.0.1:52555 fd=5 name= age=855 idle=0 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=32768 obl=0 oll=0 omem=0 events=r cmd=client
        addr=127.0.0.1:52787 fd=6 name= age=6 idle=5 flags=N db=0 sub=0 psub=0 multi=-1 qbuf=0 qbuf-free=0 obl=0 oll=0 omem=0 events=r cmd=ping



  In the above example session two clients are connected to the Redis server. The meaning of a few of the most interesting fields is the following:

      - addr: The client address, that is, the client IP and the remote port number it used to connect with the Redis server.
      - fd: The client socket file descriptor number.
      - name: The client name as set by CLIENT SETNAME. (client name 由命令 CLIENT SETNAME 设置)
                      https://redis.io/commands/client-setname

      - age: The number of seconds the connection existed for.
      - idle: The number of seconds the connection is idle.
      - flags: The kind of client (N means normal client, check the full list of flags).
                  https://redis.io/commands/client-list

      - omem: The amount of memory used by the client for the output buffer.
      - cmd: The last executed command.


  See the CLIENT LIST documentation for the full list of fields and their meaning.

  Once you have the list of clients, you can easily close the
  connection with a client using the CLIENT KILL command specifying the client address as argument.
          https://redis.io/commands/client-kill

  The commands CLIENT SETNAME and CLIENT GETNAME can be used to set and get the connection name.
  Starting with Redis 4.0, the client name is shown in the SLOWLOG output,
  so that it gets simpler to identify clients that are creating latency issues.
          https://redis.io/commands/client-setname
          https://redis.io/commands/client-getname
          https://redis.io/commands/slowlog





----------------------------------------------------------------------------------------------------
TCP keepalive

    Recent versions of Redis (3.2 or greater) have TCP keepalive (SO_KEEPALIVE socket option)
    enabled by default and set to about 300 seconds. This option is useful
    in order to detect dead peers (clients that cannot be reached even if they look connected).
    Moreover, if there is network equipment between clients and servers that need to
    see some traffic in order to take the connection open, the option
    will prevent unexpected connection closed events.



----------------------------------------------------------------------------------------------------




























