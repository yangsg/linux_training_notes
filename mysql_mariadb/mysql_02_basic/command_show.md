```text
mysql> help show

Name: 'SHOW'
Description:
SHOW has many forms that provide information about databases, tables,
columns, or status information about the server. This section describes
those following:

SHOW {BINARY | MASTER} LOGS
SHOW BINLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW CHARACTER SET [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE DATABASE db_name
SHOW CREATE EVENT event_name
SHOW CREATE FUNCTION func_name
SHOW CREATE PROCEDURE proc_name
SHOW CREATE TABLE tbl_name
SHOW CREATE TRIGGER trigger_name
SHOW CREATE VIEW view_name
SHOW DATABASES [like_or_where]
SHOW ENGINE engine_name {STATUS | MUTEX}
SHOW [STORAGE] ENGINES
SHOW ERRORS [LIMIT [offset,] row_count]
SHOW EVENTS
SHOW FUNCTION CODE func_name
SHOW FUNCTION STATUS [like_or_where]
SHOW GRANTS FOR user
SHOW INDEX FROM tbl_name [FROM db_name]
SHOW MASTER STATUS
SHOW OPEN TABLES [FROM db_name] [like_or_where]
SHOW PLUGINS
SHOW PROCEDURE CODE proc_name
SHOW PROCEDURE STATUS [like_or_where]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW PROFILE [types] [FOR QUERY n] [OFFSET n] [LIMIT n]
SHOW PROFILES
SHOW RELAYLOG EVENTS [IN 'log_name'] [FROM pos] [LIMIT [offset,] row_count]
SHOW SLAVE HOSTS
SHOW SLAVE STATUS [FOR CHANNEL channel]
SHOW [GLOBAL | SESSION] STATUS [like_or_where]
SHOW TABLE STATUS [FROM db_name] [like_or_where]
SHOW [FULL] TABLES [FROM db_name] [like_or_where]
SHOW TRIGGERS [FROM db_name] [like_or_where]
SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
SHOW WARNINGS [LIMIT [offset,] row_count]

like_or_where:
    LIKE 'pattern'
  | WHERE expr

If the syntax for a given SHOW statement includes a LIKE 'pattern'
part, 'pattern' is a string that can contain the SQL % and _ wildcard
characters. The pattern is useful for restricting statement output to
matching values.

Several SHOW statements also accept a WHERE clause that provides more
flexibility in specifying which rows to display. See
http://dev.mysql.com/doc/refman/5.7/en/extended-show.html.

URL: http://dev.mysql.com/doc/refman/5.7/en/show.html
```

```

mysql> show global variables like '%error%';
mysql> show global variables like '%slow%';
mysql> show global variables like '%bin%';
mysql> show master status;
mysql> show slave status;
mysql> show grants;
mysql> show grants for 'root'@'192.168.175.10';
mysql> show create database db01;
mysql> show engines;

```

```text
mysql> show global variables like '%per_table%';
+-----------------------+-------+
| Variable_name         | Value |
+-----------------------+-------+
| innodb_file_per_table | ON    |
+-----------------------+-------+

```

```text
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql_bin.000001 |       177 |
| mysql_bin.000002 |      3909 |
| mysql_bin.000003 |       783 |
| mysql_bin.000004 |       759 |
| mysql_bin.000005 |       201 |
| mysql_bin.000006 |       177 |
| mysql_bin.000007 |       154 |
+------------------+-----------+


mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql_bin.000007 |      154 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+


mysql> show binlog events;
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| mysql_bin.000001 |   4 | Format_desc    |       136 |         123 | Server ver: 5.7.25-log, Binlog ver: 4 |
| mysql_bin.000001 | 123 | Previous_gtids |       136 |         154 |                                       |
| mysql_bin.000001 | 154 | Stop           |       136 |         177 |                                       |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+

mysql> show binlog events in 'mysql_bin.000006';
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info                                  |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+
| mysql_bin.000006 |   4 | Format_desc    |       136 |         123 | Server ver: 5.7.25-log, Binlog ver: 4 |
| mysql_bin.000006 | 123 | Previous_gtids |       136 |         154 |                                       |
| mysql_bin.000006 | 154 | Stop           |       136 |         177 |                                       |
+------------------+-----+----------------+-----------+-------------+---------------------------------------+

mysql> show binlog events in 'mysql_bin.000006' from 123;
+------------------+-----+----------------+-----------+-------------+------+
| Log_name         | Pos | Event_type     | Server_id | End_log_pos | Info |
+------------------+-----+----------------+-----------+-------------+------+
| mysql_bin.000006 | 123 | Previous_gtids |       136 |         154 |      |
| mysql_bin.000006 | 154 | Stop           |       136 |         177 |      |
+------------------+-----+----------------+-----------+-------------+------+



```


