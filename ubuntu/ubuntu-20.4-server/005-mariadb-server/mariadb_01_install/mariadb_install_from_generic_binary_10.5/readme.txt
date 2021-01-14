
//做一些初始化的设置,
 如:
 设置 主机名, 网络参数(静态ip等), 时区, 时间同步, 国内镜像源(安装其某些依赖包)等



ysg@vm01:~$ sudo apt-get update
ysg@vm01:~$ sudo apt-get install libncurses5 -y
ysg@vm01:~$ dpkg -l libncurses5
  Desired=Unknown/Install/Remove/Purge/Hold
  | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
  |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
  ||/ Name              Version      Architecture Description
  +++-=================-============-============-=======================================================
  ii  libncurses5:amd64 6.2-0ubuntu2 amd64        shared libraries for terminal handling (legacy version)



ysg@vm01:~$ sudo mkdir /app
ysg@vm01:~$ sudo useradd -r -s /bin/false mysql

ysg@vm01:~$ sudo mkdir -p /mydata/data
ysg@vm01:~$ sudo chown -R mysql:mysql /mydata/data/





ysg@vm01:~$ cd download/
ysg@vm01:~/download$ ls
  mariadb-10.5.8-linux-systemd-x86_64.tar.gz


ysg@vm01:~/download$ sudo tar -C /app/  -xvf mariadb-10.5.8-linux-systemd-x86_64.tar.gz
ysg@vm01:~/download$ cd /app/
ysg@vm01:/app$ ls
  mariadb-10.5.8-linux-systemd-x86_64


ysg@vm01:/app$ sudo ln -s /app/mariadb-10.5.8-linux-systemd-x86_64 mysql
ysg@vm01:/app$ cd mysql

ysg@vm01:/app/mysql$ ls -F
  bin/     CREDITS            include/        lib/  mysql-test/  README-wsrep  share/      support-files/
  COPYING  EXCEPTIONS-CLIENT  INSTALL-BINARY  man/  README.md    scripts/      sql-bench/  THIRDPARTY


ysg@vm01:/app/mysql$ sudo chown -R root:mysql /app/mysql/


ysg@vm01:/app/mysql$ sudo vim /etc/profile

  export PATH=$PATH:/app/mysql/bin


ysg@vm01:/app/mysql$ source /etc/profile


ysg@vm01:/app/mysql$ ./scripts/mysql_install_db --help | less  # 查看一下 mysql_install_db 的可用参数
  --basedir=path       The path to the MariaDB installation directory.
  --datadir=path       The path to the MariaDB data directory.
  --defaults-file=name Only read default options from the given file name.
  --user=user_name     The login username to use for running mysqld.  Files
                       and directories created by mysqld will be owned by this
                       user.  You must be root to use this option.  By default
                       mysqld runs using your current login name and files and
                       directories that it creates will be owned by you.


ysg@vm01:/app/mysql$ sudo vim /etc/my.cnf

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

    basedir=/app/mysql
    datadir=/mydata/data
    port=3306
    server_id=133
    socket=/tmp/mysql.sock

    skip-name-resolve=ON




ysg@vm01:/app/mysql$ sudo ./scripts/mysql_install_db --defaults-file=/etc/my.cnf --user=mysql
    [sudo] password for ysg:
    Installing MariaDB/MySQL system tables in '/mydata/data' ...
    OK

    To start mysqld at boot time you have to copy
    support-files/mysql.server to the right place for your system <---注: 设置开机自启的方式


    Two all-privilege accounts were created. <---创建了2个 all-privilege 的账号, 即 root@localhost 和 mysql@localhost, 它们都没有设置密码,
                                                 root@localhost 可以使用 `sudo mysql` 命令利用 系统的 root 账号来连接登录,
                                                 mysql@localhost 可以通过系统账号 mysql 来连接登录
    One is root@localhost, it has no password, but you need to
    be system 'root' user to connect. Use, for example, sudo mysql
    The second is mysql@localhost, it has no password either, but
    you need to be the system 'mysql' user to connect.
    After connecting you can set the password, if you would need to be
    able to connect as any of these users with a password and without sudo

    See the MariaDB Knowledgebase at https://mariadb.com/kb or the
    MySQL manual for more instructions.

    You can start the MariaDB daemon with:
    cd '/app/mysql' ; /app/mysql/bin/mysqld_safe --datadir='/mydata/data'  <---启动MariaDB daemon 的命令

    You can test the MariaDB daemon with mysql-test-run.pl
    cd '/app/mysql//mysql-test' ; perl mysql-test-run.pl  <---测试 MariaDB daemon 的命令

    Please report any problems at https://mariadb.org/jira

    The latest information about MariaDB is available at https://mariadb.org/.
    You can find additional information about the MySQL part at:
    https://dev.mysql.com
    Consider joining MariaDB's strong and vibrant community:
    https://mariadb.org/get-involved/


