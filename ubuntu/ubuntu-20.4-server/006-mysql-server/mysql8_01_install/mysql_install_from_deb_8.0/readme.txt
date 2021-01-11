


mysql 的 国内镜像:
  清华大学开源软件镜像站:       https://mirrors.tuna.tsinghua.edu.cn/
  中国科学技术大学开源软件镜像: https://mirrors.ustc.edu.cn/ 



//做一些初始化的设置,
 如:
 设置 主机名, 网络参数(静态ip等), 时区, 时间同步, 国内镜像源(安装其某些依赖包)等

---------------------------------------------------------------------------------------------------

# 配置国内的 mysql 镜像站: 参考 https://mirrors.tuna.tsinghua.edu.cn/help/mysql/
# 注: 关于 sources.list 的内容格式，见 `man sources.list`


ysg@vm01:~$ sudo vim /etc/apt/sources.list.d/mysql-community.list

  deb https://mirrors.tuna.tsinghua.edu.cn/mysql/apt/ubuntu focal mysql-5.6 mysql-5.7 mysql-8.0 mysql-tools


ysg@vm01:~$ sudo apt-get update

  如上命令提示报问题: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY 8C718D3B5072E1F5

// 解决办法:
ysg@vm01:~$ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8C718D3B5072E1F5   #注: 此处的 8C718D3B5072E1F5 来自错误提示
    Executing: /tmp/apt-key-gpghome.RBUxFptdrE/gpg.1.sh --keyserver keyserver.ubuntu.com --recv-keys 8C718D3B5072E1F5
    gpg: key 8C718D3B5072E1F5: 1 duplicate signature removed
    gpg: key 8C718D3B5072E1F5: public key "MySQL Release Engineering <mysql-build@oss.oracle.com>" imported
    gpg: Total number processed: 1
    gpg:               imported: 1


ysg@vm01:~$ sudo apt-get update
ysg@vm01:~$ apt list mysql-server  #注: 如果想列出所有可用的版本，可用加上 '-a' 选项
  Listing... Done
  mysql-server/unknown 8.0.22-1ubuntu20.04 amd64
  N: There are 2 additional versions. Please use the '-a' switch to see them.

---------------------------------------------------------------------------------------------------
禁止 apt install 安装 package 时 daemon service 自动启动

    ysg@vm01:~$ sudo vim /usr/sbin/policy-rc.d
      #!/bin/sh
      exit 101
      EOF

    ysg@vm01:~$ sudo chmod a+x /usr/sbin/policy-rc.d

       //此时可以执行任意的 package 的安装操作, 如执行 `apt -y install nginx` 等

    ysg@vm01:~$ sudo apt install mysql-server=8.0.22-1ubuntu20.04  #安装版本为 8.0.22-1ubuntu20.04 的 mysql-server

        注: 在安装 mysql-server 的过程中会自动弹出对话框以 修改 password





---------------------------------------------------------------------------------------------------

ysg@vm01:~$ dpkg -l mysql-server   #或执行命令 `apt list mysql-server --installed` 查看
  Desired=Unknown/Install/Remove/Purge/Hold
  | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
  |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
  ||/ Name           Version             Architecture Description
  +++-==============-===================-============-=====================================================
  ii  mysql-server   8.0.22-1ubuntu20.04 amd64        MySQL Server meta package depending on latest version




ysg@vm01:~$ systemctl is-active mysql.service
  inactive  <----可以发现, mysql.service 在 执行类似 apt install 安装的时候并没有自动启动 daemon service, 这正式想要的效果


