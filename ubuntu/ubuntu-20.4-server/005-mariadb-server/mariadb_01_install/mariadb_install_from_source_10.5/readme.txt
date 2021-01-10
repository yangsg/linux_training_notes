



mariadb 下载页面:
  https://downloads.mariadb.org/


从源码编译 mariadb:
  https://mariadb.com/kb/en/compiling-mariadb-from-source/


在 ubuntu 上构建 mariadb:
  https://mariadb.com/kb/en/building-mariadb-on-ubuntu/

添加 mariadb 仓库
  https://downloads.mariadb.org/mariadb/repositories/#mirror=escience


Generic Build Instructions
  https://mariadb.com/kb/en/generic-build-instructions/






---------------------------------------------------------------------------------------------------

ysg@vm01:~$ sudo mkdir /app   #// 创建目标安装目录，准备将mysql安装到该目录下


:) 获取 mysql 源码包
  https://mariadb.com/kb/en/getting-the-mariadb-source-code/

ysg@vm01:~$ mkdir download
ysg@vm01:~$ cd download/
ysg@vm01:~/download$ wget -O mariadb-10.5.8.tar.gz https://mirrors.nju.edu.cn/mariadb//mariadb-10.5.8/source/mariadb-10.5.8.tar.gz
ysg@vm01:~/download$ tar -xvf mariadb-10.5.8.tar.gz
ysg@vm01:~/download$ cd mariadb-10.5.8/
ysg@vm01:~/download/mariadb-10.5.8$ sudo useradd -r -s /bin/false mysql
ysg@vm01:~/download/mariadb-10.5.8$ sudo mkdir -p /mydata/data
ysg@vm01:~/download/mariadb-10.5.8$ sudo chown -R mysql:mysql /mydata/data/


ysg@vm01:~/download/mariadb-10.5.8$ mkdir build-mariadb  #创建外部构建目录
ysg@vm01:~/download/mariadb-10.5.8$ cd build-mariadb/
ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ sudo apt-get install pkg-config  #安装 pkg-config, 否则执行 cmake .. 时有可能提示找不到 PkgConfig







:) 设置 build 环境
  https://mariadb.com/kb/en/Build_Environment_Setup_for_Linux/


// 安装必要的软件包 和 添加 仓库
 参考:  https://mariadb.com/kb/en/building-mariadb-on-ubuntu/

ysg@vm01:~$ sudo apt-get update
ysg@vm01:~$ sudo apt-get install software-properties-common devscripts equivs -y

// 添加仓库，准备安装构建依赖
  https://downloads.mariadb.org/mariadb/repositories/#mirror=escience


// 导入验证 key
ysg@vm01:~$ sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'


// 添加仓库配置
ysg@vm01:~$ sudo vim  /etc/apt/sources.list.d/MariaDB-Server-10.5.list

    # MariaDB 10.5 repository list - created 2021-01-09 13:47 UTC
    # http://downloads.mariadb.org/mariadb/repositories/
    deb [arch=amd64] https://mirrors.nju.edu.cn/mariadb/repo/10.5/ubuntu focal main
    deb-src https://mirrors.nju.edu.cn/mariadb/repo/10.5/ubuntu focal main


ysg@vm01:~$ sudo apt-get update
ysg@vm01:~$ sudo apt-get build-dep mariadb-server-10.5


----------------------------------------

// 先查看一下 默认的 cmake build options 有哪些且其 默认 values 是什么
ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ cmake ..  #注: 本次 `cmake ..` 仅是为了观察可用的构建参数及其默认值
ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ cmake -LA # 列出可用的构建参数及其默认值

        CMAKE_INSTALL_PREFIX:PATH=/usr/local/mysql  <---可以观察到, 默认的安装目标目录为 /usr/local/mysql
        INSTALL_UNIX_ADDRDIR:STRING=/tmp/mysql.sock





:) 开始正式的 cmake 构建
ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ cd ..
ysg@vm01:~/download/mariadb-10.5.8$ rm -rf build-mariadb/
ysg@vm01:~/download/mariadb-10.5.8$ mkdir build-mariadb
ysg@vm01:~/download/mariadb-10.5.8$ cd build-mariadb/


ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ cmake .. \
                   -DCMAKE_INSTALL_PREFIX=/app/mysql \
                   -DINSTALL_UNIX_ADDRDIR=/tmp/mysql.sock


