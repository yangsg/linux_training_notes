

官网: http://www.jumpserver.org
在线体验: https://demo.jumpserver.org/auth/login/
文档: https://jumpserver.readthedocs.io/zh/master/


Jumpserver 环境要求：

硬件配置: 2个CPU核心, 4G 内存, 50G 硬盘（最低）
操作系统: Linux 发行版 x86_64
Python = 3.6.x
Mysql Server ≥ 5.6
Mariadb Server ≥ 5.5.56
Redis

----------------------------------------------------------------------------------------------------
安装 epel 源(我的试验环境已有 epel 源, 此处略过)
[root@jump_server ~]# yum -y install epel-release


安装 python3.6 解释器
[root@jump_server ~]# yum -y install wget sqlite-devel xz gcc automake zlib-devel openssl-devel git

[root@jump_server download]# tar -xvf Python-3.6.8.tgz
[root@jump_server download]# cd Python-3.6.8/
[root@jump_server Python-3.6.8]# ./configure
[root@jump_server Python-3.6.8]# make
[root@jump_server Python-3.6.8]# make install

[root@jump_server Python-3.6.8]# python3.6 -V
    Python 3.6.8


安装 mysql 服务器 (注: 此处选择 mariadb)
[root@jump_server ~]# yum -y install mariadb-server mariadb-devel mariadb
[root@jump_server ~]# rpm -q mariadb-server mariadb-devel mariadb
      mariadb-server-5.5.64-1.el7.x86_64
      mariadb-devel-5.5.64-1.el7.x86_64
      mariadb-5.5.64-1.el7.x86_64


// 将 mysql 字符集设置为 utf8mb4 (即真正意义上的 utf8)
// https://blog.csdn.net/zhnxin_163/article/details/82879586
// https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/006-mha4mysql-semi-sync-gtid-utf8mb4-rpm
[root@jump_server ~]# vim /etc/my.cnf

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


[root@jump_server ~]# systemctl start mariadb
[root@jump_server ~]# systemctl enable mariadb
      Created symlink from /etc/systemd/system/multi-user.target.wants/mariadb.service to /usr/lib/systemd/system/mariadb.service.

[root@jump_server ~]# systemctl status mariadb
    ● mariadb.service - MariaDB database server
       Loaded: loaded (/usr/lib/systemd/system/mariadb.service; enabled; vendor preset: disabled)
       Active: active (running) since Sat 2019-10-05 18:34:14 CST; 1min 8s ago
     Main PID: 15752 (mysqld_safe)
       CGroup: /system.slice/mariadb.service
               ├─15752 /bin/sh /usr/bin/mysqld_safe --basedir=/usr
               └─15950 /usr/libexec/mysqld --basedir=/usr --datadir=/var/lib/mysql --plugin-dir=/usr/lib64/mysql/plugin --log-error=/var/log/mariadb/mariadb.log --pid-file=/var/run/mariadb/...

    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: MySQL manual for more instructions.
    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: Please report any problems at http://mariadb.org/jira
    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: The latest information about MariaDB is available at http://mariadb.org/.
    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: You can find additional information about the MySQL part at:
    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: http://dev.mysql.com
    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: Consider joining MariaDB's strong and vibrant community:
    Oct 05 18:34:12 jump_server mariadb-prepare-db-dir[15666]: https://mariadb.org/get-involved/
    Oct 05 18:34:12 jump_server mysqld_safe[15752]: 191005 18:34:12 mysqld_safe Logging to '/var/log/mariadb/mariadb.log'.
    Oct 05 18:34:13 jump_server mysqld_safe[15752]: 191005 18:34:13 mysqld_safe Starting mysqld daemon with databases from /var/lib/mysql
    Oct 05 18:34:14 jump_server systemd[1]: Started MariaDB database server.


[root@jump_server ~]# mysql_secure_installation

      ......
      New password:   <=========为 root 键入新密码
      Re-enter new password:  <=========重复为 root 键入新密码
      Password updated successfully!
      ......

