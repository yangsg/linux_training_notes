


- [uuid 重复的问题](https://stackoverflow.com/questions/9750536/mysql-uuid-duplication-bug)
- [生成 uuidv4](https://stackoverflow.com/questions/32965743/how-to-generate-a-uuidv4-in-mysql)

```text
mysql> select uuid(), uuid(); --类似这种同一时间执行 uuid() 对导致 uuid 结果重复。注: mysql8 也会出现该问题，且其使用的是 UUIDv1 版本
+--------------------------------------+--------------------------------------+
| uuid()                               | uuid()                               |
+--------------------------------------+--------------------------------------+
| 86ab0358-7101-11eb-8eee-000c290b0e89 | 86ab035f-7101-11eb-8eee-000c290b0e89 |
+--------------------------------------+--------------------------------------+
1 row in set (0.00 sec)

```


```text
参考: https://blog.csdn.net/wuzuyu365/article/details/83893252

mysql> select md5(uuid()), md5(uuid());  //注:这种方式可能有点影响性能,也许可以考虑不使用了 uuid 或由客户端app生成 uuid
+----------------------------------+----------------------------------+
| md5(uuid())                      | md5(uuid())                      |
+----------------------------------+----------------------------------+
| 9bb672d73bad8ac8350c594a0959fcc7 | 9fefcbeebf388f006e51bc3e27d90c84 |
+----------------------------------+----------------------------------+

```
















