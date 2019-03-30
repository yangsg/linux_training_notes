
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

```bash
[root@dbserver ~]# mysqlbinlog /mydata/bin-log/mysql_bin.000003  | less
```

```output

/*!50530 SET @@SESSION.PSEUDO_SLAVE_MODE=1*/;
/*!50003 SET @OLD_COMPLETION_TYPE=@@COMPLETION_TYPE,COMPLETION_TYPE=0*/;
DELIMITER /*!*/;
# at 4
#190330 13:36:01 server id 136  end_log_pos 123 CRC32 0x948a513c        Start: binlog v 4, server v 5.7.25-log created 190330 13:36:01
# Warning: this binlog is either in use or was not closed properly.
BINLOG '
QQCfXA+IAAAAdwAAAHsAAAABAAQANS43LjI1LWxvZwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
AAAAAAAAAAAAAAAAAAAAAAAAEzgNAAgAEgAEBAQEEgAAXwAEGggAAAAICAgCAAAACgoKKioAEjQA
ATxRipQ=
'/*!*/;
# at 123
#190330 13:36:01 server id 136  end_log_pos 154 CRC32 0xa80e1642        Previous-GTIDs
# [empty]
# at 154
#190330 14:29:01 server id 136  end_log_pos 219 CRC32 0x4e412f92        Anonymous_GTID  last_committed=0        sequence_number=1       rbr_only=no
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 219
#190330 14:29:01 server id 136  end_log_pos 346 CRC32 0xcd4345cd        Query   thread_id=3     exec_time=0     error_code=0
SET TIMESTAMP=1553927341/*!*/;
SET @@session.pseudo_thread_id=3/*!*/;
SET @@session.foreign_key_checks=1, @@session.sql_auto_is_null=0, @@session.unique_checks=1, @@session.autocommit=1/*!*/;
SET @@session.sql_mode=1075838976/*!*/;
SET @@session.auto_increment_increment=1, @@session.auto_increment_offset=1/*!*/;
/*!\C utf8 *//*!*/;
SET @@session.character_set_client=33,@@session.collation_connection=33,@@session.collation_server=33/*!*/;
SET @@session.lc_time_names=0/*!*/;
SET @@session.collation_database=DEFAULT/*!*/;
create database db_web01 default charset utf8
/*!*/;
# at 346
#190330 14:33:09 server id 136  end_log_pos 411 CRC32 0xf9065a39        Anonymous_GTID  last_committed=1        sequence_number=2       rbr_only=no
SET @@SESSION.GTID_NEXT= 'ANONYMOUS'/*!*/;
# at 411
#190330 14:33:09 server id 136  end_log_pos 652 CRC32 0xc819e11f        Query   thread_id=3     exec_time=1     error_code=0
use `db_web01`/*!*/;
SET TIMESTAMP=1553927589/*!*/;
create table user(
  id int primary key auto_increment,
  name varchar(20) unique not null,
  password varchar(20) not null
)engine=innodb default charset utf8
/*!*/;
# at 652
#190330 14:36:30 server id 136  end_log_pos 717 CRC32 0xf1d79d48        Anonymous_GTID  last_committed=2        sequence_number=3       rbr_only=yes


```





