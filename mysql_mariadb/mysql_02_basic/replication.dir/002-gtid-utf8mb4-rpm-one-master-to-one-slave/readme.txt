


gtid_mode=ON
enforce-gtid-consistency=true


--skip-slave-start
--skip-log-bin
--skip-log-slave-updates



mysql> CHANGE MASTER TO
     >     MASTER_HOST = host,
     >     MASTER_PORT = port,
     >     MASTER_USER = user,
     >     MASTER_PASSWORD = password,
     >     MASTER_AUTO_POSITION = 1;





















---------------------------------------------------------------------------------------------------
网上资料:

https://dev.mysql.com/doc/refman/5.7/en/replication.html

16.1.1 Binary Log File Position Based Replication Configuration Overview
      https://dev.mysql.com/doc/refman/5.7/en/binlog-replication-configuration-overview.html

16.1.3 Replication with Global Transaction Identifiers
      https://dev.mysql.com/doc/refman/5.7/en/replication-gtids.html



16.1.3.4 Setting Up Replication Using GTIDs
    https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-howto.html

16.1.3.6 Restrictions on Replication with GTIDs  (基于 GTIDs 的 复制的 限制)
    https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-restrictions.html


谨记一点:
      未启用 GTIDs 的 transactions 的 binary log 是 不能 用在 启用了  GTIDs 的 server 上的

      It is important to understand that logs containing transactions
      without GTIDs cannot be used on servers where GTIDs are enabled.
      Before proceeding, you must be sure that transactions without
      GTIDs do not exist anywhere in the topology.

注: 在 启用 GTIDs 之前做的 已经存在的 backups 不能 再 用于 启用了 GTIDs 的 server
    此时做 一个 新的 backup, 你将 不会没有 可用的 backup.

