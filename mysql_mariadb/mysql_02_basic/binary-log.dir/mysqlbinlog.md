
- [5.4.4 The Binary Log](https://dev.mysql.com/doc/refman/5.7/en/binary-log.html)
- [4.6.7 mysqlbinlog — Utility for Processing Binary Log Files](https://dev.mysql.com/doc/refman/5.7/en/mysqlbinlog.html)
- [15 mysqlbinlog Command Examples for MySQL Binary Log Files](https://www.thegeekstuff.com/2017/08/mysqlbinlog-examples/)


```bash
[root@dbserver ~]# man mysqlbinlog
[root@dbserver ~]# mysqlbinlog --help | less
```

```text
mysql> create database db_web01 default charset utf8;
```

```text
mysql> create table user(
         id int primary key auto_increment,
         name varchar(20) unique not null,
         password varchar(20) not null
       )engine=innodb default charset utf8;
mysql> insert into user(id, name, password) values(null, 'user01', 'password01');
mysql> insert into user(id, name, password) values(null, 'user02', 'password02');
mysql> update user set password='redhat01' where id = 2;
mysql> delete from user where id = 2;
```

```text
mysql> pager less -Fi
mysql> show binlog events in 'mysql_bin.000003';   # 下面的output是修改后的版本
    | Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info
    ---------------------------------------------------------------------------------------------------------------
    | mysql_bin.000003 |    4 | Format_desc    |       136 |         123 | Server ver: 5.7.25-log, Binlog ver: 4
    | mysql_bin.000003 |  123 | Previous_gtids |       136 |         154 |
    | mysql_bin.000003 |  154 | Anonymous_Gtid |       136 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'
    | mysql_bin.000003 |  219 | Query          |       136 |         346 | create database db_web01 default charset utf8
```

```bash
#// 查看指定的 binary log file
[root@dbserver ~]# mysqlbinlog /mydata/bin-log/mysql_bin.000003  | less
#// 输出结果见  https://github.com/yangsg/linux_training_notes/blob/master/mysql_mariadb/mysql_02_basic/binary-log.dir/output.examples/mysqlbinlog_mysql_bin.000003.output.txt
```

> mysqlbinlog命令显示的二进制日志内容中一个event的范围为起始于 'at', 终止于 'end_log_pos',
> 且'at'与'end_log_pos'描述的是一个半开半闭区间,即[at, end_log_pos)
> 同理，mysqlbinlog命令的选项也有类似对应的选项
>> [--start-position, --stop-position)
>> [--start-datetime, --stop-datetime)
```bash
[root@dbserver binary-log.dir]# mysqlbinlog --start-position=123  --stop-position=154  /mydata/bin-log/mysql_bin.000003
[root@dbserver ~]# mysqlbinlog --start-position=123 /mydata/bin-log/mysql_bin.000003

#// 输出结果见
https://github.com/yangsg/linux_training_notes/blob/master/mysql_mariadb/mysql_02_basic/binary-log.dir/output.examples/mysqlbinlog--start-position--stop-position.mysql_bin.000003.output.md
```


```bash
[root@dbserver ~]# mysqlbinlog --start-datetime="2019-03-30 13:36:01" --stop-datetime="2019-03-30 14:33:09"  /mydata/bin-log/mysql_bin.000003
[root@dbserver ~]# mysqlbinlog --start-datetime="2019-03-30 13:36:01"  /mydata/bin-log/mysql_bin.000003

#// 输出结果见


```

### 其他mysql内部支持的命令
```text
mysql> help show;
```

```text
mysql> show binary logs;
+------------------+-----------+
| Log_name         | File_size |
+------------------+-----------+
| mysql_bin.000001 |       177 |
| mysql_bin.000002 |       201 |
| mysql_bin.000003 |      1867 |
| mysql_bin.000004 |       177 |
| mysql_bin.000005 |       154 |
+------------------+-----------+

```

```text
mysql> show binlog events in 'mysql_bin.000003';
+------------------+------+----------------+-----------+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Log_name         | Pos  | Event_type     | Server_id | End_log_pos | Info                                                                                                                                                                            |
+------------------+------+----------------+-----------+-------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| mysql_bin.000003 |    4 | Format_desc    |       136 |         123 | Server ver: 5.7.25-log, Binlog ver: 4                                                                                                                                           |
| mysql_bin.000003 |  123 | Previous_gtids |       136 |         154 |                                                                                                                                                                                 |
| mysql_bin.000003 |  154 | Anonymous_Gtid |       136 |         219 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                            |
| mysql_bin.000003 |  219 | Query          |       136 |         346 | create database db_web01 default charset utf8                                                                                                                                   |
| mysql_bin.000003 |  346 | Anonymous_Gtid |       136 |         411 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                                                                            |
| mysql_bin.000003 |  411 | Query          |       136 |         652 | use `db_web01`; create table user(
  id int primary key auto_increment,
  name varchar(20) unique not null,
  password varchar(20) not null
)engine=innodb default charset utf8 |
| mysql_bin.000003 |  652 | Anonymous_Gtid |       136 |         717 | SET @@SESSION.GTID_NEXT= 'ANONYMOUS'                                                                                  
```

```text
mysql> show master status;
+------------------+----------+--------------+------------------+-------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+------------------+----------+--------------+------------------+-------------------+
| mysql_bin.000005 |      154 |              |                  |                   |
+------------------+----------+--------------+------------------+-------------------+

```

> - mysql binary log files 滚动3种情况：
>> - server每次重启
>> - 手动执行flush logs
>> - binary log file 大小超过1G (意外特例：包含单个大事务的binary log file可能实际会超过这个限制)


> - 如果多个binary log要执行，安全的方式是在单一的一个(single)到server的connection中执行所有的这些binary log中的语句。否则如果是在多个connection中分开执行，则后续的语句如果依赖前面语句的结果,很可能造成失败(如临时表，前面的connection生成的临时表在那次connection关闭后就释放了，所以后面新的connection中依赖该临时表的语句就没有临时表可用，所以导致失败)
> - If you have more than one binary log to execute on the MySQL server, the safe method is to process them all using a single connection to the server. Here is an example that
> demonstrates what may be unsafe:
> 
>> -   shell> mysqlbinlog binlog.000001 | mysql -u root -p # DANGER!!  危险！！
>> -   shell> mysqlbinlog binlog.000002 | mysql -u root -p # DANGER!!  危险！！
> 
> Processing binary logs this way using multiple connections to the server causes problems if the first log file contains a CREATE TEMPORARY TABLE statement and the second log
> contains a statement that uses the temporary table. When the first mysql process terminates, the server drops the temporary table. When the second mysql process attempts to use
> the table, the server reports “unknown table.”
> 
> To avoid problems like this, use a single mysql process to execute the contents of all binary logs that you want to process. Here is one way to do so:
> 
>> -  shell> mysqlbinlog binlog.000001 binlog.000002 | mysql -u root -p
> 
> Another approach is to write all the logs to a single file and then process the file:
> 
>> -   shell> mysqlbinlog binlog.000001 >  /tmp/statements.sql
>> -   shell> mysqlbinlog binlog.000002 >> /tmp/statements.sql
>> -   shell> mysql -u root -p -e "source /tmp/statements.sql"


```text
trouble shooting

 [root@slave mysql]# mysqlbinlog --no-defaults  slave-bin.000001
     这里如果不加 --no-defaults 则会报错: mysqlbinlog: [ERROR] unknown variable 'default-character-set=utf8mb4'
     原因是 mysqlbinlog 不识别 default-character-set 设置.
     详细见:
           https://www.programering.com/a/MTN2QDNwATM.html
           https://www.cnblogs.com/cobbliu/p/4311926.html
      https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/003-gtid-utf8mb4-rpm-multi-source-replication
```

