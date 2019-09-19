
https://redis.io/topics/security


----------------------------------------------------------------------------------------------------
Redis general security model

  通常 redis 不应该直接 暴露在 Internet 上, 应该使其在 trusted environments 中让 trusted clients 访问.
  Redis 做了 最大化的 性能优化和简化, 但 没有对 security 做最大的优化处理.


    Redis is designed to be accessed by trusted clients inside trusted environments.
    This means that usually it is not a good idea to expose the Redis instance directly
    to the internet or, in general, to an environment where untrusted
    clients can directly access the Redis TCP port or UNIX socket.

    For instance, in the common context of a web application implemented using Redis as a database,
    cache, or messaging system, the clients inside the front-end (web side) of the application
    will query Redis to generate pages or to perform operations requested or triggered by the web application user.

    In this case, the web application mediates access between Redis
    and untrusted clients (the user browsers accessing the web application).

    This is a specific example, but, in general, untrusted access to Redis should
    always be mediated by a layer implementing ACLs, validating user input,
    and deciding what operations to perform against the Redis instance.

    In general, Redis is not optimized for maximum security but for maximum performance and simplicity.



----------------------------------------------------------------------------------------------------
Network security

      防火墙(firewall)

  Note that it is possible to bind Redis to a single interface
  by adding a line like the following to the redis.conf file:

        bind 127.0.0.1

如果没有 有效的 保护 Redis port 访问, 一个简单的 FLUSHALL 命令就能够被 an external attacker 用来删除整个 data set.



----------------------------------------------------------------------------------------------------
Protected mode


    Unfortunately many users fail to protect Redis instances from being accessed from external networks.
    Many instances are simply left exposed on the internet with public IPs. For this reasons
    since version 3.2.0, when Redis is executed with the default
    configuration (binding all the interfaces) and without any password
    in order to access it, it enters a special mode called protected mode.
    In this mode Redis only replies to queries from the loopback interfaces,
    and reply to other clients connecting from other addresses with an error,
    explaining what is happening and how to configure Redis properly.

    We expect protected mode to seriously decrease the security issues caused
    by unprotected Redis instances executed without proper administration,
    however the system administrator can still ignore the error given
    by Redis and just disable protected mode or manually bind all the interfaces.



----------------------------------------------------------------------------------------------------
Authentication feature

      requirepass

      AUTH

          设置足够长的密码(可以很长)

      注: AUTH 命令和 其他 Redis command 一样, 属于 非加密传输,
          所以无法防止被 能够访问网络的 an attacker 窃听.


    The password is set by the system administrator in clear text inside the redis.conf file.
    It should be long enough to prevent brute force attacks for two reasons:

    - Redis is very fast at serving queries. Many passwords per second can be tested by an external client.
    - The Redis password is stored inside the redis.conf file and inside the client configuration,
      so it does not need to be remembered by the system administrator, and thus it can be very long.

    The goal of the authentication layer is to optionally provide a layer of redundancy.
    If firewalling or any other system implemented to protect Redis from external attackers fail,
    an external client will still not be able to access the Redis instance
    without knowledge of the authentication password.

    The AUTH command, like every other Redis command, is sent unencrypted, so it does
    not protect against an attacker that has enough access to the network to perform eavesdropping.




----------------------------------------------------------------------------------------------------
Data encryption support

    Redis does not support encryption. In order to implement setups where trusted
    parties can access a Redis instance over the internet or other untrusted networks,
    an additional layer of protection should be implemented, such as an SSL proxy. We recommend spiped.

        http://www.tarsnap.com/spiped.html



----------------------------------------------------------------------------------------------------
Disabling of specific commands


    It is possible to disable commands in Redis or to rename them into an unguessable name,
    so that normal clients are limited to a specified set of commands.

    For instance, a virtualized server provider may offer a managed Redis instance service.
    In this context, normal users should probably not be able to call the Redis CONFIG command
    to alter the configuration of the instance, but the systems that
    provide and remove instances should be able to do so.

    In this case, it is possible to either rename or completely shadow commands from the
    command table. This feature is available as a statement that
    can be used inside the redis.conf configuration file. For example:

          // 为命令 CONFIG 更名为 一个 难以猜测的名字
          rename-command CONFIG b840fc02d524045429941cc15f59e41cb7be6c52

    In the above example, the CONFIG command was renamed into an unguessable name.
    It is also possible to completely disable it (or any other command)
    by renaming it to the empty string, like in the following example:

          // 完全, 彻底 禁用(disable) 命令 CONFIG
          rename-command CONFIG ""







----------------------------------------------------------------------------------------------------
Attacks triggered by carefully selected inputs from external clients


    There is a class of attacks that an attacker can trigger from the outside even without
    external access to the instance. An example of such attacks are the ability to
    insert data into Redis that triggers pathological (worst case) algorithm complexity
    on data structures implemented inside Redis internals.

    For instance an attacker could supply, via a web form, a set of strings that
    is known to hash to the same bucket into a hash table in order to turn
    the O(1) expected time (the average time) to the O(N) worst case,
    consuming more CPU than expected, and ultimately causing a Denial of Service.

    To prevent this specific attack, Redis uses a per-execution pseudo-random seed to the hash function.

    Redis implements the SORT command using the qsort algorithm. Currently,
    the algorithm is not randomized, so it is possible to trigger
    a quadratic worst-case behavior by carefully selecting the right set of inputs.


----------------------------------------------------------------------------------------------------
String escaping and NoSQL injection

    The Redis protocol has no concept of string escaping, so injection is impossible
    under normal circumstances using a normal client library.
    The protocol uses prefixed-length strings and is completely binary safe.

    Lua scripts executed by the EVAL and EVALSHA commands
    follow the same rules, and thus those commands are also safe.

    While it would be a very strange use case, the application should
    avoid composing the body of the Lua script using strings obtained from untrusted sources.




----------------------------------------------------------------------------------------------------
Code security

    以非 特权的 用户身份运行 redis 实例

    禁止使用某些 CONFIG 等命令

      In a classical Redis setup, clients are allowed full access to the command set,
      but accessing the instance should never result in the ability to control the system where Redis is running.

      Internally, Redis uses all the well known practices for writing secure code,
      to prevent buffer overflows, format bugs and other memory corruption issues.
      However, the ability to control the server configuration using the CONFIG
      command makes the client able to change the working dir of the program
      and the name of the dump file. This allows clients to write RDB Redis
      files at random paths, that is a security issue that may easily
      lead to the ability to compromise the system and/or run untrusted
      code as the same user as Redis is running.

      Redis does not requires root privileges to run. It is recommended to
      run it as an unprivileged redis user that is only used for this purpose.
      The Redis authors are currently investigating the possibility of adding
      a new configuration parameter to prevent CONFIG SET/GET dir and
      other similar run-time configuration directives. This would prevent
      clients from forcing the server to write Redis dump files at arbitrary locations.


----------------------------------------------------------------------------------------------------

























