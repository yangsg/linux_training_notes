

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

---------------------------------------------------------------------------------------------------

























