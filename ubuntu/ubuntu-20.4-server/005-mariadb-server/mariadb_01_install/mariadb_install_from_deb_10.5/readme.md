

//做一些初始化的设置,
 如:
 设置 主机名, 网络参数(静态ip等), 时间同步, 国内镜像源(安装其某些依赖包)等

```bash
# 查看本机环境

ysg@vm01:~$ hostnamectl
   Static hostname: vm01
         Icon name: computer-vm
           Chassis: vm
        Machine ID: 4db7b4a47c594588b4c1d08b489478ae
           Boot ID: efc297b48d1740e6935063d3544c9e5f
    Virtualization: vmware
  Operating System: Ubuntu 20.04.1 LTS
            Kernel: Linux 5.4.0-54-generic
      Architecture: x86-64


ysg@vm01:~$ ip addr show dev ens33  #查看本机 ip
2: ens33: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc fq_codel state UP group default qlen 1000
    link/ether 00:0c:29:d5:3a:f8 brd ff:ff:ff:ff:ff:ff
    inet 192.168.175.133/24 brd 192.168.175.255 scope global ens33
       valid_lft forever preferred_lft forever
    inet6 fe80::20c:29ff:fed5:3af8/64 scope link
       valid_lft forever preferred_lft forever


```
#### 安装 10.5.8 版本的 mariadb-server

参考资料:
  - https://www.osradar.com/install-mariadb-10-5-ubuntu-20-04-18-04/



  - https://mariadb.com/kb/en/binary-packages/
  - https://mariadb.com/kb/en/installing-mariadb-deb-files/


  各 Linux 发行版的 mariadb 包的仓库信息见:
    https://downloads.mariadb.org/mariadb/repositories/#mirror=escience




### Setting up MariaDB Repositories
```bash
ysg@vm01:~$ sudo apt-get update
ysg@vm01:~$ sudo apt-get install software-properties-common -y
# 导入认证 key
ysg@vm01:~$ sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'

# 添加仓库(此处使用的是创建 MariaDB-Server-10.5.list 仓库配置文件的方式)
# //参考 https://downloads.mariadb.org/mariadb/repositories/#mirror=escience
ysg@vm01:~$ sudo vim  /etc/apt/sources.list.d/MariaDB-Server-10.5.list

  # MariaDB 10.5 repository list - created 2021-01-09 13:47 UTC
  # http://downloads.mariadb.org/mariadb/repositories/
  deb [arch=amd64] https://mirrors.nju.edu.cn/mariadb/repo/10.5/ubuntu focal main
  deb-src https://mirrors.nju.edu.cn/mariadb/repo/10.5/ubuntu focal main


ysg@vm01:~$ sudo apt update
ysg@vm01:~$ sudo apt install mariadb-server


ysg@vm01:~$ dpkg -l mariadb-server
    Desired=Unknown/Install/Remove/Purge/Hold
    | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
    |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
    ||/ Name           Version              Architecture Description
    +++-==============-====================-============-=====================================================================
    ii  mariadb-server 1:10.5.8+maria~focal all          MariaDB database server (metapackage depending on the latest version)


ysg@vm01:~$ mysql --version
  mysql  Ver 15.1 Distrib 10.5.8-MariaDB, for debian-linux-gnu (x86_64) using readline 5.2




// 可以观察到，安装完 mariadb-server 后,  服务 mariadb.service 自动就被 启动了，也其被设置为了开机自启
ysg@vm01:~$ systemctl status mariadb.service
  ● mariadb.service - MariaDB 10.5.8 database server
       Loaded: loaded (/lib/systemd/system/mariadb.service; enabled; vendor preset: enabled)
      Drop-In: /etc/systemd/system/mariadb.service.d
               └─migrated-from-my.cnf-settings.conf
       Active: active (running) since Sat 2021-01-09 14:03:46 UTC; 3min 16s ago
         Docs: man:mariadbd(8)
               https://mariadb.com/kb/en/library/systemd/
     Main PID: 4326 (mariadbd)
       Status: "Taking your SQL requests now..."
        Tasks: 10 (limit: 1041)
       Memory: 68.3M
       CGroup: /system.slice/mariadb.service
               └─4326 /usr/sbin/mariadbd

  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: mysql
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: performance_schema
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: Phase 6/7: Checking and upgrading tables
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: Processing databases
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: information_schema
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: performance_schema
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: Phase 7/7: Running 'FLUSH PRIVILEGES'
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4355]: OK
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4431]: Checking for insecure root accounts.
  Jan 09 14:03:47 vm01 /etc/mysql/debian-start[4436]: Triggering myisam-recover for all MyISAM tables and aria-recover for all Aria tables




ysg@vm01:~$ sudo mysql_secure_installation

  NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
        SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

  In order to log into MariaDB to secure it, we'll need the current
  password for the root user. If you've just installed MariaDB, and
  haven't set the root password yet, you should just press enter here.

  Enter current password for root (enter for none):  <------直接回车
  OK, successfully used password, moving on...

  Setting the root password or using the unix_socket ensures that nobody
  can log into the MariaDB root user without the proper authorisation.

  You already have your root account protected, so you can safely answer 'n'.

  Switch to unix_socket authentication [Y/n] n <-------键入 n
   ... skipping.

  You already have your root account protected, so you can safely answer 'n'.

  Change the root password? [Y/n] y  <------键入 y, 修改 root 密码
  New password:
  Re-enter new password:
  Password updated successfully!
  Reloading privilege tables..
   ... Success!


  By default, a MariaDB installation has an anonymous user, allowing anyone
  to log into MariaDB without having to have a user account created for
  them.  This is intended only for testing, and to make the installation
  go a bit smoother.  You should remove them before moving into a
  production environment.

  Remove anonymous users? [Y/n] y  <------删除匿名账号
   ... Success!

  Normally, root should only be allowed to connect from 'localhost'.  This
  ensures that someone cannot guess at the root password from the network.

  Disallow root login remotely? [Y/n] y  <-----禁止 root 远程登录
   ... Success!

  By default, MariaDB comes with a database named 'test' that anyone can
  access.  This is also intended only for testing, and should be removed
  before moving into a production environment.

  Remove test database and access to it? [Y/n] y  <------删除 test 数据库及其相关授权
   - Dropping test database...
   ... Success!
   - Removing privileges on test database...
   ... Success!

  Reloading the privilege tables will ensure that all changes made so far
  will take effect immediately.

  Reload privilege tables now? [Y/n] y  <-------重新加载授权表
   ... Success!

  Cleaning up...

  All done!  If you've completed all of the above steps, your MariaDB
  installation should now be secure.

  Thanks for using MariaDB!





```

