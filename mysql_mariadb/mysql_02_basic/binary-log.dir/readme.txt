https://dev.mysql.com/doc/refman/5.7/en/binary-log.html

启用binary log 功能 (可用于主从复制 和 数据还原恢复)

// 未启动前
mysql> show global variables like '%log_bin%';
+---------------------------------+-------+
| Variable_name                   | Value |
+---------------------------------+-------+
| log_bin                         | OFF   |
| log_bin_basename                |       |
| log_bin_index                   |       |
| log_bin_trust_function_creators | OFF   |
| log_bin_use_v1_row_events       | OFF   |
+---------------------------------+-------+
5 rows in set (0.00 sec)

// 创建独立的二进制日志文件来将log-bin与data分开存放
[root@dbserver ~]# mkdir -p /mydata/bin-log/
[root@dbserver ~]# chown -R mysql:mysql /mydata/bin-log/


[root@dbserver ~]# vim /etc/my.cnf
        #// 启动二进制日志--------------------
        #// In MySQL 5.7, the --server-id option must be specified if binary logging is enabled, otherwise the server is not allowed to start.
        #// https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_log_bin
        #// https://dev.mysql.com/doc/refman/5.7/en/replication-options.html#option_mysqld_server-id
        server_id=136
        log_bin=/mydata/bin-log/mysql_bin   # log_bin 是启动时参数，需要重启才能生效(生产环境中建议指定与data不同的目录及磁盘设备)
        #//log_bin=mysql_bin   # log_bin 是启动时参数，需要重启才能生效
        #// 创建独立的二进制日志文件来将log-bin与data分开存放
        #//[root@dbserver ~]# mkdir -p /mydata/bin-log/
        #//[root@dbserver ~]# chown -R mysql:mysql /mydata/bin-log/
        #// [root@dbserver ~]# /etc/init.d/mysqld restart
        #
        #// -----------------------------------


[root@dbserver ~]# /etc/init.d/mysqld restart    # 如果重启成功，至此，二进制日志功能已经启动

mysql> show global variables like '%log_bin%';
+---------------------------------+---------------------------------+
| Variable_name                   | Value                           |
+---------------------------------+---------------------------------+
| log_bin                         | ON                              |
| log_bin_basename                | /mydata/bin-log/mysql_bin       |
| log_bin_index                   | /mydata/bin-log/mysql_bin.index |
| log_bin_trust_function_creators | OFF                             |
| log_bin_use_v1_row_events       | OFF                             |
+---------------------------------+---------------------------------+






// 下面演示创建新的binary log的时机(每次start server和手动执行flush logs命令时)
// 另外，当 binary 大小操作 max_binlog_size (默认1G)时，也会自动创建新的binary log文件。
// 注：如果一个大事务的语句超过 max_binlog_size, 实际的 binary log file大小也会超过max_binlog_size的限制
// https://dev.mysql.com/doc/refman/5.7/en/replication-options-binary-log.html#sysvar_max_binlog_size

[root@dbserver ~]# ls /mydata/bin-log/     #mysqld在每次start时都会创建新的binary log文件
    mysql_bin.000001  mysql_bin.index

[root@dbserver ~]# /etc/init.d/mysqld restart
[root@dbserver ~]# ls /mydata/bin-log/
    mysql_bin.000001  mysql_bin.000002  mysql_bin.index

mysql> flush logs;       #手动执行flush logs时创建新的binary log 文件

[root@dbserver ~]# ls /mydata/bin-log/
    mysql_bin.000001  mysql_bin.000002  mysql_bin.000003  mysql_bin.index

// mysql_bin.index 文件的作用为跟踪已经被使用过的所有 binary log files
[root@dbserver ~]# cat /mydata/bin-log/mysql_bin.index
    /mydata/bin-log/mysql_bin.000001
    /mydata/bin-log/mysql_bin.000002
    /mydata/bin-log/mysql_bin.000003

[root@dbserver ~]# file /mydata/bin-log/mysql_bin.000001
    /mydata/bin-log/mysql_bin.000001: MySQL replication log
[root@dbserver ~]# file /mydata/bin-log/mysql_bin.index
    /mydata/bin-log/mysql_bin.index: ASCII text



mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql_bin.000001 |       177 |
| mysql_bin.000002 |       201 |
| mysql_bin.000003 |      1820 |
+------------------+-----------+

mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql_bin.000003 |     1820 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+


mysql> pager less -Fi
mysql> show binlog events in 'mysql_bin.000003';   # 下面的output是修改后的版本
    | Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info
    ---------------------------------------------------------------------------------------------------------------
    | mysql_bin.000003 |    4 | Format_desc    |       136 |         123 | Server ver: 5.7.25-log, Binlog ver: 4
    | mysql_bin.000003 |  123 | Previous_gtids |       136 |         154 |
    | mysql_bin.000003 |  154 | Anonymous_Gtid |       136 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'
    | mysql_bin.000003 |  219 | Query          |       136 |         346 | create database db_web01 default charset utf8








