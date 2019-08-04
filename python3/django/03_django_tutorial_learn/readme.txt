


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

mysqlclient 版本需求:  见 https://pypi.org/project/mysqlclient/
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

// 查看 django 版本
(tutorial-venv) [root@python3lang ~]# python -m django --version
    2.2

(tutorial-venv) [root@python3lang ~]# cd /root/linux_training_notes/python3/django/03_django_tutorial_learn/django-2.2-wksp01

// 创建 一个新的 Django project
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



(tutorial-venv) [root@python3lang django-2.2-wksp01]# cd mysite/
(tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000


// 在 mysql server 上创建 一个 学习用的 database
// 参考:   https://github.com/yangsg/linux_training_notes/tree/master/python3/basic02_syntax/mod_SQLAlchemy
mysql> CREATE DATABASE db_django_01 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

// 配置 Django2.2 使用 mysql 数据库, 同时顺便 也把 ALLOWED_HOSTS 配置了
(tutorial-venv) [root@python3lang mysite]# vim mysite/settings.py

                  ALLOWED_HOSTS = [
                      '192.168.175.20',
                  ]

                  # Django2.2 中使用的 sqlite3 版本与 centos7 无法兼容,
                  # 所以也不用 再继续浪费大量的时间去寻找 解决方案了(因为很可能都无法成功)
                  # 所以这里 直接 改用 mysql 数据库
                  # DATABASES = {
                  #     'default': {
                  #         'ENGINE': 'django.db.backends.sqlite3',
                  #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
                  #     }
                  # }

                  # 使用 mysql 数据库
                  DATABASES = {
                      'default': {
                          'ENGINE': 'django.db.backends.mysql',
                          'NAME': 'db_django_01',
                          'USER': 'root',
                          'PASSWORD': 'WWW.1.com',
                          'HOST': '192.168.175.100',
                          'PORT': '3306',
                      }
                  }



// 配置 本地 yum 源, 参考 https://github.com/yangsg/linux_training_notes/tree/master/local_yum_repo_server/100-localyumserver
[root@python3lang ~]# vim /etc/yum.repos.d/000-local-yum.repo
      [000-local-yum]
      name=000-local-yum
      baseurl=http://192.168.175.10/local_yum_repo_dir/
      enabled=1
      gpgcheck=0


// 安装 mysql-devel package (因为 Django 推荐使用 mysqlclient, 而 mysqlclient 又依赖于 mysql-devel)
// 见  https://pypi.org/project/mysqlclient/
[root@python3lang ~]# yum clean metadata
[root@python3lang ~]# yum -y install mysql-devel

// 安装 mysqlclient
(tutorial-venv) [root@python3lang mysite]# pip install mysqlclient
(tutorial-venv) [root@python3lang mysite]# pip show mysqlclient
      Name: mysqlclient
      Version: 1.4.2.post1
      Summary: Python interface to MySQL
      Home-page: https://github.com/PyMySQL/mysqlclient-python
      Author: Inada Naoki
      Author-email: songofacandy@gmail.com
      License: GPL
      Location: /root/tutorial-venv/lib/python3.6/site-packages
      Requires:
      Required-by:


// 启动 Django web 服务: 见 https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-runserver
(tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000


// 测试:
    浏览器访问: http://192.168.175.20:8000


---------------------------------------------------------------------------------------------------
在 project 中 创建 app

Creating the Polls app

    https://docs.djangoproject.com/en/2.2/intro/tutorial01/#creating-the-polls-app

(tutorial-venv) [root@python3lang mysite]# ls
    manage.py  mysite

(tutorial-venv) [root@python3lang mysite]# python manage.py startapp polls
(tutorial-venv) [root@python3lang mysite]# ls
    manage.py  mysite  polls

(tutorial-venv) [root@python3lang mysite]# tree polls/
      polls/
      ├── admin.py
      ├── apps.py
      ├── __init__.py
      ├── migrations
      │   └── __init__.py
      ├── models.py
      ├── tests.py
      └── views.py



(tutorial-venv) [root@python3lang mysite]# vim polls/urls.py
      from django.urls import path

      from . import views

      urlpatterns = [
          path('', views.index, name='index'),
      ]

(tutorial-venv) [root@python3lang mysite]# tree polls/
      polls/
      ├── admin.py
      ├── apps.py
      ├── __init__.py
      ├── migrations
      │   └── __init__.py
      ├── models.py
      ├── tests.py
      ├── urls.py   <------
      └── views.py


(tutorial-venv) [root@python3lang mysite]# vim mysite/urls.py
      from django.contrib import admin
      from django.urls import path

      urlpatterns = [
          path('admin/', admin.site.urls),
      ]


(tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000

浏览器访问 http://192.168.175.20:8000/polls/


---------------------------------------------------------------------------------------------------

  https://docs.djangoproject.com/en/2.2/intro/tutorial02/

为了方便, Django 默认会在 mysite/settings.py 配置文件的 INSTALLED_APPS 中包含如下 常用的 apps:

        django.contrib.admin         – The admin site. You’ll use it shortly.
        django.contrib.auth          – An authentication system.
        django.contrib.contenttypes  – A framework for content types.
        django.contrib.sessions      – A session framework.
        django.contrib.messages      – A messaging framework.
        django.contrib.staticfiles   – A framework for managing static files.

  Some of these applications make use of at least one database table,
  though, so we need to create the tables in the database beforewe can use them.
  To do that, run the following command:

// 创建数据库表:
// 命令 migrate 会查找 mysite/settings.py 中 INSTALLED_APPS 的设置并
// 根据 mysite/settings.py 中的 database 设置 创建必要的 database tables
// 和  the database migrations shipped with the app (we’ll cover those later).
(tutorial-venv) [root@python3lang mysite]# python manage.py migrate

        Operations to perform:
          Apply all migrations: admin, auth, contenttypes, sessions
        Running migrations:
          Applying contenttypes.0001_initial... OK
          Applying auth.0001_initial... OK
          Applying admin.0001_initial... OK
          Applying admin.0002_logentry_remove_auto_add... OK
          Applying admin.0003_logentry_add_action_flag_choices... OK
          Applying contenttypes.0002_remove_content_type_name... OK
          Applying auth.0002_alter_permission_name_max_length... OK
          Applying auth.0003_alter_user_email_max_length... OK
          Applying auth.0004_alter_user_username_opts... OK
          Applying auth.0005_alter_user_last_login_null... OK
          Applying auth.0006_require_contenttypes_0002... OK
          Applying auth.0007_alter_validators_add_error_messages... OK
          Applying auth.0008_alter_user_username_max_length... OK
          Applying auth.0009_alter_user_last_name_max_length... OK
          Applying auth.0010_alter_group_name_max_length... OK
          Applying auth.0011_update_proxy_permissions... OK
          Applying sessions.0001_initial... OK



mysql> use db_django_01;
mysql> show tables;      # 查看数据库中 如上命令 `python manage.py migrate` 创建的 数据表

    +----------------------------+
    | Tables_in_db_django_01     |
    +----------------------------+
    | auth_group                 |
    | auth_group_permissions     |
    | auth_permission            |
    | auth_user                  |
    | auth_user_groups           |
    | auth_user_user_permissions |
    | django_admin_log           |
    | django_content_type        |
    | django_migrations          |
    | django_session             |
    +----------------------------+

  可通过如下语句观察 表中的数据:
          select * from  auth_group;
          select * from  auth_group_permissions;
          select * from  auth_permission;
          select * from  auth_user;
          select * from  auth_user_groups;
          select * from  auth_user_user_permissions;
          select * from  django_admin_log;
          select * from  django_content_type;
          select * from  django_migrations;
          select * from  django_session;

---------------------------------------------------------------------------------------------------



















