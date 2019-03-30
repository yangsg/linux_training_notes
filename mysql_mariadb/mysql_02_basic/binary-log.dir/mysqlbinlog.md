
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
#// 查看指定的 binary log file
[root@dbserver ~]# mysqlbinlog /mydata/bin-log/mysql_bin.000003  | less
```







