

https://pypi.org/project/SQLAlchemy/

https://docs.sqlalchemy.org/en/13/

该页面 有 一张 SQLAlchemy 的 major components 描述图
https://docs.sqlalchemy.org/en/13/intro.html#installation
https://stackoverflow.com/questions/tagged/sqlalchemy


SQLAlchemy ORM
    https://docs.sqlalchemy.org/en/13/orm/index.html

SQLAlchemy Core
    https://docs.sqlalchemy.org/en/13/core/index.html

Dialects
    https://docs.sqlalchemy.org/en/13/dialects/index.html

    mysql
      https://docs.sqlalchemy.org/en/13/dialects/mysql.html

ORM Examples
    https://docs.sqlalchemy.org/en/13/orm/examples.html

https://github.com/sqlalchemy/sqlalchemy/wiki/UsageRecipes


Glossary
    https://docs.sqlalchemy.org/en/13/glossary.html#term-dbapi


关于 session (重要)
    https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-frequently-asked-questions

---------------------------------------------------------------------------------------------------

版本支持信息:
  Changed in version 1.3: Within the Python 3 series, 3.4 is now the minimum Python 3 version supported.

[root@python3lang ~]# source tutorial-venv/bin/activate
(tutorial-venv) [root@python3lang ~]# python --version
    Python 3.6.8

(tutorial-venv) [root@python3lang ~]# pip install --upgrade pip
(tutorial-venv) [root@python3lang ~]# pip --version
    pip 19.2.1 from /root/tutorial-venv/lib/python3.6/site-packages/pip (python 3.6)

// 安装 SQLAlchemy
(tutorial-venv) [root@python3lang ~]# pip install SQLAlchemy

(tutorial-venv) [root@python3lang ~]# pip show SQLAlchemy
    Name: SQLAlchemy
    Version: 1.3.6
    Summary: Database Abstraction Library
    Home-page: http://www.sqlalchemy.org
    Author: Mike Bayer
    Author-email: mike_mp@zzzcomputing.com
    License: MIT
    Location: /root/tutorial-venv/lib/python3.6/site-packages
    Requires:
    Required-by:

检查 SQLAlchemy 版本 (通过执行 python 语句的方式)
(tutorial-venv) [root@python3lang ~]# python -c 'import sqlalchemy; print(sqlalchemy.__version__)'
      1.3.6

// 安装 PyMySQL (注: SQLAlchemy 本身是一个 ORM 框架, 其需要特定的database driver, 这好比 java中的 Hibernate 或 MyBatis 需要 jdbc driver 一样)
(tutorial-venv) [root@python3lang ~]# pip install PyMySQL
(tutorial-venv) [root@python3lang ~]# pip show PyMySQL
      Name: PyMySQL
      Version: 0.9.3
      Summary: Pure Python MySQL Driver
      Home-page: https://github.com/PyMySQL/PyMySQL/
      Author: yutaka.matsubara
      Author-email: yutaka.matsubara@gmail.com
      License: "MIT"
      Location: /root/tutorial-venv/lib/python3.6/site-packages
      Requires:
      Required-by:


---------------------------------------------------------------------------------------------------

安装 一台 mysql 服务器:
参考如下 等 笔记:
    https://github.com/yangsg/linux_training_notes/tree/master/mysql_mariadb/mysql_02_basic/replication.dir/006-mha4mysql-semi-sync-gtid-utf8mb4-rpm


[root@master ~]# rpm -q mysql-community-server
    mysql-community-server-5.7.26-1.el7.x86_64


相关主机 ip 信息:
[root@python3lang ~]# ip addr show ens33  | awk '/inet / {print $2}'
      192.168.175.20/24
[root@master ~]# ip addr show ens33  | awk '/inet / {print $2}'
      192.168.175.100/24

// 创建 user 并 授权
mysql> USE mysql
mysql> CREATE USER IF NOT EXISTS 'root'@'192.168.175.20' IDENTIFIED BY 'WWW.1.com';
mysql> GRANT ALL ON *.* TO 'root'@'192.168.175.20';

// 创建 学习用的 数据库
mysql> CREATE DATABASE db_test01 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;






