#### 观察端口号
```bash

ysg@vm01:~$ sudo ss -antp | grep :3306
  [sudo] password for ysg:
  LISTEN   0        80                 127.0.0.1:3306              0.0.0.0:*       users:(("mariadbd",pid=4326,fd=19))                  
```



#### 登录 mariadb 数据库(注: 正确的连接方式还应指定参数 --default-character-set=utf8mb4)
```bash
ysg@vm01:~$ mysql -u root -p  #注: 其实还应该指定 --default-character-set=utf8mb4 参数
  Enter password:
  Welcome to the MariaDB monitor.  Commands end with ; or \g.
  Your MariaDB connection id is 51
  Server version: 10.5.8-MariaDB-1:10.5.8+maria~focal mariadb.org binary distribution

  Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

  MariaDB [(none)]> USE mysql;
  MariaDB [mysql]> SELECT User, Host, plugin FROM mysql.user;
  +-------------+-----------+-----------------------+
  | User        | Host      | plugin                |
  +-------------+-----------+-----------------------+
  | mariadb.sys | localhost | mysql_native_password |
  | root        | localhost | mysql_native_password |
  | mysql       | localhost | mysql_native_password |
  +-------------+-----------+-----------------------+

  MariaDB [mysql]> SHOW VARIABLES LIKE 'character%';    #观察字符集
  +--------------------------+----------------------------+
  | Variable_name            | Value                      |
  +--------------------------+----------------------------+
  | character_set_client     | utf8                       | <---客户端没有设置 --default-character-set=utf8mb4 造成
  | character_set_connection | utf8                       |
  | character_set_database   | utf8mb4                    |
  | character_set_filesystem | binary                     |
  | character_set_results    | utf8                       |
  | character_set_server     | utf8mb4                    |
  | character_set_system     | utf8                       |
  | character_sets_dir       | /usr/share/mysql/charsets/ |
  +--------------------------+----------------------------+
  8 rows in set (0.001 sec)

  MariaDB [mysql]> SHOW VARIABLES LIKE 'collation%';   #观察比较规则
  +----------------------+--------------------+
  | Variable_name        | Value              |
  +----------------------+--------------------+
  | collation_connection | utf8_general_ci    |
  | collation_database   | utf8mb4_general_ci |
  | collation_server     | utf8mb4_general_ci |
  +----------------------+--------------------+
  3 rows in set (0.001 sec)


MariaDB [mysql]> status
  --------------
  mysql  Ver 15.1 Distrib 10.5.8-MariaDB, for debian-linux-gnu (x86_64) using readline 5.2

  Connection id:          51
  Current database:       mysql
  Current user:           root@localhost
  SSL:                    Not in use
  Current pager:          stdout
  Using outfile:          ''
  Using delimiter:        ;
  Server:                 MariaDB
  Server version:         10.5.8-MariaDB-1:10.5.8+maria~focal mariadb.org binary distribution
  Protocol version:       10
  Connection:             Localhost via UNIX socket
  Server characterset:    utf8mb4
  Db     characterset:    utf8mb4
  Client characterset:    utf8
  Conn.  characterset:    utf8
  UNIX socket:            /run/mysqld/mysqld.sock
  Uptime:                 29 min 57 sec

  Threads: 3  Questions: 526  Slow queries: 0  Opens: 172  Open tables: 30  Queries per second avg: 0.292
  --------------



```

