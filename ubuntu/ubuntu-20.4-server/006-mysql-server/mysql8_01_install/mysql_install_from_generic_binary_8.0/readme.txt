


https://dev.mysql.com/doc/refman/8.0/en/binary-installation.html





ysg@vm01:~$ sudo apt update


:) 安装依赖包(如果没有安装该包，则 Data directory initialization 和后续的 server startup 步骤会失败)
ysg@vm01:~$ apt search libaio
ysg@vm01:~$ sudo apt install libaio1

// https://stackoverflow.com/questions/17005654/error-while-loading-shared-libraries-libncurses-so-5
ysg@vm01:~$ sudo apt install libncurses5

 注: 如果不安装 libncurses5, 后面步骤中使用 mysql_secure_installation 做安全初始化设置时可能包如下错误:
			mysql: error while loading shared libraries: libtinfo.so.5: cannot open shared object file: No such file or directory


ysg@vm01:~$ sudo mkdir /app
ysg@vm01:~$ sudo useradd -r -s /bin/false mysql
ysg@vm01:~$ sudo mkdir -p /mydata/data
ysg@vm01:~$ sudo chown -R mysql:mysql /mydata/data/


ysg@vm01:~$ cd download/
ysg@vm01:~/download$ tree
	.
	└── mysql-8.0.23-linux-glibc2.12-x86_64.tar.xz


ysg@vm01:~/download$ sudo tar -C /app/  -xvf mysql-8.0.23-linux-glibc2.12-x86_64.tar.xz
ysg@vm01:~/download$ cd /app/
ysg@vm01:/app$ ls
	mysql-8.0.23-linux-glibc2.12-x86_64

ysg@vm01:/app$ sudo ln -s /app/mysql-8.0.23-linux-glibc2.12-x86_64 mysql
ysg@vm01:/app$ cd mysql

ysg@vm01:/app/mysql$ ls -F
	bin/  docs/  include/  lib/  LICENSE  man/  README  share/  support-files/


ysg@vm01:/app/mysql$ sudo chown -R root:mysql /app/mysql/

ysg@vm01:/app/mysql$ sudo vim /etc/profile

		export PATH=$PATH:/app/mysql/bin

ysg@vm01:/app/mysql$ source /etc/profile



// 初始化数据库(即初始化 data directory)
 参考: https://dev.mysql.com/doc/refman/8.0/en/data-directory-initialization.html

  //注: 除了使用 命令类似 `sudo bin/mysqld --initialize --user=mysql --basedir=/app/mysql/  --datadir=/mydata/data` 这样的命令
        来初始化 data 目录，也可以指定 option file 来实现初始化选项的指定.
ysg@vm01:/app/mysql$ sudo vim /etc/my.cnf

  #注: 发现设置了[client], [mysql] 中的  default-character-set 后无法在 mysql 客户端工具中键入中文字符,所以这里将其注释掉
	[client]  # 注: [client] group 是 所有的 mysql client 工具都会读取的配置文件
	#loose-default-character-set = utf8mb4   # 加 loose- 前缀是为解决 [mysqlbinlog] group 不识别该 选项的 问题

	[mysql]
	#default-character-set = utf8mb4

	[mysqlbinlog]
	set_charset=utf8mb4

	[mysqld]
	# 设置 mysql 字符集为 utf8mb4
	character-set-client-handshake = FALSE  # 忽略 client 端的 character set 设置
	character-set-server = utf8mb4    # 设置了 character-set-server 的 同时也应该设置 collation-server
	collation-server = utf8mb4_unicode_ci   #注: mysql8 中,如不指定 collation-server,则其采用默认值为 utf8mb4_0900_ai_ci

	basedir=/app/mysql
	datadir=/mydata/data
	port=3306
	server_id=133
	socket=/tmp/mysql.sock

	skip-name-resolve=ON




