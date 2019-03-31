
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

```bash
[root@dbserver binary-log.dir]# mysqlbinlog --start-position=123  --stop-position=154  /mydata/bin-log/mysql_bin.000003

[root@dbserver ~]# mysqlbinlog --start-position=123 /mydata/bin-log/mysql_bin.000003
```






