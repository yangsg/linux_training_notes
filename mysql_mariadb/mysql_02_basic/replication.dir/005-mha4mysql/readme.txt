


mha4mysql:
      MHA for MySQL: Master High Availability Manager and tools for MySQL (MHA) for automating master failover and fast master switch.

mha4mysql 可以保证数据的 一致性(consistency), 结合 semi-sync 几乎(最大限度) 保证 no data loss.


MHA works with the most common two-tier single master and multiple slaves environments

MHA Manager 通常运行在 一台专用的 server 上(或 2 台, 为了 高可用)
MHA Manager can monitor lots of (even 100+) masters from single server
When monitoring master server, MHA just sends ping packets to master every N seconds (default 3) and it does not send heavy queries.


---------------------------------------------------------------------------------------------------

本示例 采用 1 主 3 从 的复制拓扑结构:

    主要是考虑 1主3从 相比 1主2从, 3台 slaves 能更好 scale out reading traffic,
    而对于一般的网站而言大部分查询都是 select 查询.
    而 假如 有 1 台 server 宕机了, 则还剩 3 台 servers, 此时 仍能保持 为 1主2从,
    此时 执行一些 耗时的 操作(如backups, analytic queries, batch jobs) 从 维护方便 和 性能
    影响考虑还是可以接受的. 总之, 应尽可能降低 出现 1主1从 的风险, 使管理员在 维护时
    至少保证有 1主2从 的环境, 这样可以降低 管理员的 维护压力 和 在线的性能影响.

    更多此类问题的讨论见:
        https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Other_HA_Solutions.md
        https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/UseCases.md


manager :   192.168.175.100  <----- 生产环境中 最好 manager server 也弄 2 台以上, 保证 manager 本身的高可用
master  :   192.168.175.101
slave01 :   192.168.175.102
slave02 :   192.168.175.103
slave03 :   192.168.175.104




---------------------------------------------------------------------------------------------------
网上资料:


yoshinorim/mha4mysql-manager
    https://github.com/yoshinorim/mha4mysql-manager/wiki
    https://github.com/yoshinorim/mha4mysql-manager
    https://www.percona.com/blog/2016/09/02/mha-quickstart-guide/


http://www.ttlsa.com/mysql/step-one-by-one-deploy-mysql-mha-cluster/


mha 之外的 其他一些 解决方案的 缺点 和 问题(重要):
      https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Other_HA_Solutions.md

mha 体系结构
https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Architecture.md

  MHA Components:
      MHA Manager has manager programs such as monitoring MySQL master, controlling master failover, etc.

  MHA Node:
      MHA Node has failover helper scripts such as parsing MySQL binary/relay logs,
      identifying relay log position from which relay logs should be applied to other slaves,
      applying events to the target slave, etc. MHA Node runs on each MySQL server.

  When MHA Manager does failover, MHA manager connects MHA Node via SSH and executes MHA Node commands when needed.


  MHA has a couple of extention points. For example, MHA can call any custom script
  to update master's ip address (updating global catalog database that manages master's ip address,
  updating virtual ip, etc). This is because how to manage IP address depends on
  users' environments and MHA does not want to force one approach.


mha 的优点:
  https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/Advantages.md

      * [Master failover and slave promotion can be done very quickly](#master-failover-and-slave-promotion-can-be-done-very-quickly)
      * [Master crash does not result in data inconsistency](#master-crash-does-not-result-in-data-inconsistency)
      * [No need to modify current MySQL settings](#no-need-to-modify-current-mysql-settings)
      * [No need to increase lots of servers](#no-need-to-increase-lots-of-servers)
      * [No performance penalty](#no-performance-penalty)
      * [Works with any storage engine](#works-with-any-storage-engine)


mha 的典型用例:
  https://raw.githubusercontent.com/wiki/yoshinorim/mha4mysql-manager/UseCases.md