ysg@vm01:/app/mysql$ sudo bin/mysqld --defaults-file=/etc/my.cnf --initialize --user=mysql  #注意记录下该命令生成的临时密码
	2021-02-07T16:06:40.883195Z 0 [System] [MY-013169] [Server] /app/mysql-8.0.23-linux-glibc2.12-x86_64/bin/mysqld (mysqld 8.0.23) initializing of server in progress as process 3005
	2021-02-07T16:06:40.925790Z 1 [System] [MY-013576] [InnoDB] InnoDB initialization has started.
	2021-02-07T16:06:43.061839Z 1 [System] [MY-013577] [InnoDB] InnoDB initialization has ended.
	2021-02-07T16:06:44.971051Z 6 [Note] [MY-010454] [Server] A temporary password is generated for root@localhost: Ts-#GoX+=1Jc   #<<<<<<<记下临时密码




// 设置开机自启
ysg@vm01:/app/mysql$ sudo cp /app/mysql/support-files/mysql.server  /etc/init.d/mysqld
ysg@vm01:/app/mysql$ sudo chmod a+x /etc/init.d/mysqld

ysg@vm01:/app/mysql$ sudo vim /etc/init.d/mysqld

    basedir=/app/mysql
    datadir=/mydata/data


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
	Starting mysqld (via systemctl): mysqld.service.


ysg@vm01:~$ systemctl status mysqld  #使用命令 `systemctl status mysqld` 查看 mysqld 服务状态
	● mysqld.service - LSB: start and stop MySQL
			 Loaded: loaded (/etc/init.d/mysqld; generated)
			 Active: active (running) since Mon 2021-02-08 00:09:48 CST; 20s ago
				 Docs: man:systemd-sysv-generator(8)
			Process: 3204 ExecStart=/etc/init.d/mysqld start (code=exited, status=0/SUCCESS)
				Tasks: 39 (limit: 1041)
			 Memory: 359.1M
			 CGroup: /system.slice/mysqld.service
							 ├─3226 /bin/sh /app/mysql/bin/mysqld_safe --datadir=/mydata/data --pid-file=/mydata/data/vm01.pid
							 └─3427 /app/mysql/bin/mysqld --basedir=/app/mysql --datadir=/mydata/data --plugin-dir=/app/mysql/lib/plugin --user=mysql --log-error=vm01.err --pid-file=/mydata/data/vm01.pid --socket=/tmp/mysql.sock --port=3306

	Feb 08 00:09:46 vm01 systemd[1]: Starting LSB: start and stop MySQL...
	Feb 08 00:09:46 vm01 mysqld[3204]: Starting MySQL
	Feb 08 00:09:46 vm01 mysqld[3204]: .
	Feb 08 00:09:46 vm01 mysqld[3226]: Logging to '/mydata/data/vm01.err'.
	Feb 08 00:09:48 vm01 mysqld[3204]: . *
	Feb 08 00:09:48 vm01 systemd[1]: Started LSB: start and stop MySQL.



ysg@vm01:~$ systemctl cat mysqld.service  #查看一下自动生成的 mysqld.service 的内容
	# /run/systemd/generator.late/mysqld.service
	# Automatically generated by systemd-sysv-generator

	[Unit]
	Documentation=man:systemd-sysv-generator(8)
	SourcePath=/etc/init.d/mysqld
	Description=LSB: start and stop MySQL
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



ysg@vm01:~$ sudo ss -anptu | grep 3306
	tcp    LISTEN  0       70                       *:33060                 *:*      users:(("mysqld",pid=5711,fd=31))
	tcp    LISTEN  0       151                      *:3306                  *:*      users:(("mysqld",pid=5711,fd=33))