// 观察一下提供的参数是否被插入了
ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ cmake -LA | grep -E '/app/mysql|/tmp/mysql.sock'

  CMAKE_INSTALL_PREFIX:PATH=/app/mysql
  GRN_DEFAULT_DOCUMENT_ROOT:PATH=/app/mysql/share/groonga/html/admin
  GRN_LOG_PATH:FILEPATH=/app/mysql/var/log/groonga/groonga.log
  INSTALL_UNIX_ADDRDIR:STRING=/tmp/mysql.sock
  MYSQL_DATADIR:PATH=/app/mysql/data


ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ make
ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ sudo make install



ysg@vm01:~$ sudo chown -R root:mysql /app/mysql/

ysg@vm01:~$ sudo vim /etc/profile

  export PATH=$PATH:/app/mysql/bin


ysg@vm01:~$ source /etc/profile


ysg@vm01:~$ cd /app/mysql/
ysg@vm01:/app/mysql$ ls -F
  bin/     CREDITS            include/        lib/  mysql-test/  README-wsrep  share/      support-files/
  COPYING  EXCEPTIONS-CLIENT  INSTALL-BINARY  man/  README.md    scripts/      sql-bench/  THIRDPARTY



ysg@vm01:/app/mysql$ sudo vim /etc/my.cnf

    [client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
    loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

    [mysql]
    default-character-set = utf8mb4

    [mysqlbinlog]
    set_charset=utf8mb4

    [mysqld]
    # 设置 mysql 字符集为 utf8mb4
    character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
    collation-server = utf8mb4_unicode_ci

    basedir=/app/mysql
    datadir=/mydata/data
    port=3306
    server_id=133
    socket=/tmp/mysql.sock

    skip-name-resolve=ON







ysg@vm01:/app/mysql$ sudo ./scripts/mysql_install_db --defaults-file=/etc/my.cnf --user=mysql
    Installing MariaDB/MySQL system tables in '/mydata/data' ...
    OK

    To start mysqld at boot time you have to copy
    support-files/mysql.server to the right place for your system


    Two all-privilege accounts were created.
    One is root@localhost, it has no password, but you need to
    be system 'root' user to connect. Use, for example, sudo mysql
    The second is mysql@localhost, it has no password either, but
    you need to be the system 'mysql' user to connect.
    After connecting you can set the password, if you would need to be
    able to connect as any of these users with a password and without sudo

    See the MariaDB Knowledgebase at https://mariadb.com/kb or the
    MySQL manual for more instructions.

    You can start the MariaDB daemon with:
    cd '/app/mysql' ; /app/mysql/bin/mysqld_safe --datadir='/mydata/data'

    You can test the MariaDB daemon with mysql-test-run.pl
    cd '/app/mysql/mysql-test' ; perl mysql-test-run.pl

    Please report any problems at https://mariadb.org/jira

    The latest information about MariaDB is available at https://mariadb.org/.
    You can find additional information about the MySQL part at:
    https://dev.mysql.com
    Consider joining MariaDB's strong and vibrant community:
    https://mariadb.org/get-involved/



//设置开机自启
ysg@vm01:/app/mysql$ sudo cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld
ysg@vm01:/app/mysql$ sudo chmod a+x /etc/init.d/mysqld


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


ysg@vm01:/app/mysql$ systemctl status mysqld | less   #使用命令 `systemctl status mysqld` 查看 mysqld 服务状态

    ● mysqld.service - LSB: start and stop MariaDB
         Loaded: loaded (/etc/init.d/mysqld; generated)
         Active: active (running) since Sun 2021-01-10 08:34:56 UTC; 13s ago
           Docs: man:systemd-sysv-generator(8)
        Process: 77593 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)
          Tasks: 13 (limit: 1041)
         Memory: 61.4M
         CGroup: /system.slice/mysqld.service
                 ├─77635 /bin/sh /app/mysql/bin/mysqld_safe --datadir=/mydata/data --pid-file=/mydata/data/vm01.pid
                 └─77734 /app/mysql/bin/mariadbd --basedir=/app/mysql --datadir=/mydata/data --plugin-dir=/app/mysql/lib/plugin --user=mysql --log-error=/mydata/data/vm01.err --pid-file=/mydata/data/vm01.pid --socket=/tmp/mysql.sock --port=3306

    Jan 10 08:34:55 vm01 systemd[1]: Starting LSB: start and stop MariaDB...
    Jan 10 08:34:55 vm01 mysqld[77593]: Starting MariaDB
    Jan 10 08:34:55 vm01 mysqld[77593]: .
    Jan 10 08:34:55 vm01 mysqld[77635]: 210110 08:34:55 mysqld_safe Logging to '/mydata/data/vm01.err'.
    Jan 10 08:34:55 vm01 mysqld[77635]: 210110 08:34:55 mysqld_safe Starting mariadbd daemon with databases from /mydata/data
    Jan 10 08:34:56 vm01 mysqld[77593]:  *
    Jan 10 08:34:56 vm01 systemd[1]: Started LSB: start and stop MariaDB.