//设置开机自启
ysg@vm01:/app/mysql$ sudo cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld
ysg@vm01:/app/mysql$ sudo chmod a+x /etc/init.d/mysqld

// 注: 如上命令没有采用类似 `cp support-files/systemd/mariadb.service /usr/lib/systemd/system/mariadb.service`
//     这种方式，因为我的 mairadb 安装安装到了自定义的 /app 目录，没有安装到其默认的 /usr/local 目录，
//     而文件 `support-files/systemd/mariadb.service` 没有提供直观简单的修改 basedir 和 datadir 参数的方式,
//     所以此处我采用了 `sudo cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld` 的方式,
//     其在启动时也会自动生成文件 '/run/systemd/generator.late/mysqld.service' 来借助 systemd 来管理

// 因为没有采用默认的 /usr/local 安装目录，所以需要编辑修改启动脚本中的 basedir 和 datadir 参数
ysg@vm01:/app/mysql$ sudo vim /etc/init.d/mysqld

    basedir=/app/mysql
    datadir=/mydata/data

// ubuntu 不再使用 chkconfig, 其使用的是 update-rc.d
ysg@vm01:~$ sudo update-rc.d mysqld defaults
ysg@vm01:~$ find /etc/rc*.d  | grep mysqld  # 可以观察到, 默认 2 3 4 5 会被设置为开机自启
  /etc/rc0.d/K01mysqld
  /etc/rc1.d/K01mysqld
  /etc/rc2.d/S01mysqld
  /etc/rc3.d/S01mysqld
  /etc/rc4.d/S01mysqld
  /etc/rc5.d/S01mysqld
  /etc/rc6.d/K01mysqld

ysg@vm01:~$ sudo /etc/init.d/mysqld start  #启动 mysqld 服务
  Starting mysqld (via systemctl): mysqld.service. <---观察这一行信息


ysg@vm01:~$ systemctl status mysqld  #使用命令 `systemctl status mysqld` 查看 mysqld 服务状态
  ● mysqld.service - LSB: start and stop MariaDB
       Loaded: loaded (/etc/init.d/mysqld; generated)
       Active: active (running) since Sun 2021-01-10 00:52:15 UTC; 2min 45s ago
         Docs: man:systemd-sysv-generator(8)
      Process: 8441 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)
        Tasks: 11 (limit: 1041)
       Memory: 63.4M
       CGroup: /system.slice/mysqld.service
               ├─8474 /bin/sh /app/mysql/bin/mysqld_safe --datadir=/mydata/data --pid-file=/mydata/data/vm01.pid
               └─8562 /app/mysql/bin/mariadbd --basedir=/app/mysql --datadir=/mydata/data --plugin-dir=/app/mysql/lib/plugin --user=mysql --log-error=/mydata/data/vm01.err --pid-file=/mydata/data/vm01.pid --socket=/tmp/mysql.sock --port=3306

  Jan 10 00:52:14 vm01 systemd[1]: Starting LSB: start and stop MariaDB...
  Jan 10 00:52:14 vm01 mysqld[8441]: Starting MariaDB
  Jan 10 00:52:14 vm01 mysqld[8474]: 210110 00:52:14 mysqld_safe Logging to '/mydata/data/vm01.err'.
  Jan 10 00:52:14 vm01 mysqld[8474]: 210110 00:52:14 mysqld_safe Starting mariadbd daemon with databases from /mydata/data
  Jan 10 00:52:15 vm01 mysqld[8441]: . *
  Jan 10 00:52:15 vm01 systemd[1]: Started LSB: start and stop MariaDB.