#### 正确的登录连接方式(指定 --default-character-set=utf8mb4 参数)
```bash
ysg@vm01:~$ mysql -u root -p --default-character-set=utf8mb4
  Enter password:
  Welcome to the MariaDB monitor.  Commands end with ; or \g.
  Your MariaDB connection id is 53
  Server version: 10.5.8-MariaDB-1:10.5.8+maria~focal mariadb.org binary distribution

  Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

  Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

  MariaDB [(none)]> status
  --------------
  mysql  Ver 15.1 Distrib 10.5.8-MariaDB, for debian-linux-gnu (x86_64) using readline 5.2

  Connection id:          53
  Current database:
  Current user:           root@localhost
  SSL:                    Not in use
  Current pager:          stdout
  Using outfile:          ''
  Using delimiter:        ;
  Server:                 MariaDB
  Server version:         10.5.8-MariaDB-1:10.5.8+maria~focal mariadb.org binary distribution
  Protocol version:       10
  Connection:             Localhost via UNIX socket
  Server characterset:    utf8mb4
  Db     characterset:    utf8mb4
  Client characterset:    utf8mb4
  Conn.  characterset:    utf8mb4
  UNIX socket:            /run/mysqld/mysqld.sock
  Uptime:                 32 min 59 sec

  Threads: 3  Questions: 529  Slow queries: 0  Opens: 172  Open tables: 30  Queries per second avg: 0.267
  --------------

MariaDB [(none)]> SHOW VARIABLES WHERE Variable_name LIKE 'character_set_%' OR Variable_name LIKE 'collation%';
  +--------------------------+----------------------------+
  | Variable_name            | Value                      |
  +--------------------------+----------------------------+
  | character_set_client     | utf8mb4                    |
  | character_set_connection | utf8mb4                    |
  | character_set_database   | utf8mb4                    |
  | character_set_filesystem | binary                     |
  | character_set_results    | utf8mb4                    |
  | character_set_server     | utf8mb4                    |
  | character_set_system     | utf8                       |
  | character_sets_dir       | /usr/share/mysql/charsets/ |
  | collation_connection     | utf8mb4_general_ci         |
  | collation_database       | utf8mb4_general_ci         |
  | collation_server         | utf8mb4_general_ci         |
  +--------------------------+----------------------------+
  11 rows in set (0.001 sec)




```


```text
一些可能的登录问题及解决办法:
// 登录时出现如下问题:
ysg@vm01:~$ mysql -u root -p
Enter password:
ERROR 1698 (28000): Access denied for user 'root'@'localhost'


解决办法:
  https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
  https://phoenixnap.com/kb/access-denied-for-user-root-localhost
  https://dailydoseoftech.com/solved-error-1698-28000-access-denied-for-user-rootlocalhost/
  https://dba.stackexchange.com/questions/209996/error-1698-28000-access-denied-for-user-rootlocalhost




```





































