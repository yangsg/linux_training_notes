

半同步复制 Semisynchronous Replication

准备 实现 环境用的 3 台 主机:
master:  192.168.175.100
slave01: 192.168.175.101
slave02: 192.168.175.102


---------------------------------------------------------------------------------------------------
搭建 本地 yum repo 服务器

因为 外网 网速 太慢, 所有这次 准备自己 搭建 一台 简单的 local yum repo 服务器, 通过该 server 安装 mysql 软件.
具体步骤见:
      https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver


---------------------------------------------------------------------------------------------------
master 上 安装 mysql

// 配置 本地 yum 源, 参考 https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver
[root@master01 ~]# vim /etc/yum.repos.d/000-local-yum.repo

        [000-local-yum]
        name=000-local-yum
        baseurl=http://192.168.175.10/local_yum_repo_dir/
        enabled=1
        gpgcheck=0



[root@master ~]# yum repolist | grep local-yum
[root@master ~]# yum clean metadata
[root@master ~]# yum -y install mysql-community-server

[root@master ~]# rpm -q mysql-community-server
          mysql-community-server-5.7.26-1.el7.x86_64

[root@master ~]# yum list installed  mysql-community-server

[root@master ~]# systemctl start mysqld
[root@master ~]# systemctl enable mysqld.service
[root@master ~]# systemctl status mysqld.service

[root@master ~]# grep 'temporary password' /var/log/mysqld.log
        2019-07-18T02:35:40.301694Z 1 [Note] A temporary password is generated for root@localhost: O0MNuVV!7?#)

[root@master ~]# mysql -u root -p
      mysql> ALTER USER 'root'@'localhost' IDENTIFIED BY 'WWW.1.com';
      mysql> quit

[root@master ~]# netstat -anptu  | grep mysql
    tcp6       0      0 :::3306                 :::*                    LISTEN      2067/mysqld

[root@master ~]# ps -elf | grep mysql
    1 S mysql      2067      1  0  80   0 - 279982 poll_s 15:52 ?       00:00:00 /usr/sbin/mysqld --daemonize --pid-file=/var/run/mysqld/mysqld.pid


---------------------------------------------------------------------------------------------------
在 slave01, slave02 上安装 mysql, 方法 与 如上 master 安装方法一样 (此处略)




---------------------------------------------------------------------------------------------------
// 开始正式 配置 与 replication 相关的 设置

--------------------
master01 相关配置

注: 启用 半同步 复制前 必须 先 安装其 对应的 半同步复制 插件

// 安装 半同步 复制 的 master 端 插件 semisync_master.so
mysql> INSTALL PLUGIN rpl_semi_sync_master SONAME 'semisync_master.so';

// 验证 插件 semisync_master.so 的安装 (还 可以使用 语句 SHOW PLUGINS 查看)
mysql> SELECT PLUGIN_NAME, PLUGIN_STATUS FROM INFORMATION_SCHEMA.PLUGINS WHERE PLUGIN_NAME LIKE '%semi%';
      +----------------------+---------------+
      | PLUGIN_NAME          | PLUGIN_STATUS |
      +----------------------+---------------+
      | rpl_semi_sync_master | ACTIVE        |
      +----------------------+---------------+


[root@master ~]# vim /etc/my.cnf

          [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
          loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

          [mysql]
          default-character-set = utf8mb4

          [mysqlbinlog]
          set_charset=utf8mb4

          [mysqld]
          # 设置 mysql 字符集为 utf8mb4
          character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
          character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
          collation-server = utf8mb4_unicode_ci

          # 如下 4 行 配置 是与 replication 和 gtid 相关的 配置
          log-bin=master-bin
          server-id=100   # server-id 范围: 1 and (232)−1
          gtid_mode=ON    # ON: Both new and replicated transactions must be GTID transactions.
          enforce-gtid-consistency=true  # ON: no transaction is allowed to violate GTID consistency.

          # 关于 系统变量 gtid_mode 和 enforce-gtid-consistency 的信息, 见:
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_gtid_mode
          #  https://dev.mysql.com/doc/refman/5.7/en/replication-options-gtids.html#sysvar_enforce_gtid_consistency

          # 如下 2 行 是与 半同步复制 相关的设置
          # 注: 半同步复制 必须同时(both) 在 master 和 slave 上启用, 否则会 退化为 异步复制 方式
          rpl_semi_sync_master_enabled=1    # 启用 master 的 semi-sync replication功能 # 默认为 0 即关闭
          rpl_semi_sync_master_timeout=1000 # 1 second # 默认为 10 seconds

          # 更多 与 半同步复制 相关的 系统变量 或 状态变量 见:
          #    https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html
          #    https://dev.mysql.com/doc/refman/5.7/en/server-status-variables.html



// 重启 mysql server, 以 应用 如上的配置
[root@master ~]# systemctl restart mysqld


// 创建 专用于 replication 的 user. 参见 https://dev.mysql.com/doc/refman/5.7/en/replication-howto-repuser.html
// 注:
//     create user 的步骤有 许多 问题 或 细节要考虑, 所以为了 最大的 灵活性, 最好 按部就班 的 按如下的 步骤 和 语法
//     来 创建用户(尤其是 涉及 replication 的 拓扑结构中), 具体原因见
//     https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/003-gtid-utf8mb4-rpm-multi-source-replication
//     或 参考   http://www.unixfbi.com/155.html   中 “复制账号重复问题”
mysql> USE mysql;
mysql> CREATE USER IF NOT EXISTS 'repluser'@'192.168.175.103' IDENTIFIED BY 'WWW.1.com';   # 创建 用于 replication 的用户
mysql> GRANT REPLICATION SLAVE ON *.* TO 'repluser'@'192.168.175.103';       授予 该用户 replication slave 权限

     注: mysql 5.7 的文档中 推荐 使用 命令 create user 创建用户和密码, 而不推荐使用 grant 来创建,
         所以如上例子中 为了迎合这种趋势, 没有使用更简单的一行 grant ... identified by ... 这种语句来创建 user.


-----------------------------------------------------------------------------









---------------------------------------------------------------------------------------------------
网上资料:

16.3.9 Semisynchronous Replication
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync.html

16.3.9.1 Semisynchronous Replication Administrative Interface
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-interface.html

16.3.9.2 Semisynchronous Replication Installation and Configuration
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-installation.html

      5.5.1 Installing and Uninstalling Plugins
            https://dev.mysql.com/doc/refman/5.7/en/plugin-loading.html

16.3.9.3 Semisynchronous Replication Monitoring
      https://dev.mysql.com/doc/refman/5.7/en/replication-semisync-monitoring.html