ysg@vm01:/app/mysql$ /etc/init.d/mysqld status  #使用命令 `/etc/init.d/mysqld status` 查看 mysqld 服务状态
  ● mysqld.service - LSB: start and stop MariaDB
       Loaded: loaded (/etc/init.d/mysqld; generated)
       Active: active (running) since Sun 2021-01-10 00:52:15 UTC; 6min ago
         Docs: man:systemd-sysv-generator(8)
      Process: 8441 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)
        Tasks: 10 (limit: 1041)
       Memory: 63.3M
       CGroup: /system.slice/mysqld.service
               ├─8474 /bin/sh /app/mysql/bin/mysqld_safe --datadir=/mydata/data --pid-file=/mydata/data/vm01.pid
               └─8562 /app/mysql/bin/mariadbd --basedir=/app/mysql --datadir=/mydata/data --plugin-dir=/app/mysql/lib/plugin --user=mysql --log-error=/mydata/d…

  Jan 10 00:52:14 vm01 systemd[1]: Starting LSB: start and stop MariaDB...
  Jan 10 00:52:14 vm01 mysqld[8441]: Starting MariaDB
  Jan 10 00:52:14 vm01 mysqld[8474]: 210110 00:52:14 mysqld_safe Logging to '/mydata/data/vm01.err'.
  Jan 10 00:52:14 vm01 mysqld[8474]: 210110 00:52:14 mysqld_safe Starting mariadbd daemon with databases from /mydata/data
  Jan 10 00:52:15 vm01 mysqld[8441]: . *
  Jan 10 00:52:15 vm01 systemd[1]: Started LSB: start and stop MariaDB.



ysg@vm01:~$ systemctl cat mysqld.service  #查看一下自动生成的 mysqld.service 的内容
  # /run/systemd/generator.late/mysqld.service  <---自动生成的 mysqld.service 的路径
  # Automatically generated by systemd-sysv-generator

  [Unit]
  Documentation=man:systemd-sysv-generator(8)
  SourcePath=/etc/init.d/mysqld
  Description=LSB: start and stop MariaDB
  Before=multi-user.target
  Before=multi-user.target
  Before=multi-user.target
  Before=graphical.target
  After=network-online.target
  After=remote-fs.target
  After=ypbind.service
  After=nscd.service
  After=ldap.service
  After=ntpd.service
  After=xntpd.service
  Wants=network-online.target

  [Service]
  Type=forking
  Restart=no
  TimeoutSec=5min
  IgnoreSIGPIPE=no
  KillMode=process
  GuessMainPID=no
  RemainAfterExit=yes
  SuccessExitStatus=5 6
  ExecStart=/etc/init.d/mysqld start
  ExecStop=/etc/init.d/mysqld stop
  ExecReload=/etc/init.d/mysqld reload


ysg@vm01:~$ sudo ss -anptu | grep 3306  #查看 mysqld  服务端口 //注:通过 sudo 执行 ss 命令才能看到类似 "users:(("mariadbd",pid=8562,fd=17))" 这样的信息

  tcp    LISTEN  0       80                       *:3306                 *:*       users:(("mariadbd",pid=8562,fd=17))      



ysg@vm01:/app/mysql$ sudo ./bin/mysql_secure_installation --basedir=/app/mysql/
  print: /app/mysql//bin/my_print_defaults

  NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
        SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

  In order to log into MariaDB to secure it, we'll need the current
  password for the root user. If you've just installed MariaDB, and
  haven't set the root password yet, you should just press enter here.

  Enter current password for root (enter for none):  <-----直接回车
  OK, successfully used password, moving on...

  Setting the root password or using the unix_socket ensures that nobody
  can log into the MariaDB root user without the proper authorisation.

  You already have your root account protected, so you can safely answer 'n'.

  Switch to unix_socket authentication [Y/n] n  <-----不切换至 unix_socket 验证
   ... skipping.

  You already have your root account protected, so you can safely answer 'n'.

  Change the root password? [Y/n] y  <-----修改 root 密码
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

  Remove anonymous users? [Y/n] y  <----删除匿名账号
   ... Success!

  Normally, root should only be allowed to connect from 'localhost'.  This
  ensures that someone cannot guess at the root password from the network.

  Disallow root login remotely? [Y/n] y  <----禁止 root 远程登录
   ... Success!

  By default, MariaDB comes with a database named 'test' that anyone can
  access.  This is also intended only for testing, and should be removed
  before moving into a production environment.

  Remove test database and access to it? [Y/n] y  <----删除 test 数据库及其授权
   - Dropping test database...
   ... Success!
   - Removing privileges on test database...
   ... Success!

  Reloading the privilege tables will ensure that all changes made so far
  will take effect immediately.

  Reload privilege tables now? [Y/n] y  <-----重新加载授权表
   ... Success!

  Cleaning up...

  All done!  If you've completed all of the above steps, your MariaDB
  installation should now be secure.

  Thanks for using MariaDB!





