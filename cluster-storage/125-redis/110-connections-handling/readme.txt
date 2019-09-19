

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



----------------------------------------------------------------------------------------------------




