ysg@vm01:/app/mysql$ /etc/init.d/mysqld status  #使用命令 `/etc/init.d/mysqld status` 查看 mysqld 服务状态

    ● mysqld.service - LSB: start and stop MariaDB
         Loaded: loaded (/etc/init.d/mysqld; generated)
         Active: active (running) since Sun 2021-01-10 08:34:56 UTC; 57s ago
           Docs: man:systemd-sysv-generator(8)
        Process: 77593 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)
          Tasks: 13 (limit: 1041)
         Memory: 61.4M
         CGroup: /system.slice/mysqld.service
                 ├─77635 /bin/sh /app/mysql/bin/mysqld_safe --datadir=/mydata/data --pid-file=/mydata/data/vm01.pid
                 └─77734 /app/mysql/bin/mariadbd --basedir=/app/mysql --datadir=/mydata/data --plugin-dir=/app/mysql/lib/plugin --user=mysql --log-error=/mydata/…

    Jan 10 08:34:55 vm01 systemd[1]: Starting LSB: start and stop MariaDB...
    Jan 10 08:34:55 vm01 mysqld[77593]: Starting MariaDB
    Jan 10 08:34:55 vm01 mysqld[77593]: .
    Jan 10 08:34:55 vm01 mysqld[77635]: 210110 08:34:55 mysqld_safe Logging to '/mydata/data/vm01.err'.
    Jan 10 08:34:55 vm01 mysqld[77635]: 210110 08:34:55 mysqld_safe Starting mariadbd daemon with databases from /mydata/data
    Jan 10 08:34:56 vm01 mysqld[77593]:  *
    Jan 10 08:34:56 vm01 systemd[1]: Started LSB: start and stop MariaDB.



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

  tcp    LISTEN  0       80                      *:3306                  *:*       users:(("mariadbd",pid=77734,fd=19))




ysg@vm01:/app/mysql$ sudo ./bin/mysql_secure_installation --basedir=/app/mysql/
    print: /app/mysql//bin/my_print_defaults

    NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
          SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

    In order to log into MariaDB to secure it, we'll need the current
    password for the root user. If you've just installed MariaDB, and
    haven't set the root password yet, you should just press enter here.

    Enter current password for root (enter for none):
    OK, successfully used password, moving on...

    Setting the root password or using the unix_socket ensures that nobody
    can log into the MariaDB root user without the proper authorisation.

    You already have your root account protected, so you can safely answer 'n'.

    Switch to unix_socket authentication [Y/n] n
     ... skipping.

    You already have your root account protected, so you can safely answer 'n'.

    Change the root password? [Y/n] y
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

    Remove anonymous users? [Y/n] y
     ... Success!

    Normally, root should only be allowed to connect from 'localhost'.  This
    ensures that someone cannot guess at the root password from the network.

    Disallow root login remotely? [Y/n] y
     ... Success!

    By default, MariaDB comes with a database named 'test' that anyone can
    access.  This is also intended only for testing, and should be removed
    before moving into a production environment.

    Remove test database and access to it? [Y/n] y
     - Dropping test database...
     ... Success!
     - Removing privileges on test database...
     ... Success!

    Reloading the privilege tables will ensure that all changes made so far
    will take effect immediately.

    Reload privilege tables now? [Y/n] y
     ... Success!

    Cleaning up...

    All done!  If you've completed all of the above steps, your MariaDB
    installation should now be secure.

    Thanks for using MariaDB!




