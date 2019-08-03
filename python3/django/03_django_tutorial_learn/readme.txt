


Django documentation
    https://docs.djangoproject.com/en/2.2/


Django 与 python 版本 关系:  https://docs.djangoproject.com/en/2.2/faq/install/#faq-python-version-support

      Django version    Python versions
      1.11              2.7, 3.4, 3.5, 3.6, 3.7 (added in 1.11.17)
      2.0               3.4, 3.5, 3.6, 3.7
      2.1, 2.2          3.5, 3.6, 3.7    <------


mysql 相关:
    https://docs.djangoproject.com/en/2.2/ref/databases/#mysql-notes
    https://docs.djangoproject.com/en/2.2/ref/databases/#mysql-db-api-drivers

    python 按 'PEP 249' 实现的 MySQL DB API Drivers 有如下两个:
        1) (推荐)mysqlclient is a native driver. It’s the recommended choice.
        2) MySQL Connector/Python is a pure Python driver from Oracle that does not require
           the MySQL client library or any Python modules outside the standard library.

        These drivers are thread-safe and provide connection pooling.

    Django 通过 ORM 访问 database drivers 还需要适配器(adapter), Django 提供了一个访问 mysqlclient
    的适配器, 而  MySQL Connector/Python 有其 自己的适配器.

mysql 版本需求:
  Django supports MySQL 5.6 and higher.

  Django 期望 the database 支持 Unicode (UTF-8 encoding), 并 委托 task 时 强制 transactions 和 referential integrity.
  所以最好 使用 支持事务 和 外键引用的 InnoDB(推荐) 存储引擎(storage engine). 而不要使用 MyISAM, 因其不支持 事务 和 外键约束.

  InnoDB 存储引擎需要注意的地方:
      However, the InnoDB autoincrement counter is lost on a MySQL restart because
      it does not remember the AUTO_INCREMENT value, instead recreating it as
      “max(id)+1”. This may result in an inadvertent reuse of AutoField values.

    小心: 千万不要在事务中 混合使用 支持事务 和 不支持事务的表, 这会导致数据完整性和一致性的问题,
          因为 不支持事务的表 在 rollback 时所做的修改无法被撤销.

mysqlclient 版本需求:
  Django requires mysqlclient 1.3.13 or later.

关于 timezone 时区的支持:
    https://docs.djangoproject.com/en/2.2/ref/databases/#time-zone-definitions
    https://docs.djangoproject.com/en/2.2/topics/i18n/timezones/
    https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html


Table names:
    使用小写的 表名


---------------------------------------------------------------------------------------------------
安装Django

[root@python3lang ~]# source tutorial-venv/bin/activate
(tutorial-venv) [root@python3lang ~]# pip install --upgrade pip
(tutorial-venv) [root@python3lang ~]# pip install Django==2.2

(tutorial-venv) [root@python3lang ~]# pip show Django
      Name: Django
      Version: 2.2
      Summary: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
      Home-page: https://www.djangoproject.com/
      Author: Django Software Foundation
      Author-email: foundation@djangoproject.com
      License: BSD
      Location: /root/tutorial-venv/lib/python3.6/site-packages
      Requires: sqlparse, pytz
      Required-by:

(tutorial-venv) [root@python3lang ~]# python -m django --version
    2.2

(tutorial-venv) [root@python3lang ~]# cd /root/linux_training_notes/python3/django/03_django_tutorial_learn/django-2.2-wksp01

(tutorial-venv) [root@python3lang django-2.2-wksp01]# django-admin startproject mysite
(tutorial-venv) [root@python3lang django-2.2-wksp01]# tree
      .
      └── mysite  <----  project 的 root directory, 其名字与 Django 不相关, 可以对其 重命名(rename)
          ├── manage.py  <---- 命令行交互工具, 可通过它来与 该 Django project 以各种方式交互,  见: https://docs.djangoproject.com/en/2.2/ref/django-admin/
          └── mysite     <---- 该 project 的实际的 python package 目录, 其名字 就是在 代码中 import 时可能需要用到的 the Python package name (如 mysite.urls)
              ├── __init__.py  <--- An empty file, 用于告诉 Python 视 该目录为 a Python package.
              ├── settings.py  <--- Settings/configuration for this Django project. 见 https://docs.djangoproject.com/en/2.2/topics/settings/
              ├── urls.py      <--- The URL declarations for this Django project; 见 https://docs.djangoproject.com/en/2.2/topics/http/urls/
              └── wsgi.py      <--- An entry-point for WSGI-compatible web servers to serve your project. 见 https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/














---------------------------------------------------------------------------------------------------


















