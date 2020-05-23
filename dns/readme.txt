
---------------------------------------------------------------------------------------------------
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-dns_servers

- DNS server 也被称为 name server


注: 当dns server 被配置为 a recursive name servers 且 没有 authoritative answer,
    或还不存在 以前 query 的 cached answer, 则 dns server 会去 query 其他的 name servers(即 root name servers)
    从而确定 which name servers 对 question 中的 name 具有 权威性, 并 通过查询 它们来 获取 the requested name.
    如果 Name servers 被配置为纯粹的 with recursion disabled 的权威服务器，则其 不会代表 clients 进行查找.

https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-dns_servers

- Name server Zones

  RR:   resource records
  TLD:  top-level domain
  RRSet:  A set of RRs with the same type, owner, and class is called a resource record set (RRSet).



  RR 示例:
     example.com.      86400    IN         A           192.0.2.1
       域名             TTL    class       type        hostaddress


  Zones 通过 使用 zone files 在 authoritative name servers 上被定义的, 包含了 每个 zone 的 resource records 的 定义.
  Zone files 被存放在 primary name servers (也被称为 master name servers) 上, 可在其上 对 这些 files 做修改.
  secondary name servers(also called master name servers), 其 从 primary name servers 接受 zone definitions.
  Both primary and secondary name servers 对于 the zone 都 具有 权威性(authoritative) 并 对 clients 而言 是相同的.
  依赖于 configuration, any name server can also serve as a primary or secondary server for multiple zones at the same time. 

  注: DNS 和 DHCP servers 的 系统管理员, 以及在任何 provisioning applications, 都应该遵循 the host name format used in an organization.

- Name server Types (更多细节见 redhat 官网)
        authoritative
        recursive


- BIND as a Name server

    BIND 有  DNS 相关的 一些程序组成, 如 named (name server), rndc 和 dig.

---------------------------------------------------------------------------------------------------
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/sec-bind

zone files 中常用的 Resource Records:

      A: Address

        格式： hostname IN A IP-address
        例：
               server1  IN  A  10.0.1.3
                        IN  A  10.0.1.5

      CNAME: Canonical Name

        格式:  alias-name IN CNAME real-name
        例:
               server1  IN  A      10.0.1.5
               www      IN  CNAME  server1

      MX: Mail Exchange

        格式:  IN MX preference-value email-server-name
        例:
               example.com.  IN  MX  10  mail.example.com.
                             IN  MX  20  mail2.example.com.

      NS: Nameserver

        格式:  IN NS nameserver-name
        例:
               IN  NS  dns1.example.com.
               IN  NS  dns2.example.com.

      PTR: Pointer
        格式: last-IP-digit IN PTR FQDN-of-system
        例:
              2  IN  PTR  dns2.example.com.

---------------------------------------------------------------------------------------------------
https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-Configure_Host_Names#sec-Recommended_Naming_Practices

存在 3 中 类型的 hostname: static, pretty, and transient.

    static :   传统的主机名, 可被用户指定, 其存储在 文件 /etc/hostname 中
    transient: 由 kernel 维护的 动态主机名, 默认被 初始化为 transient, 而其默认值为 localhost. 可在运行时被 DHCP or mDNS 修改.
    pretty:    a free-form UTF8 host name for presentation to the user.



注意:
   A host name 尽管 可以是 长度至 64 characters 的  free-form 的 字符串,
   当 Red Hat 推荐 static 和 transient names 和 DNS 中使用的 machine 的 fully-qualified domain name (FQDN) 匹配(如 host.example.com).
   It is also recommended that the static and transient names consists only of 7 bit ASCII lower-case characters, no spaces or dots,
   and limits itself to the format allowed for DNS domain name labels, even though this is not a strict requirement.
   Older specifications do not permit the underscore, and so their use is not recommended.

ICANN:  Internet Corporation for Assigned Names and Numbers

---------------------------------------------------------------------------------------------------





网上资料:
dns servers: https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-dns_servers
bind:  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/sec-bind

配置 hostname:  https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/networking_guide/ch-Configure_Host_Names#sec-Recommended_Naming_Practices

      http://www.rfc-editor.org/rfc/rfc1034.txt

Linux（RHEL7及CentOS7）下DNS服务器的搭建与配置
  https://blog.csdn.net/solaraceboy/article/details/78960307
---------------------------------------------------------------------------------------------------


---------------------------------------------------------------------------------------------------
其他:
     DNS污染
	https://baike.baidu.com/item/DNS%E6%B1%A1%E6%9F%93/8620359?fr=aladdin
	https://zhuanlan.zhihu.com/p/101908711

	GitHub的raw.githubusercontent.com的DNS被污染，修改Hosts解决
		https://blog.csdn.net/qq_23204557/article/details/105934126







