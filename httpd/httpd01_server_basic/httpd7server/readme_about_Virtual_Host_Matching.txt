
https://httpd.apache.org/docs/2.4/en/vhosts/details.html
Virtual Host Matching

server确定由那个虚拟主机用于响应客户request的策略如下：

# IP address lookup
1. 当基于某个ip地址和port端口的connection(就是向指定ip:port发起的连接请求)第一次received时，server会查找所有具有相同ip:port的VirtualHost定义。
2. 如果没有对于该ip:port的明确的匹配，then wildcard (*) matches are considered
3. 如果还是没有匹配成功，则由 'main server' 负责服务该请求

如果上面'IP address lookup'的步骤1中有针对于该ip地址的VirtualHost的定义，则下一步就是确定是采用一个IP-based 还是 一个 name-based 的虚拟主机响应。

## IP-based vhost
如果仅有一个VirtualHost指令指定的ip:port绑定被确认为是最佳匹配，则不会再执行其他后续操作，同时将由该配置的vhost来服务该请求。

## Name-based vhost
如果有多个 VirtualHost 指令指定的 ip:port绑定被确认为是最佳匹配，(the "list" in the remaining steps refers to the list of vhosts that matched,
in the order they were in the configuration file.)//在我们后续讨论的步骤中, 将使用单词 "list" 表示和引用这些被匹配到的虚拟主机vhosts,且它们的顺序
与其在配置文件中定义的顺序一致。

If the connection is using SSL, the server supports Server Name Indication,
and the SSL client handshake includes the TLS extension with the requested hostname,
then that hostname is used below just like the Host: header would be used on a non-SSL connection.
Otherwise, the first name-based vhost whose address matched is used for SSL connections.
This is significant because the vhost determines which certificate the server will use for the connection.

If the request contains a Host: header field, the list is searched for the first vhost with a matching ServerName or ServerAlias,
and the request is served from that vhost.
A Host: header field can contain a port number, but Apache always ignores it and matches against the real port to which the client sent the request.

The first vhost in the config file with the specified IP address has the highest priority and catches any request to an unknown server name,
or a request without a Host: header field (such as a HTTP/1.0 request).

Persistent connections
The IP lookup described above is only done once for a particular TCP/IP session while
the name lookup is done on every request during a KeepAlive/persistent connection. 
In other words, a client may request pages from different name-based vhosts during a single persistent connection.

Absolute URI
If the URI from the request is an absolute URI, and its hostname and port match the main server or
one of the configured virtual hosts and match the address and port to which the client sent the request,
then the scheme/hostname/port prefix is stripped off and the remaining relative URI is
served by the corresponding main server or virtual host.
If it does not match, then the URI remains untouched and the request is taken to be a proxy request.


# 结论：
  -  Name-based virtual hosting 是在server已经选择了最佳 IP-based virtual host 之后才被应用的处理过程。
  -  如果你不关心客户端的请求的connection具体所连接到的是那个ip地址，使用通配符"*"作为所有每个虚拟主机的地址，
     那么 name-based virtual hosting 的处理将可应用于所有配置中的虚拟主机
  -  只有针对特定的ip地址中的那些 name-based vhosts, 其顺序才是有意义的(即此时这些虚拟主机的位置顺序才会有产生影响)。
     配置文件中第一个(最先)出现的 name-based vhosts 具有最高优先级(for its corresponding address set.)。
  -  Any port in the Host: header field is never used during the matching process.
     Apache always uses the real port to which the client sent the request.
  -  If two vhosts have an address in common, those common addresses act as name-based virtual hosts implicitly. This is new behavior as of 2.3.11.
  -  The main server is only used to serve a request if the IP address and port number to which the client
     connected does not match any vhost (including a * vhost). In other words, the main server only catches
     a request for an unspecified address/port combination (unless there is a _default_ vhost which matches that port).
  -  You should never specify DNS names in VirtualHost directives because it will force your server to rely on DNS to boot.
     Furthermore it poses a security threat if you do not control the DNS for all the domains listed.
     There's more information available on this and the next two topics.
  -  总是应该为每个虚拟主机vhosts 设置 ServerName ，否则，每个虚拟主机都需要一次DNS查询。