ysg@vm01:~$ mysql -u root -p --default-character-set=utf8mb4
    Enter password:
    Welcome to the MariaDB monitor.  Commands end with ; or \g.
    Your MariaDB connection id is 14
    Server version: 10.5.8-MariaDB Source distribution

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
    3 rows in set (0.002 sec)

    MariaDB [mysql]> SHOW VARIABLES LIKE 'character%';   #观察字符集
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
    | character_sets_dir       | /app/mysql/share/charsets/ |
    +--------------------------+----------------------------+
    8 rows in set (0.001 sec)

    MariaDB [mysql]> SHOW VARIABLES LIKE 'collation%';    #观察比较规则
    +----------------------+--------------------+
    | Variable_name        | Value              |
    +----------------------+--------------------+
    | collation_connection | utf8mb4_general_ci |
    | collation_database   | utf8mb4_unicode_ci |
    | collation_server     | utf8mb4_unicode_ci |
    +----------------------+--------------------+
    3 rows in set (0.001 sec)

    MariaDB [mysql]> status
    --------------
    mysql  Ver 15.1 Distrib 10.5.8-MariaDB, for Linux (x86_64) using readline 5.2

    Connection id:          14
    Current database:       mysql
    Current user:           root@localhost
    SSL:                    Not in use
    Current pager:          stdout
    Using outfile:          ''
    Using delimiter:        ;
    Server:                 MariaDB
    Server version:         10.5.8-MariaDB Source distribution
    Protocol version:       10
    Connection:             Localhost via UNIX socket
    Server characterset:    utf8mb4
    Db     characterset:    utf8mb4
    Client characterset:    utf8mb4
    Conn.  characterset:    utf8mb4
    UNIX socket:            /tmp/mysql.sock
    Uptime:                 7 min 13 sec

    Threads: 2  Questions: 63  Slow queries: 0  Opens: 36  Open tables: 30  Queries per second avg: 0.145
    --------------

    MariaDB [mysql]> quit






安装完毕
----------------------------------------



其他:




问题: 构建时找不到 PkgConfig:
  ysg@vm01:~/download/mariadb-10.5.8/build-mariadb$ cmake ..
  -- Running cmake version 3.16.3
  -- MariaDB 10.5.8
  -- Wsrep-lib version: 1.0.0
  -- Could NOT find PkgConfig (missing: PKG_CONFIG_EXECUTABLE) <---执行cmake .. 时出现无法找到 PkgConfig 的问题解决办法:`sudo apt install pkg-config`
  == Configuring MariaDB Connector/C
  -- Dynamic column API support: ON
  -- Could NOT find PkgConfig (missing: PKG_CONFIG_EXECUTABLE)


  关于 pkg-config
    https://www.freedesktop.org/wiki/Software/pkg-config/
      ysg@vm01:~$ sudo apt install pkg-config






列出 所有的 CMake build options 及其 default values?
  https://stackoverflow.com/questions/16851084/how-to-list-all-cmake-build-options-and-their-default-values

        mkdir build
        cd build
        cmake ..
        cmake -LA | awk '{if(f)print} /-- Cache values/{f=1}'

cmake 的外部构建:
  Looking for a 'cmake clean' command to clear up CMake output
      https://stackoverflow.com/questions/9680420/looking-for-a-cmake-clean-command-to-clear-up-cmake-output#:~:text=%28CMake%20does%20generate%20a%20%22make%20clean%22%20target%20to,to%20adopt%20the%20notion%20of%20an%20out-of-source%20build.

  How to clean up the project files generated by cmake?
    https://www.howtobuildsoftware.com/index.php/how-do/bIeT/cmake-how-to-clean-up-the-project-files-generated-by-cmake



网上资料:

  https://blog.csdn.net/sadcd/article/details/104482775