// 安全初始化设置
ysg@vm01:/app/mysql$ sudo ./bin/mysql_secure_installation --basedir=/app/mysql/
	mysql_secure_installation: [Warning] unknown variable 'loose-default-character-set=utf8mb4'.
	mysql_secure_installation: [ERROR] unknown variable 'default-character-set=utf8mb4'.

	Securing the MySQL server deployment.

	Enter password for user root:  <--- 此处键入之前步骤中记录下的临时密码, 如此例中为 Ts-#GoX+=1Jc

	The existing password for the user account root has expired. Please set a new password.

	New password:  <----键入新密码

	Re-enter new password: <----再次键入一遍新密码

	VALIDATE PASSWORD COMPONENT can be used to test passwords
	and improve security. It checks the strength of password
	and allows the users to set only those passwords which are
	secure enough. Would you like to setup VALIDATE PASSWORD component?

	Press y|Y for Yes, any other key for No: n <----直接键入n, 即回答 no
	Using existing password for root.
	Change the password for root ? ((Press y|Y for Yes, any other key for No) : n <----直接键入n, 即回答 no




	Remove anonymous users? (Press y|Y for Yes, any other key for No) : y  <--- 删除匿名账号
	Success.

	Disallow root login remotely? (Press y|Y for Yes, any other key for No) : y <----禁止 root 远程登录
	Success.

	Remove test database and access to it? (Press y|Y for Yes, any other key for No) : y <---删除 test 示例数据库
	 - Dropping test database...
	Success.

	Reload privilege tables now? (Press y|Y for Yes, any other key for No) : y  <----重新加载授权表
	Success.

	All done!





ysg@vm01:~$ mysql -u root -p
	Enter password:
	Welcome to the MySQL monitor.  Commands end with ; or \g.
	Your MySQL connection id is 11
	Server version: 8.0.23 MySQL Community Server - GPL

	Copyright (c) 2000, 2021, Oracle and/or its affiliates.

	Oracle is a registered trademark of Oracle Corporation and/or its
	affiliates. Other names may be trademarks of their respective
	owners.

	Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

	mysql> status
	--------------
	mysql  Ver 8.0.23 for Linux on x86_64 (MySQL Community Server - GPL)

	Connection id:          11
	Current database:
	Current user:           root@localhost
	SSL:                    Not in use
	Current pager:          stdout
	Using outfile:          ''
	Using delimiter:        ;
	Server version:         8.0.23 MySQL Community Server - GPL
	Protocol version:       10
	Connection:             Localhost via UNIX socket
	Server characterset:    utf8mb4
	Db     characterset:    utf8mb4
	Client characterset:    utf8mb4
	Conn.  characterset:    utf8mb4
	UNIX socket:            /tmp/mysql.sock
	Binary data as:         Hexadecimal
	Uptime:                 15 min 19 sec

	Threads: 2  Questions: 13  Slow queries: 0  Opens: 133  Flush tables: 3  Open tables: 49  Queries per second avg: 0.014
	--------------

	mysql> SELECT User, Host, plugin FROM mysql.user;
	+------------------+-----------+-----------------------+
	| User             | Host      | plugin                |
	+------------------+-----------+-----------------------+
	| mysql.infoschema | localhost | caching_sha2_password |
	| mysql.session    | localhost | caching_sha2_password |
	| mysql.sys        | localhost | caching_sha2_password |
	| root             | localhost | caching_sha2_password |
	+------------------+-----------+-----------------------+
	4 rows in set (0.11 sec)

	mysql> SHOW VARIABLES LIKE 'character%';
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
	| character_sets_dir       | /app/mysql-8.0.23-linux-glibc2.12-x86_64/share/charsets/ |
	+--------------------------+----------------------------------------------------------+
	8 rows in set (0.03 sec)


	mysql> SHOW VARIABLES LIKE 'collation%';
	+----------------------+--------------------+
	| Variable_name        | Value              |
	+----------------------+--------------------+
	| collation_connection | utf8mb4_unicode_ci | <--注: 如果不在 option file 中做 utf8mb4_unicode_ci 的相应配置，则 mysql8 默认采用 utf8mb4_0900_ai_ci
	| collation_database   | utf8mb4_unicode_ci |
	| collation_server     | utf8mb4_unicode_ci |
	+----------------------+--------------------+
	3 rows in set (0.00 sec)


	mysql> quit
	Bye