ysg@vm01:~$ mysql -u root -p --default-character-set=utf8mb4
    Enter password:
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 13
    Server version: 10.5.8-MariaDB MariaDB Server

    Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

    Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

    MariaDB [(none)]> use mysql
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Database changed
    MariaDB [mysql]> SELECT User, Host, plugin FROM mysql.user;
    +-------------+-----------+-----------------------+
    | User        | Host      | plugin                |
    +-------------+-----------+-----------------------+
    | mariadb.sys | localhost | mysql_native_password |
    | root        | localhost | mysql_native_password |
    | mysql       | localhost | mysql_native_password |
    +-------------+-----------+-----------------------+
    3 rows in set (0.001 sec)

    MariaDB [mysql]> SHOW VARIABLES LIKE 'character%';  #观察字符集
    +--------------------------+----------------------------------------------------------+
    | Variable_name            | Value                                                    |
    +--------------------------+----------------------------------------------------------+
    | character_set_client     | utf8mb4                                                  |
    | character_set_connection | utf8mb4                                                  |
    | character_set_database   | utf8mb4                                                  |
    | character_set_filesystem | binary                                                   |
    | character_set_results    | utf8mb4                                                  |
    | character_set_server     | utf8mb4                                                  |
    | character_set_system     | utf8                                                     |
    | character_sets_dir       | /app/mariadb-10.5.8-linux-systemd-x86_64/share/charsets/ |
    +--------------------------+----------------------------------------------------------+
    8 rows in set (0.001 sec)

    MariaDB [mysql]> SHOW VARIABLES LIKE 'collation%';    #观察比较规则
    +----------------------+--------------------+
    | Variable_name        | Value              |
    +----------------------+--------------------+
    | collation_connection | utf8mb4_unicode_ci |
    | collation_database   | utf8mb4_unicode_ci |
    | collation_server     | utf8mb4_unicode_ci |
    +----------------------+--------------------+
    3 rows in set (0.001 sec)

    MariaDB [mysql]> status
    --------------
    mysql  Ver 15.1 Distrib 10.5.8-MariaDB, for Linux (x86_64) using readline 5.1

    Connection id:          13
    Current database:       mysql
    Current user:           root@localhost
    SSL:                    Not in use
    Current pager:          stdout
    Using outfile:          ''
    Using delimiter:        ;
    Server:                 MariaDB
    Server version:         10.5.8-MariaDB MariaDB Server
    Protocol version:       10
    Connection:             Localhost via UNIX socket
    Server characterset:    utf8mb4
    Db     characterset:    utf8mb4
    Client characterset:    utf8mb4
    Conn.  characterset:    utf8mb4
    UNIX socket:            /tmp/mysql.sock
    Uptime:                 7 min 32 sec

    Threads: 2  Questions: 65  Slow queries: 0  Opens: 36  Open tables: 30  Queries per second avg: 0.143
    --------------

    MariaDB [mysql]> quit
    Bye



网上资料:
  https://code.i-harness.com/en/docs/mariadb/installing-mariadb-binary-tarballs/index
  https://dev.mysql.com/doc/refman/8.0/en/binary-installation.html
  https://blog.csdn.net/blueboz/article/details/109968308
  https://www.cnblogs.com/wuvikr/p/13788576.html



  ubuntu 的 update-rc.d (作用类似于 centos 中的 chkconfig)
    https://stackoverflow.com/questions/20680050/how-do-i-install-chkconfig-on-ubuntu











