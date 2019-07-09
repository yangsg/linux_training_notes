
https://dev.mysql.com/doc/refman/5.7/en/replication.html


---------------------------------------------------------------------------------------------------
主从复制的优点

Advantages of replication in MySQL include:

Scale-out solutions: 负载分配, 读写分离. master 上 write, update, 一个或多个 slave 上 read.
Data security: 备份. slave 可暂停 replication process. 且在 slave 上  run backup services 不影响破坏 master 的 data.
Analytics: 在 master 上 live data 被创建时, 在 slave 上做 数据分析从而不影响 master 的性能.
Long-distance data distribution - 使用 replication 创建 remote site 使用的 a local copy, 无需持久的 access master.

MySQL 5.7 supports different methods of replication. The traditional method is based on replicating events from the master's binary log,
and requires the log files and positions in them to be synchronized between master and slave.
The newer method based on global transaction identifiers (GTIDs) is transactional and therefore
does not require working with log files or positions within these files, which greatly simplifies many common replication tasks.
Replication using GTIDs guarantees consistency between master and slave as long as all
transactions committed on the master have also been applied on the slave.

mysql5.7 上 推荐 GTIDs 的方式来 实现 replication. 因其 简化了 replication tasks
且能更好的保证 master 与 slave 之间的数据一致性.

          -------
          16.1.3 Replication with Global Transaction Identifiers
               https://dev.mysql.com/doc/refman/5.7/en/replication-gtids.html


          16.1 Configuring Replication
              https://dev.mysql.com/doc/refman/5.7/en/replication-configuration.html

          -------


单向异步
同步 (如果需要同步复制特性, 则 应使用 NDB Cluster)     见 https://dev.mysql.com/doc/refman/5.7/en/mysql-cluster.html
mysql 5.7 还支持 半同步 (semisynchronous replication)

    With semisynchronous replication, a commit performed on the master blocks before returning to the session
    that performed the transaction until at least one slave acknowledges
    that it has received and logged the events for the transaction;

      -------
      16.3.9 Semisynchronous Replication
            https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html

      -------

MySQL 5.7 还支持 延迟复制, 即 slave 故意滞后 master 一段时间.
      -------
      16.3.10 Delayed Replication
            https://dev.mysql.com/doc/refman/5.7/en/replication-delayed.html

      -------