此时可以根据需要 通过 `sudo vim /etc/mysql/my.cnf` 等命令 来编辑 my.cnf 使其满足自己的需求

  注: mysql8 默认在 在 Unix and Unix-Like Systems 上读取配置文件的顺序(后读取的具有更高的优先级):
          https://dev.mysql.com/doc/refman/5.7/en/option-files.html

        On Unix and Unix-like systems, MySQL programs read startup options from the files shown in the following table,
        in the specified order (files listed first are read first, files read later take precedence).

            Table 4.2 Option Files Read on Unix and Unix-Like Systems
            ---------------------|---------------------------------------------------------
            File Name            |  Purpose
            ---------------------|---------------------------------------------------------
            /etc/my.cnf          |  Global options
            ---------------------|---------------------------------------------------------
            /etc/mysql/my.cnf    |  Global options
            ---------------------|---------------------------------------------------------
            SYSCONFDIR/my.cnf    |  Global options
            ---------------------|---------------------------------------------------------
            $MYSQL_HOME/my.cnf   |  Server-specific options (server only)
            ---------------------|---------------------------------------------------------
            defaults-extra-file  |  The file specified with --defaults-extra-file, if any
            ---------------------|---------------------------------------------------------
            ~/.my.cnf            |  User-specific options
            ---------------------|---------------------------------------------------------
            ~/.mylogin.cnf       |  User-specific login path options (clients only)
            ---------------------|---------------------------------------------------------





ysg@vm01:~$ sudo systemctl start mysql.service   #启动 mysql 服务
ysg@vm01:~$ sudo systemctl enable mysql.service  #设置为开机自启(注:  ubuntu 中 apt 下载后可能就自动设置为开机自启了, 不管怎样，安装任何 daemon service 的package 后都最好明确确认一下)




ysg@vm01:~$ mysql_secure_installation    #安全初始化设置

VALIDATE PASSWORD COMPONENT can be used to test passwords
and improve security. It checks the strength of password
and allows the users to set only those passwords which are
secure enough. Would you like to setup VALIDATE PASSWORD component?

Press y|Y for Yes, any other key for No:   <-----不进行密码的 validate 检查

