// 在ubuntu18.04 桌面版上安装 mariadb-server

参考：
		https://websiteforstudents.com/installing-mariadb-database-server-on-ubuntu-18-04-lts-beta-server/
		https://linuxize.com/post/how-to-install-mariadb-on-ubuntu-18-04/

yangsg@vm:~$ sudo apt install mariadb-server   #// 注：此处 mariadb-server 安装好后默认就是启动的


// 查看mariadb-server 版本的命令：
yangsg@vm:~$ dpkg -s mariadb-server   #// 或  apt policy mariadb-server  或 apt show mariadb-server

// 安全设置
yangsg@vm:~$ sudo mysql_secure_installation
配置文件位置：/etc/mysql/mariadb.conf.d/50-server.cnf

yangsg@vm:~$ sudo systemctl stop mariadb.service
yangsg@vm:~$ sudo systemctl start mariadb.service
yangsg@vm:~$ sudo systemctl enable mariadb.service

//  https://superuser.com/questions/957708/mysql-mariadb-error-1698-28000-access-denied-for-user-rootlocalhost
//  https://stackoverflow.com/questions/39281594/error-1698-28000-access-denied-for-user-rootlocalhost
//  直接使用 mysql -u root -p 会报错, 如下：
//  	>      yangsg@vm:~$ mysql -u root -p
//  	>      Enter password:
//  	>      ERROR 1698 (28000): Access denied for user 'root'@'localhost'

// 使用 sudo 命令登录是成功的:
yangsg@vm:~$ sudo mysql -u root -p

// 为了方便(即允许不加sudo也可以直接使用`mysql -u root -p`登录), 可以做如下修改：
MariaDB [mysql]> use mysql;
MariaDB [mysql]> UPDATE user SET plugin='mysql_native_password' WHERE User='root';
MariaDB [mysql]> flush privileges;
yangsg@vm:~$ sudo systemctl restart mariadb.service
现在就可以直接使用 `mysql -u root -p` 登录数据库了

// 创建其他可登录的账户：
MariaDB [(none)]> GRANT ALL ON django_db01.* TO 'django_user01'@'127.0.0.1' IDENTIFIED BY 'WWW.1.com';
MariaDB [mysql]> SELECT User, Host, plugin FROM mysql.user;;
+---------------+-----------+-----------------------+
| User          | Host      | plugin                |
+---------------+-----------+-----------------------+
| root          | localhost | mysql_native_password |
| django_user01 | 127.0.0.1 |                       |
+---------------+-----------+-----------------------+
MariaDB [mysql]> flush privileges;

//  使用其他账户登录mariadb-server
//  https://stackoverflow.com/questions/10299148/mysql-error-1045-28000-access-denied-for-user-billlocalhost-using-passw
yangsg@vm:~$ mysql -h 127.0.0.1 -u django_user01 -p





