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


// 下面演示创建新的binary log的时机(每次start server和手动执行flush logs命令时)
// 另外，当 binary 大小操作 max_binlog_size (默认1G)时，也会自动创建新的binary log文件。
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