Using existing password for root.
Change the password for root ? ((Press y|Y for Yes, any other key for No) : No  <------不修改 root 密码


Remove anonymous users? (Press y|Y for Yes, any other key for No) : y  <-------删除匿名账号
Success.


Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y <-----禁止 root 远程登录
Success.

Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y  <------删除 test 数据库 及其 相关授权
 - Dropping test database...
Success.


Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y  <------重新加载授权表



ysg@vm01:~$ mysql -u root -p --default-character-set=utf8mb4



    mysql> status
    --------------
    mysql  Ver 8.0.22 for Linux on x86_64 (MySQL Community Server - GPL)

    Connection id:          12
    Current database:
    Current user:           root@localhost
    SSL:                    Not in use
    Current pager:          stdout
    Using outfile:          ''
    Using delimiter:        ;
    Server version:         8.0.22 MySQL Community Server - GPL
    Protocol version:       10
    Connection:             Localhost via UNIX socket
    Server characterset:    utf8mb4
    Db     characterset:    utf8mb4
    Client characterset:    utf8mb4
    Conn.  characterset:    utf8mb4
    UNIX socket:            /var/run/mysqld/mysqld.sock
    Binary data as:         Hexadecimal
    Uptime:                 12 min 23 sec

    Threads: 2  Questions: 13  Slow queries: 0  Opens: 129  Flush tables: 3  Open tables: 50  Queries per second avg: 0.017
    --------------


    mysql> USE mysql;
    Reading table information for completion of table and column names
    You can turn off this feature to get a quicker startup with -A

    Database changed
    mysql> SELECT User, Host, plugin FROM mysql.user;  <-----查看验证插件
    +------------------+-----------+-----------------------+
    | User             | Host      | plugin                |
    +------------------+-----------+-----------------------+
    | mysql.infoschema | localhost | caching_sha2_password |
    | mysql.session    | localhost | caching_sha2_password |
    | mysql.sys        | localhost | caching_sha2_password |
    | root             | localhost | caching_sha2_password |
    +------------------+-----------+-----------------------+
    4 rows in set (0.00 sec)

    mysql> SHOW VARIABLES LIKE 'character%';   <-------查看字符集
    +--------------------------+--------------------------------+
    | Variable_name            | Value                          |
    +--------------------------+--------------------------------+
    | character_set_client     | utf8mb4                        |
    | character_set_connection | utf8mb4                        |
    | character_set_database   | utf8mb4                        |
    | character_set_filesystem | binary                         |
    | character_set_results    | utf8mb4                        |
    | character_set_server     | utf8mb4                        |
    | character_set_system     | utf8                           |
    | character_sets_dir       | /usr/share/mysql-8.0/charsets/ |
    +--------------------------+--------------------------------+
    8 rows in set (0.01 sec)

    mysql> SHOW VARIABLES LIKE 'collation%';  <--------查看字符比较规则
    +----------------------+--------------------+
    | Variable_name        | Value              |
    +----------------------+--------------------+
    | collation_connection | utf8mb4_0900_ai_ci | <---关于utf8mb4_0900_ai_ci 作用见 https://www.rednn.com/createsite/202004/01209.html
    | collation_database   | utf8mb4_0900_ai_ci | <--- 最好修改为类似 utf8mb4_unicode_ci或者utf8mb4_general_ci 的排序规则, 见 https://www.rednn.com/createsite/202003/26109.html
    | collation_server     | utf8mb4_0900_ai_ci |
    +----------------------+--------------------+
    3 rows in set (0.01 sec)

    mysql> quit
    Bye



ysg@vm01:~$ sudo ss -anptu | grep :3306
  tcp    LISTEN  0       70                      *:33060                 *:*       users:(("mysqld",pid=5373,fd=32))
  tcp    LISTEN  0       151                     *:3306                  *:*       users:(("mysqld",pid=5373,fd=34))


 // 关于 mysql8 的 tcp/33060 或其他端口 的信息见
    https://dev.mysql.com/doc/mysql-port-reference/en/mysql-ports-reference-tables.html
    https://stackoverflow.com/questions/63556825/what-is-the-port-33060-for-mysql-server-ports-in-addition-to-the-port-3306

      Port 3306 is the default port for the classic MySQL protocol (port), which is used by the mysql client,
      MySQL Connectors, and utilities such as mysqldump and mysqlpump. The port for X Protocol (mysqlx_port),
      supported by clients such as MySQL Shell, MySQL Connectors and MySQL Router,
      is calculated by multiplying the port used for classic MySQL protocol by 10.
      For example if the classic MySQL protocol port is the default value of 3306 then the X Protocol port is 33060.








---------------------------------------------------------------------------------------------------

网上资料:
    https://www.server-world.info/en/note?os=Ubuntu_20.04&p=mysql8&f=1
    https://www.fosstechnix.com/how-to-install-mysql-8-on-ubuntu-20-04/
    https://www.cyberciti.biz/faq/install-mysql-server-8-on-ubuntu-20-04-lts-linux/
    https://computingforgeeks.com/how-to-install-mysql-8-on-ubuntu/




导入key:
  https://chrisjean.com/fix-apt-get-update-the-following-signatures-couldnt-be-verified-because-the-public-key-is-not-available/
  https://askubuntu.com/questions/291035/how-to-add-a-gpg-key-to-the-apt-sources-keyring

    $ sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 8C718D3B5072E1F5


apt 安装 packages 时避免 自动启动
  https://serverfault.com/questions/861583/how-to-stop-nginx-from-being-automatically-started-on-install
  https://serverfault.com/questions/567474/how-can-i-install-packages-without-starting-their-associated-services
  https://askubuntu.com/questions/74061/install-packages-without-starting-background-processes-and-services
  https://askubuntu.com/questions/482928/ignore-apt-get-postinstall-scripts-automatically

  方法1: 该方法不一定完整，但在大多数时候应该是可以的

      $ sudo vim /usr/sbin/policy-rc.d
        #!/bin/sh
        exit 101
        EOF

      $ sudo chmod a+x /usr/sbin/policy-rc.d



  方法2(失败): //注: 实际测试 方法 2 并没有成功
    ysg@vm01:~$ sudo su -
    root@vm01:~# dpkg-divert --add --rename --local /sbin/start-stop-daemon


    root@vm01:~# echo '
    #!/bin/sh
    echo
    echo "Warning: Fake start-stop-daemon called, doing nothing"' > /sbin/start-stop-daemon

    root@vm01:~# chmod 755 /sbin/start-stop-daemon

       //此时可以执行任意的 package 的安装操作, 如执行 `apt -y install nginx` 等


    root@vm01:~# rm /sbin/start-stop-daemon
    root@vm01:~# dpkg-divert --remove --rename /sbin/start-stop-daemon




mysql8 比较规则 utf8mb4_0900_ai_ci 的问题:
  https://www.rednn.com/createsite/202004/01209.html
  https://www.rednn.com/createsite/202003/26109.html