// 查看字符集信息
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
| collation_connection     | utf8mb4_unicode_ci         |
| collation_database       | utf8mb4_unicode_ci         |
| collation_server         | utf8mb4_unicode_ci         |
+--------------------------+----------------------------+

   变量 character_set_system : The character set used by the server for storing identifiers. The value is always utf8.



[root@jump_server ~]# yum -y install redis
[root@jump_server ~]# rpm -q redis
    redis-3.2.12-2.el7.x86_64


[root@jump_server ~]# systemctl start redis
[root@jump_server ~]# systemctl enable redis
      Created symlink from /etc/systemd/system/multi-user.target.wants/redis.service to /usr/lib/systemd/system/redis.service.

[root@jump_server ~]# systemctl status redis
    ● redis.service - Redis persistent key-value database
       Loaded: loaded (/usr/lib/systemd/system/redis.service; enabled; vendor preset: disabled)
      Drop-In: /etc/systemd/system/redis.service.d
               └─limit.conf
       Active: active (running) since Sat 2019-10-05 18:58:40 CST; 1min 6s ago
     Main PID: 34865 (redis-server)
       CGroup: /system.slice/redis.service
               └─34865 /usr/bin/redis-server 127.0.0.1:6379

    Oct 05 18:58:40 jump_server systemd[1]: Starting Redis persistent key-value database...
    Oct 05 18:58:40 jump_server systemd[1]: Started Redis persistent key-value database.



// 创建 py3 虚拟环境
[root@jump_server ~]# python3.6 -m venv /opt/py3


// 载入 py3 虚拟环境
// 注: 每次操作 jumpserver 都需要使用下面的命令载入 py3 虚拟环境
[root@jump_server ~]# source /opt/py3/bin/activate
(py3) [root@jump_server ~]#

// 获取 jumpserver 代码
(py3) [root@jump_server ~]# cd /opt
(py3) [root@jump_server opt]# git clone --depth=1 https://github.com/jumpserver/jumpserver.git


// 安装依赖
(py3) [root@jump_server opt]# cd /opt/jumpserver/requirements
(py3) [root@jump_server requirements]# ls
      alpine_requirements.txt  deb_requirements.txt  issues.txt  mac_requirements.txt  requirements.txt  rpm_requirements.txt

(py3) [root@jump_server requirements]# yum install -y $(cat rpm_requirements.txt)

// 安装 依赖的 python modules 之前先升级一下 pip 工具
(py3) [root@jump_server requirements]# pip install --upgrade pip

// 安装 依赖的 python modules
(py3) [root@jump_server requirements]# pip install -r requirements.txt


// 当如上的命令 进行到 安装 python-gssapi-0.6.4 时 出现如下错误(网络不可达):

    distutils.errors.DistutilsError: Download error for https://files.pythonhosted.org/packages/5f/bf/6aa1925384c23ffeb579e97a5569eb9abce41b6310b329352b8252cee1c3/cffi-1.12.3-cp36-cp36m-manylinux1_x86_64.whl#sha256=59b4dc008f98fc6ee2bb4fd7fc786a8d70000d058c2bbe2698275bc53a8d3fa7: [Errno 101] Network is unreachable

// 解决办法: 手动下载 python-gssapi-0.6.4.tar.gz 并在 本地执行安装
//   https://stackoverflow.com/questions/36014334/how-to-install-python-packages-from-the-tar-gz-file-without-using-pip-install
//   https://stackoverflow.com/questions/43419975/installing-downloaded-tar-gz-files-with-pip?noredirect=1
//   https://pypi.org/project/python-gssapi/
//   https://github.com/sigmaris/python-gssapi/releases
//   https://github.com/pythongssapi/python-gssapi

(py3) [root@jump_server requirements]# wget -O /root/download/python-gssapi-0.6.4.tar.gz  https://files.pythonhosted.org/packages/a4/9e/648b4e85235097edcee561c986f7075cb1606be24c514cfcdd2930e35c5e/python-gssapi-0.6.4.tar.gz
(py3) [root@jump_server requirements]# pip install /root/download/python-gssapi-0.6.4.tar.gz

// 解决了如上问题后, 重新执行 如下命令 继续安装相关  依赖的 python 模块
(py3) [root@jump_server requirements]# pip install -r requirements.txt






























