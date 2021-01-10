



mariadb 下载页面:
  https://downloads.mariadb.org/


从源码编译 mariadb:
  https://mariadb.com/kb/en/compiling-mariadb-from-source/


在 ubuntu 上构建 mariadb:
  https://mariadb.com/kb/en/building-mariadb-on-ubuntu/

添加 mariadb 仓库
  https://downloads.mariadb.org/mariadb/repositories/#mirror=escience


```bash

ysg@vm01:~$ sudo apt-get update

ysg@vm01:~$ sudo apt-get install software-properties-common devscripts equivs -y


ysg@vm01:~$ dpkg -l software-properties-common devscripts equivs -y
  dpkg-query: no packages found matching -y
  Desired=Unknown/Install/Remove/Purge/Hold
  | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
  |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad)
  ||/ Name                       Version       Architecture Description
  +++-==========================-=============-============-===============================================================
  ii  devscripts                 2.20.2ubuntu2 amd64        scripts to make the life of a Debian Package maintainer easier
  ii  equivs                     2.2.0         all          Circumvent Debian package dependencies
  ii  software-properties-common 0.98.9.3      all          manage the repositories that you install software from (common)



```

#### 安装构建所需依赖:
```bash

# 导入认证 key
ysg@vm01:~$ sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'

# 添加仓库(此处使用的是创建 MariaDB-Server-10.5.list 仓库配置文件的方式)
ysg@vm01:~$ sudo vim  /etc/apt/sources.list.d/MariaDB-Server-10.5.list

  # MariaDB 10.5 repository list - created 2021-01-09 13:47 UTC
  # http://downloads.mariadb.org/mariadb/repositories/
  deb [arch=amd64] https://mirrors.nju.edu.cn/mariadb/repo/10.5/ubuntu focal main
  deb-src https://mirrors.nju.edu.cn/mariadb/repo/10.5/ubuntu focal main



ysg@vm01:~$ sudo apt-get update

ysg@vm01:~$ sudo apt-get build-dep mariadb-10.5 -y

```


```bash

ysg@vm01:~$ sudo mkdir /app


ysg@vm01:~$ cd download/

ysg@vm01:~/download$ ls
mariadb-10.5.8-linux-systemd-x86_64.tar.gz


ysg@vm01:~$ which gunzip
/usr/bin/gunzip
ysg@vm01:~$ which tar
/usr/bin/tar


ysg@vm01:~$ sudo groupadd mysql
ysg@vm01:~$ sudo useradd -g mysql mysql

ysg@vm01:~/download$ sudo tar -C /app -xvf mariadb-10.5.8-linux-systemd-x86_64.tar.gz
ysg@vm01:~/download$ cd /app/
ysg@vm01:/app$ ls
mariadb-10.5.8-linux-systemd-x86_64

ysg@vm01:/app$ sudo ln -s /app/mariadb-10.5.8-linux-systemd-x86_64 mysql
ysg@vm01:/app$ cd mysql

ysg@vm01:/app/mysql$ sudo chown -R mysql .
ysg@vm01:/app/mysql$ sudo chgrp -R mysql .


ysg@vm01:/app/mysql$ sudo scripts/mysql_install_db --user=mysql
  Installing MariaDB/MySQL system tables in './data' ...
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
  cd '.' ; ./bin/mysqld_safe --datadir='./data'

  You can test the MariaDB daemon with mysql-test-run.pl
  cd './mysql-test' ; perl mysql-test-run.pl

  Please report any problems at https://mariadb.org/jira

  The latest information about MariaDB is available at https://mariadb.org/.
  You can find additional information about the MySQL part at:
  https://dev.mysql.com
  Consider joining MariaDB's strong and vibrant community:
  https://mariadb.org/get-involved/




ysg@vm01:/app/mysql$ sudo chown -R root .
ysg@vm01:/app/mysql$ sudo chown -R mysql data

ysg@vm01:/app/mysql$ bin/mysqld_safe --user=mysql &
  [1] 22264
  ysg@vm01:/app/mysql$ 210109 16:10:44 mysqld_safe Logging to '/usr/local/mysql/data/vm01.err'.
  210109 16:10:44 mysqld_safe Starting mariadbd daemon with databases from /usr/local/mysql/data




ysg@vm01:/app/mysql$ sudo bin/mysql_secure_installation --basedir=/app/mysql/
  [sudo] password for ysg:
  print: /app/mysql//bin/my_print_defaults

  NOTE: RUNNING ALL PARTS OF THIS SCRIPT IS RECOMMENDED FOR ALL MariaDB
        SERVERS IN PRODUCTION USE!  PLEASE READ EACH STEP CAREFULLY!

  In order to log into MariaDB to secure it, we'll need the current
  password for the root user. If you've just installed MariaDB, and
  haven't set the root password yet, you should just press enter here.

  Enter current password for root (enter for none):
  /app/mysql//bin/mysql: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory
  OK, successfully used password, moving on...

  Setting the root password or using the unix_socket ensures that nobody
  can log into the MariaDB root user without the proper authorisation.

  Enable unix_socket authentication? [Y/n] n
   ... skipping.

  Set root password? [Y/n] y
  New password:
  Re-enter new password:
  /app/mysql//bin/mysql: error while loading shared libraries: libncurses.so.5: cannot open shared object file: No such file or directory
  Password update failed!
  Cleaning up...




ysg@vm01:/app/mysql$ sudo apt install libncurses5










```







```



































