


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

    ------------
       关于在 Django 中使用 pymysql 的问题:
           虽然也许可以在 Django 中使用 pymysql, 但 极度不推荐 这么做, 而还是应该使用 Django 官网推荐的方式.
           因为 通常 官网推荐的方式 如果出现 兼容等相关的 bug 问题, 一般官方都会 努力去做 bug 修复,
           而官方没有推荐或说明的, 则官方也就 不会 给出 bug 修复或改进的承诺.

          https://stackoverflow.com/questions/34777755/how-to-config-django-using-pymysql-as-driver
          https://github.com/PyMySQL/PyMySQL/issues/790
          https://stackoverflow.com/questions/43102442/whats-the-difference-between-mysqldb-mysqlclient-and-mysql-connector-python

          You can import pymsql so it presents as MySQLdb. You'll need to do this before any django code is run,
          so put this in your manage.py file

              import pymysql
              pymysql.install_as_MySQLdb()
    ------------

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



// 启动 Django 自带的 server, 该 自带的 server 仅用于 开发环境(development) 而非 生产环境(production)
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

                  # Database
                  # https://docs.djangoproject.com/en/2.2/ref/settings/#databases

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
                          'OPTIONS': {
                              # https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-OPTIONS
                              # https://docs.djangoproject.com/en/2.2/ref/databases/#mysql-notes
                              # https://docs.djangoproject.com/en/2.2/ref/databases/#connecting-to-the-database
                              # https://mysqlclient.readthedocs.io/user_guide.html#functions-and-attributes
                              'use_unicode': True,
                              'charset': 'utf8mb4',
                          }
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

--------------------------------------------------
Creating models

https://docs.djangoproject.com/en/2.2/intro/tutorial02/#creating-models


创建 2 个 models:
      Question 和 Choice, 且每个 Choice 都与 一个 Question 关联:

(tutorial-venv) [root@python3lang mysite]# vim polls/models.py
(tutorial-venv) [root@python3lang mysite]# cat polls/models.py

      from django.db import models

      class Question(models.Model):
          question_text = models.CharField(max_length=200)
          pub_date = models.DateTimeField('date published')


      class Choice(models.Model):
          question = models.ForeignKey(Question, on_delete=models.CASCADE)
          choice_text = models.CharField(max_length=200)
          votes = models.IntegerField(default=0)

--------------------------------------------------
Activating models

https://docs.djangoproject.com/en/2.2/intro/tutorial02/#activating-models


Philosophy: (Django 中 apps 的可插拔的 设计理念)
  Django apps are “pluggable”: You can use an app in multiple projects,
  and you can distribute apps, because they don’t have to be tied to a given Django installation.

// 查看 polls/apps.py 包含 polls app 的 configuration class 'PollsConfig' 的定义
(tutorial-venv) [root@python3lang mysite]# grep 'PollsConfig'  polls/apps.py
      class PollsConfig(AppConfig):

// 在 mysite/settings.py 的 INSTALLED_APPS 添加 polls app 的 配置类的引用信息
(tutorial-venv) [root@python3lang mysite]# vim mysite/settings.py
      INSTALLED_APPS = [
          'polls.apps.PollsConfig',  #<-----

          'django.contrib.admin',
          'django.contrib.auth',
          'django.contrib.contenttypes',
          'django.contrib.sessions',
          'django.contrib.messages',
          'django.contrib.staticfiles',
      ]

// 生成 polls app 的 Migration
(tutorial-venv) [root@python3lang mysite]# python manage.py makemigrations polls
      Migrations for 'polls':
        polls/migrations/0001_initial.py
          - Create model Question
          - Create model Choice


// 查看 如上命令 生成的  的 polls app 的 Migration
(tutorial-venv) [root@python3lang mysite]# cat polls/migrations/0001_initial.py

                # Generated by Django 2.2 on 2019-08-04 05:37

                from django.db import migrations, models
                import django.db.models.deletion


                class Migration(migrations.Migration):

                    initial = True

                    dependencies = [
                    ]

                    operations = [
                        migrations.CreateModel(
                            name='Question',
                            fields=[
                                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                                ('question_text', models.CharField(max_length=200)),
                                ('pub_date', models.DateTimeField(verbose_name='date published')),
                            ],
                        ),
                        migrations.CreateModel(
                            name='Choice',
                            fields=[
                                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                                ('choice_text', models.CharField(max_length=200)),
                                ('votes', models.IntegerField(default=0)),
                                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polls.Question')),
                            ],
                        ),
                    ]



// Prints the SQL for the named migration.
//   This requires an active database connection,
//   which it will use to resolve constraint names; this means you must generate
//   the SQL against a copy of the database you wish to later apply it on.
//   见   https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-sqlmigrate
(tutorial-venv) [root@python3lang mysite]# python manage.py sqlmigrate polls 0001
          BEGIN
                  ;
                  --
                  -- Create model Question
                  --
                  CREATE TABLE `polls_question` #<------- 注意 table name 的命名方式
                          (
                                  `id`            integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                                  `question_text` varchar(200) NOT NULL                      ,
                                  `pub_date`      datetime(6) NOT NULL
                          );

                  --
                  -- Create model Choice
                  --
                  CREATE TABLE `polls_choice`
                          (
                                  `id`          integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
                                  `choice_text` varchar(200) NOT NULL                      ,
                                  `votes`       integer NOT NULL                           ,
                                  `question_id` integer NOT NULL
                          );

                  # 不同的数据库输出结果可能是不一样的(如 constraint names 的命名规则), 这也是为什么
                  # 命令 sqlmigrate 需要 连接查询 数据库的原因.
                  # By convention, Django appends "_id" to the foreign key field name. (Yes, you can override this, as well.)

                  ALTER TABLE `polls_choice` ADD CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id` FOREIGN KEY (`question_id`) REFERENCES `polls_question` (`id`);

                  COMMIT;

                // 注:
                // The sqlmigrate command doesn’t actually run the migration on your database -
                // it just prints it to the screen so that you can see what SQL Django thinks is required.
                // It’s useful for checking what Django is going to do or if
                // you have database administrators who require SQL scripts for changes.


// you can also run python manage.py check; this checks for any problems in your project without making migrations or touching the database.
// 见  https://docs.djangoproject.com/en/2.2/ref/django-admin/#check
(tutorial-venv) [root@python3lang mysite]# python manage.py check   #检查project 中的 所有 apps
(tutorial-venv) [root@python3lang mysite]# python manage.py check polls  #检查 project 中的 polls 应用
(tutorial-venv) [root@python3lang mysite]# python manage.py check admin polls  #检查 project 中的 admin 和 polls 应用

// 在 数据库中 创建 models 的数据库表
(tutorial-venv) [root@python3lang mysite]# python manage.py migrate

      Operations to perform:
        Apply all migrations: admin, auth, contenttypes, polls, sessions
      Running migrations:
        Applying polls.0001_initial... OK

mysql> show tables;
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
    | polls_choice               | <----
    | polls_question             | <----
    +----------------------------+

mysql> show create table polls_choice;

        | polls_choice | CREATE TABLE `polls_choice` (
          `id` int(11) NOT NULL AUTO_INCREMENT,
          `choice_text` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
          `votes` int(11) NOT NULL,
          `question_id` int(11) NOT NULL,
          PRIMARY KEY (`id`),
          KEY `polls_choice_question_id_c5b4b260_fk_polls_question_id` (`question_id`),
          CONSTRAINT `polls_choice_question_id_c5b4b260_fk_polls_question_id` FOREIGN KEY (`question_id`) REFERENCES `polls_question` (`id`)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci |

mysql> show create table polls_question\G
          *************************** 1. row ***************************
                 Table: polls_question
          Create Table: CREATE TABLE `polls_question` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `question_text` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
            `pub_date` datetime(6) NOT NULL,
            PRIMARY KEY (`id`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci



// The migrate command takes all the migrations that haven’t been applied
// (Django tracks which ones are applied using a special table in your database
// called django_migrations) and runs them against your database - essentially,
//  synchronizing the changes you made to your models with the schema in the database.

mysql> select * from  django_migrations;   #Django 通过 表 django_migrations 来跟踪 被 applied 过的 migrations
      +----+--------------+------------------------------------------+----------------------------+
      | id | app          | name                                     | applied                    |
      +----+--------------+------------------------------------------+----------------------------+
      |  1 | contenttypes | 0001_initial                             | 2019-08-04 03:09:27.878283 |
      |  2 | auth         | 0001_initial                             | 2019-08-04 03:09:28.006904 |
      |  3 | admin        | 0001_initial                             | 2019-08-04 03:09:28.182461 |
      |  4 | admin        | 0002_logentry_remove_auto_add            | 2019-08-04 03:09:28.215400 |
      |  5 | admin        | 0003_logentry_add_action_flag_choices    | 2019-08-04 03:09:28.228290 |
      |  6 | contenttypes | 0002_remove_content_type_name            | 2019-08-04 03:09:28.281312 |
      |  7 | auth         | 0002_alter_permission_name_max_length    | 2019-08-04 03:09:28.297584 |
      |  8 | auth         | 0003_alter_user_email_max_length         | 2019-08-04 03:09:28.318129 |
      |  9 | auth         | 0004_alter_user_username_opts            | 2019-08-04 03:09:28.328763 |
      | 10 | auth         | 0005_alter_user_last_login_null          | 2019-08-04 03:09:28.348975 |
      | 11 | auth         | 0006_require_contenttypes_0002           | 2019-08-04 03:09:28.351680 |
      | 12 | auth         | 0007_alter_validators_add_error_messages | 2019-08-04 03:09:28.360939 |
      | 13 | auth         | 0008_alter_user_username_max_length      | 2019-08-04 03:09:28.381292 |
      | 14 | auth         | 0009_alter_user_last_name_max_length     | 2019-08-04 03:09:28.398973 |
      | 15 | auth         | 0010_alter_group_name_max_length         | 2019-08-04 03:09:28.412058 |
      | 16 | auth         | 0011_update_proxy_permissions            | 2019-08-04 03:09:28.425350 |
      | 17 | sessions     | 0001_initial                             | 2019-08-04 03:09:28.436590 |
      | 18 | polls        | 0001_initial                             | 2019-08-04 06:31:49.328115 | <------------
      +----+--------------+------------------------------------------+----------------------------+

          // Migrations are very powerful and let you change your models over time,
          // as you develop your project, without the need to delete your database
          // or tables and make new ones - it specializes in upgrading your database live,
          // without losing data. We’ll cover them in more depth in a later part
          // of the tutorial, but for now, remember the three-step guide to making model changes:

            - Change your models (in models.py).
            - Run python manage.py makemigrations to create migrations for those changes
            - Run python manage.py migrate to apply those changes to the database.

        // The reason that there are separate commands to make and apply migrations
        // is because you’ll commit migrations to your version control system and
        // ship them with your app; they not only make your development easier,
        // they’re also usable by other developers and in production.

    更多 manage.py 相关的信息见  https://docs.djangoproject.com/en/2.2/ref/django-admin/


--------------------------------------------------
Playing with the API

      https://docs.djangoproject.com/en/2.2/intro/tutorial02/#playing-with-the-api


(tutorial-venv) [root@python3lang mysite]# python manage.py shell
Python 3.6.8 (default, Jul 24 2019, 13:57:26)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> import os
>>> print(os.environ['DJANGO_SETTINGS_MODULE'])
mysite.settings  <----- 观察

    如上命令中 manage.py 设置了环境变量 DJANGO_SETTINGS_MODULE, which gives Django the Python import path to your mysite/settings.py file.

    见:
      https://github.com/yangsg/linux_training_notes/blob/master/python3/django/03_django_tutorial_learn/django-2.2-wksp01/mysite/polls/my_learn_demo01.py

            >>> from polls.models import Choice, Question     # Import the model classes we just wrote.

            # No questions are in the system yet.
            >>> Question.objects.all()
            <QuerySet []>

            # Create a new Question.
            # Support for time zones is enabled in the default settings file, so
            # Django expects a datetime with tzinfo for pub_date. Use timezone.now()
            # instead of datetime.datetime.now() and it will do the right thing.
            >>> from django.utils import timezone
            >>> q = Question(question_text="What's new?", pub_date=timezone.now())   #<--- 注:这里使用的是 timezone.now(),因为启用了时区支持

            # Save the object into the database. You have to call save() explicitly.
            >>> q.save()

            # Now it has an ID.
            >>> q.id
            1

            # Access model field values via Python attributes.
            >>> q.question_text
            "What's new?"
            >>> q.pub_date
            datetime.datetime(2019, 8, 4, 7, 22, 19, 276409, tzinfo=<UTC>)

            # Change values by changing the attributes, then calling save().
            >>> q.question_text = "What's up?"
            >>> q.save()

            # objects.all() displays all the questions in the database.
            >>> Question.objects.all()
            <QuerySet [<Question: Question object (1)>]>




// 为 models 添加 __str__ 方法:
//   It’s important to add __str__() methods to your models,
//   not only for your own convenience when dealing with the interactive prompt,
//   but also because objects’ representations are used throughout Django’s automatically-generated admin.
// https://github.com/yangsg/linux_training_notes/blob/master/python3/django/03_django_tutorial_learn/django-2.2-wksp01/mysite/polls/models.py

(tutorial-venv) [root@python3lang mysite]# vim polls/models.py

        from django.db import models

        class Question(models.Model):
            # ...
            def __str__(self):
                return self.question_text

        class Choice(models.Model):
            # ...
            def __str__(self):
                return self.choice_text




// 添加 一个 仅用于 演示用的  was_published_recently 方法:
//    Note these are normal Python methods. Let’s add a custom method, just for demonstration:
// https://github.com/yangsg/linux_training_notes/blob/master/python3/django/03_django_tutorial_learn/django-2.2-wksp01/mysite/polls/models.py
(tutorial-venv) [root@python3lang mysite]# vim polls/models.py

          import datetime

          from django.db import models
          from django.utils import timezone


          class Question(models.Model):
              # ...
              def was_published_recently(self):
                  return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

        // 注:
        // Note the addition of import datetime and from django.utils import timezone,
        // to reference Python’s standard datetime module and Django’s time-zone-related
        // utilities in django.utils.timezone, respectively. If you aren’t familiar with
        // time zone handling in Python, you can learn more in the time zone support docs.



(tutorial-venv) [root@python3lang mysite]# python manage.py shell
Python 3.6.8 (default, Jul 24 2019, 13:57:26)
[GCC 4.8.5 20150623 (Red Hat 4.8.5-36)] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)

          见:
          https://github.com/yangsg/linux_training_notes/blob/master/python3/django/03_django_tutorial_learn/django-2.2-wksp01/mysite/polls/my_learn_demo02.py

                >>> from polls.models import Choice, Question

                # Make sure our __str__() addition worked.
                >>> Question.objects.all()
                <QuerySet [<Question: What's up?>]>

                # Django provides a rich database lookup API that's entirely driven by
                # keyword arguments.
                >>> Question.objects.filter(id=1)
                <QuerySet [<Question: What's up?>]>
                >>> Question.objects.filter(question_text__startswith='What')
                <QuerySet [<Question: What's up?>]>

                # Get the question that was published this year.
                >>> from django.utils import timezone
                >>> current_year = timezone.now().year
                >>> Question.objects.get(pub_date__year=current_year)
                <Question: What's up?>

                # Request an ID that doesn't exist, this will raise an exception.
                >>> Question.objects.get(id=2)
                Traceback (most recent call last):
                  File "<console>", line 1, in <module>
                  File "/root/tutorial-venv/lib/python3.6/site-packages/django/db/models/manager.py", line 82, in manager_method
                    return getattr(self.get_queryset(), name)(*args, **kwargs)
                  File "/root/tutorial-venv/lib/python3.6/site-packages/django/db/models/query.py", line 408, in get
                    self.model._meta.object_name
                polls.models.Question.DoesNotExist: Question matching query does not exist.

                # Lookup by a primary key is the most common case, so Django provides a
                # shortcut for primary-key exact lookups.
                # The following is identical to Question.objects.get(id=1).
                >>> Question.objects.get(pk=1)
                <Question: What's up?>

                # Make sure our custom method worked.
                >>> q = Question.objects.get(pk=1)
                >>> q.was_published_recently()
                True

                # Give the Question a couple of Choices. The create call constructs a new
                # Choice object, does the INSERT statement, adds the choice to the set
                # of available choices and returns the new Choice object. Django creates
                # a set to hold the "other side" of a ForeignKey relation
                # (e.g. a question's choice) which can be accessed via the API.
                >>> q = Question.objects.get(pk=1)

                # Display any choices from the related object set -- none so far.
                >>> q.choice_set.all()
                <QuerySet []>

                # Create three choices.
                >>> q.choice_set.create(choice_text='Not much', votes=0)
                <Choice: Not much>
                >>> q.choice_set.create(choice_text='The sky', votes=0)
                <Choice: The sky>
                >>> c = q.choice_set.create(choice_text='Just hacking again', votes=0)

                # Choice objects have API access to their related Question objects.
                >>> c.question
                <Question: What's up?>

                # And vice versa: Question objects get access to Choice objects.
                >>> q.choice_set.all()
                <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

                # The API automatically follows relationships as far as you need.
                # Use double underscores to separate relationships.
                # This works as many levels deep as you want; there's no limit.
                # Find all Choices for any question whose pub_date is in this year
                # (reusing the 'current_year' variable we created above).
                >>> q.choice_set.count()
                3

                # The API automatically follows relationships as far as you need.
                # Use double underscores to separate relationships.
                # This works as many levels deep as you want; there's no limit.
                # Find all Choices for any question whose pub_date is in this year
                # (reusing the 'current_year' variable we created above).
                >>> Choice.objects.filter(question__pub_date__year=current_year)
                <QuerySet [<Choice: Not much>, <Choice: The sky>, <Choice: Just hacking again>]>

                # Let's delete one of the choices. Use delete() for that.
                >>> c = q.choice_set.filter(choice_text__startswith='Just hacking')
                >>> c.delete()
                (1, {'polls.Choice': 1})


              更多 model 的关联对象 信息见:
              For more information on model relations, see Accessing related objects.
                  https://docs.djangoproject.com/en/2.2/ref/models/relations/

              更多 通过 API 使用 双下划线 执行 字段查找 的 信息见:
              For more on how to use double underscores to perform field lookups via the API, see Field lookups.
                    https://docs.djangoproject.com/en/2.2/topics/db/queries/#field-lookups-intro

              更多 database API 相关信息见:
              For full details on the database API, see our Database API reference.
                  https://docs.djangoproject.com/en/2.2/topics/db/queries/





--------------------------------------------------
Introducing the Django Admin

    https://docs.djangoproject.com/en/2.2/intro/tutorial02/#introducing-the-django-admin


                    Philosophy

                    Generating admin sites for your staff or clients to add, change, and delete content
                    is tedious work that doesn’t require much creativity. For that reason,
                    Django entirely automates creation of admin interfaces for models.

                    Django was written in a newsroom environment, with a very clear
                    separation between “content publishers” and the “public” site.
                    Site managers use the system to add news stories, events, sports scores, etc.,
                    and that content is displayed on the public site. Django solves
                    the problem of creating a unified interface for site administrators to edit content.

                    The admin isn’t intended to be used by site visitors. It’s for site managers.


// 创建一个管理用户( Creating an admin user )
(tutorial-venv) [root@python3lang mysite]# python manage.py createsuperuser
          Username (leave blank to use 'root'): admin  <======= 输入用户名
          Email address: admin@example.com  <======= 输入 email 地址
          Password:     <====== 输入密码
          Password (again):  <======== 重新输入密码
          Superuser created successfully.

                '''
                mysql> select id, username, email from auth_user;
                +----+----------+-------------------+
                | id | username | email             |
                +----+----------+-------------------+
                |  1 | admin    | admin@example.com |
                +----+----------+-------------------+
                '''

// Start the development server
//   The Django admin site is activated by default. Let’s start the development server and explore it.
(tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000

    浏览器访问:  http://192.168.175.20:8000/admin/
          则 打开 Django administration 的 登录界面



--------------------------------------------------
Enter the admin site

    https://docs.djangoproject.com/en/2.2/intro/tutorial02/#enter-the-admin-site

    在 Django admin index page 可以看到  groups 和 users,
    它们是由 Django 自带的 django.contrib.auth 应用提供的


--------------------------------------------------
Make the poll app modifiable in the admin

    https://docs.djangoproject.com/en/2.2/intro/tutorial02/#make-the-poll-app-modifiable-in-the-admin
    https://docs.djangoproject.com/en/2.2/intro/tutorial02/#explore-the-free-admin-functionality

But where’s our poll app? It’s not displayed on the admin index page.

// 在 Django administration 网页 为  'Question' model 提供 管理接口(即管理 'Question' model 用的增删改查的 html 控件)
// Just one thing to do: we need to tell the admin that Question objects have an admin interface.
// To do this, open the polls/admin.py file, and edit it to look like this:
(tutorial-venv) [root@python3lang mysite]# vim polls/admin.py

          from django.contrib import admin

          from .models import Question

          admin.site.register(Question)







---------------------------------------------------------------------------------------------------
Writing your first Django app, part 3

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/



A view is a “type” of Web page in your Django application that generally serves a specific function and has a specific template.

In our poll application, we’ll have the following four views:

在 poll application 示例中, 包含 如下 4 个 views:
    1) Question “index” page    – displays the latest few questions.
    2) Question “detail” page   – displays a question text, with no results but with a form to vote.
    3) Question “results” page  – displays results for a particular question.
    4) Vote action              – handles voting for a particular choice in a particular question.

  In Django, web pages and other content are delivered by views. Each view is represented
  by a simple Python function (or method, in the case of class-based views).
  Django will choose a view by examining the URL that’s requested
  (to be precise, the part of the URL after the domain name).

  A URL pattern is simply the general form of a URL - for example: /newsarchive/<year>/<month>/.

  To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

  更多关于 URLconf 的信息见:
        https://docs.djangoproject.com/en/2.2/topics/http/urls/



--------------------------------------------------
Writing more views

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#writing-more-views

(tutorial-venv) [root@python3lang mysite]# vim polls/views.py

        def detail(request, question_id):
            return HttpResponse("You're looking at question %s." % question_id)

        def results(request, question_id):
            response = "You're looking at the results of question %s."
            return HttpResponse(response % question_id)

        def vote(request, question_id):
            return HttpResponse("You're voting on question %s." % question_id)


// Wire these new views into the polls.urls module by adding the following path() calls:
(tutorial-venv) [root@python3lang mysite]# vim polls/urls.py

          from django.urls import path

          from . import views

          urlpatterns = [
              # ex: /polls/
              path('', views.index, name='index'),
              # ex: /polls/5/
              path('<int:question_id>/', views.detail, name='detail'),
              # ex: /polls/5/results/
              path('<int:question_id>/results/', views.results, name='results'),
              # ex: /polls/5/vote/
              path('<int:question_id>/vote/', views.vote, name='vote'),
          ]



    重启 server 并 用浏览器访问:
        http://192.168.175.20:8000/polls/34/
        http://192.168.175.20:8000/polls/34/results/
        http://192.168.175.20:8000/polls/34/vote/

    '''
     url 匹配 处理流程:
         When somebody requests a page from your website – say,
         “/polls/34/”, Django will load the mysite.urls Python module
         because it’s pointed to by the ROOT_URLCONF setting.
         It finds the variable named urlpatterns and traverses the patterns
         in order. After finding the match at 'polls/', it strips off
         the matching text ("polls/") and sends the remaining
         text – "34/" – to the ‘polls.urls’ URLconf for further processing.
         There it matches '<int:question_id>/', resulting
         in a call to the detail() view like so:

         detail(request=<HttpRequest object>, question_id=34)

         The question_id=34 part comes from <int:question_id>.
         Using angle brackets “captures” part of the URL and sends it as
         a keyword argument to the view function. The :question_id> part
         of the string defines the name that will be used to identify the matched pattern,
         and the <int: part is a converter that determines what patterns
         should match this part of the URL path.
    '''



--------------------------------------------------
Write views that actually do something

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#write-views-that-actually-do-something

First, create a directory called templates in your polls directory.
Django will look for templates in there.


// 创建 polls/templates 目录
(tutorial-venv) [root@python3lang mysite]# mkdir polls/templates


// 观察一下 mysite/settings.py 中 的 TEMPLATES 配置
(tutorial-venv) [root@python3lang mysite]# less mysite/settings.py

          TEMPLATES = [
              {
                  'BACKEND': 'django.template.backends.django.DjangoTemplates',
                  'DIRS': [],
                  'APP_DIRS': True,
                  'OPTIONS': {
                      'context_processors': [
                          'django.template.context_processors.debug',
                          'django.template.context_processors.request',
                          'django.contrib.auth.context_processors.auth',
                          'django.contrib.messages.context_processors.messages',
                      ],
                  },
              },
          ]



(tutorial-venv) [root@python3lang mysite]# mkdir -p  polls/templates/polls
(tutorial-venv) [root@python3lang mysite]# vim polls/templates/polls/index.html

      {% if latest_question_list %}
          <ul>
          {% for question in latest_question_list %}
              <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
          {% endfor %}
          </ul>
      {% else %}
          <p>No polls are available.</p>
      {% endif %}


    Your project’s TEMPLATES setting describes how Django will load and render templates.
    The default settings file configures a DjangoTemplates backend whose APP_DIRS option
    is set to True. By convention DjangoTemplates looks for a “templates” subdirectory
    in each of the INSTALLED_APPS.

    Within the templates directory you have just created, create another
    directory called polls, and within that create a file called index.html.
    In other words, your template should be at polls/templates/polls/index.html.
    Because of how the app_directories template loader works as described above,
    you can refer to this template within Django simply as polls/index.html.


如下这段描述 解释了 为什么在 目录 polls/templates/ 下 还要创建 与 app 同名的 polls/ 目录
    Template namespacing (Template 的 名字空间)

        Now we might be able to get away with putting our templates directly
        in polls/templates (rather than creating another polls subdirectory),
        but it would actually be a bad idea. Django will choose the first
        template it finds whose name matches, and if you had a template
        with the same name in a different application, Django would be unable
        to distinguish between them. We need to be able to point Django
        at the right one, and the easiest way to ensure this is by namespacing them.
        That is, by putting those templates inside another directory
        named for the application itself.


// Now let’s update our index view in polls/views.py to use the template:
(tutorial-venv) [root@python3lang mysite]# vim polls/views.py

      from django.http import HttpResponse
      from django.template import loader

      from .models import Question


      def index(request):
          latest_question_list = Question.objects.order_by('-pub_date')[:5]
          template = loader.get_template('polls/index.html')
          context = {
              'latest_question_list': latest_question_list,
          }
          return HttpResponse(template.render(context, request))


重启 server 并使用 浏览器访问: http://192.168.175.20:8000/polls/

--------------------------------------------------
A shortcut: render()

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#a-shortcut-render


(tutorial-venv) [root@python3lang mysite]# vim polls/views.py

        from django.shortcuts import render

        from .models import Question


        def index(request):
            latest_question_list = Question.objects.order_by('-pub_date')[:5]
            context = {'latest_question_list': latest_question_list}
            return render(request, 'polls/index.html', context)



--------------------------------------------------
Raising a 404 error

      https://docs.djangoproject.com/en/2.2/intro/tutorial03/#a-shortcut-render


(tutorial-venv) [root@python3lang mysite]# vim polls/views.py

      from django.http import Http404
      from django.shortcuts import render

      from .models import Question
      # ...
      def detail(request, question_id):
          try:
              question = Question.objects.get(pk=question_id)
          except Question.DoesNotExist:
              raise Http404("Question does not exist")
          return render(request, 'polls/detail.html', {'question': question})


(tutorial-venv) [root@python3lang mysite]# vim polls/templates/polls/detail.html

      {{ question }}


    重启 server 浏览器访问
          http://192.168.175.20:8000/polls/1/
          http://192.168.175.20:8000/polls/99/   <-- 404 的情况




--------------------------------------------------
A shortcut: get_object_or_404()

      get_list_or_404()

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#a-shortcut-get-object-or-404
    https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/#django.shortcuts.get_object_or_404

(tutorial-venv) [root@python3lang mysite]# vim polls/views.py

      from django.shortcuts import get_object_or_404, render

      from .models import Question
      # ...
      def detail(request, question_id):
          question = get_object_or_404(Question, pk=question_id)
          return render(request, 'polls/detail.html', {'question': question})


        '''
        The get_object_or_404() function takes a Django model as its first argument
        and an arbitrary number of keyword arguments, which it passes to the get()
        function of the model’s manager. It raises Http404 if the object doesn’t exist.

        Django 提供 get_object_or_404() 是基于 Django 的松耦合的 设计哲学
        Philosophy

                Why do we use a helper function get_object_or_404() instead of automatically
                catching the ObjectDoesNotExist exceptions at a higher level, or having
                the model API raise Http404 instead of ObjectDoesNotExist?

                Because that would couple the model layer to the view layer.
                One of the foremost design goals of Django is to maintain loose coupling.
                Some controlled coupling is introduced in the django.shortcuts module.

        There’s also a get_list_or_404() function, which works just as get_object_or_404()
        – except using filter() instead of get(). It raises Http404 if the list is empty.
        '''

--------------------------------------------------
Use the template system

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#use-the-template-system


(tutorial-venv) [root@python3lang mysite]# vim polls/templates/polls/detail.html

            <h1>{{ question.question_text }}</h1>
            <ul>
            {% for choice in question.choice_set.all %}
                <li>{{ choice.choice_text }}</li>
            {% endfor %}
            </ul>

        <!--
        https://docs.djangoproject.com/en/2.2/intro/tutorial03/#use-the-template-system

        使用模板系统

        模板系统 采用 dot-lookup 语法访问变量属性.
            大概的查找顺序为:
                首先执行 a dictionary 查找, 如失败，则执行
                an attribute 查找, 如果失败, 则执行
                a list-index 查找

        The template system uses dot-lookup syntax to access variable attributes.
        In the example of {{ question.question_text }}, first Django does a dictionary
        lookup on the object question. Failing that, it tries an attribute
        lookup – which works, in this case. If attribute lookup had failed,
        it would’ve tried a list-index lookup.

        Method-calling happens in the {% for %} loop: question.choice_set.all is interpreted
        as the Python code question.choice_set.all(), which returns an iterable of Choice
        objects and is suitable for use in the {% for %} tag.

        更多 template 的信息见:
            https://docs.djangoproject.com/en/2.2/topics/templates/
        -->

--------------------------------------------------

Removing hardcoded URLs in templates

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#removing-hardcoded-urls-in-templates


(tutorial-venv) [root@python3lang mysite]# vim polls/templates/polls/index.html

        <!--
        Bad Practice
        <li><a href="/polls/{{ question.id }}/">{{ question.question_text }}</a></li>
        -->
        <!--
        https://docs.djangoproject.com/en/2.2/intro/tutorial03/#removing-hardcoded-urls-in-templates

        根据 Django 弱耦合 的设计哲学, 应该 使用 类似 {% url 'detail' question.id %} 的
        方式实现链接引用而不应采用硬编码的方式直接将 url 嵌入到 template 中.

        The problem with this hardcoded, tightly-coupled approach is that it becomes
        challenging to change URLs on projects with a lot of templates. However,
        since you defined the name argument in the path() functions in the polls.urls module,
        you can remove a reliance on specific URL paths defined in your url
        configurations by using the {% url %} template tag:

        <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>

        The way this works is by looking up the URL definition as specified in the polls.urls module.
        You can see exactly where the URL name of ‘detail’ is defined below:

                # the 'name' value as called by the {% url %} template tag
                path('<int:question_id>/', views.detail, name='detail'),
        -->
        <!-- 一种改良版本, 注: 这还不是 最佳实践, 最佳实践是 还应该同时采用 命令空间的 url(Namespacing URL names) -->
        <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>

--------------------------------------------------
Namespacing URL names

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#namespacing-url-names

(tutorial-venv) [root@python3lang mysite]# vim polls/urls.py

          from django.urls import path

          from . import views

          app_name = 'polls'  # 定义 app 的 名字空间(app namespace)
          urlpatterns = [
              path('', views.index, name='index'),
              path('<int:question_id>/', views.detail, name='detail'),
              path('<int:question_id>/results/', views.results, name='results'),
              path('<int:question_id>/vote/', views.vote, name='vote'),
          ]


(tutorial-venv) [root@python3lang mysite]# vim polls/templates/polls/index.html
    <!-- Best Practice -->
    <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>


----------------------------------------------------------------------------------------------------
Writing your first Django app, part 4

    https://docs.djangoproject.com/en/2.2/intro/tutorial04/#writing-your-first-django-app-part-4


(tutorial-venv) [root@python3lang mysite]# vim polls/templates/polls/detail.html


TODO
TODO
TODO
TODO
TODO
TODO
TODO
TODO


----------------------------------------------------------------------------------------------------
Writing your first Django app, part 6

    https://docs.djangoproject.com/en/2.2/intro/tutorial06/


django.contrib.staticfiles 作用:
    it collects static files from each of your applications (and any other places you specify)
    into a single location that can easily be served in production.

(tutorial-venv) [root@python3lang mysite]# mkdir polls/static

    Django 会查找 polls/static 下的 files, 方式类似于 查找 polls/templates/ 下的 templates 文件.


https://docs.djangoproject.com/en/2.2/ref/settings/#staticfiles-finders
https://docs.djangoproject.com/en/2.2/intro/tutorial06/#customize-your-app-s-look-and-feel

STATICFILES_FINDERS 的默认值为:

        [
            'django.contrib.staticfiles.finders.FileSystemFinder',
            'django.contrib.staticfiles.finders.AppDirectoriesFinder',
        ]


  Django’s STATICFILES_FINDERS setting contains a list of finders that
  know how to discover static files from various sources.
  One of the defaults is AppDirectoriesFinder which looks for a “static” subdirectory
  in each of the INSTALLED_APPS, like the one in polls we just created.
  The admin site uses the same directory structure for its static files.

  Within the static directory you have just created, create another directory called
  polls and within that create a file called style.css. In other words,
  your stylesheet should be at polls/static/polls/style.css. Because of
  how the AppDirectoriesFinder staticfile finder works, you can refer to
  this static file in Django simply as polls/style.css, similar to
  how you reference the path for templates.


(tutorial-venv) [root@python3lang mysite]# mkdir -p polls/static/polls
(tutorial-venv) [root@python3lang mysite]# vim polls/static/polls/style.css

    Static file namespacing (静态文件的 名字空间, 其作用和道理和 template file 的名字空间类似 )

      Just like templates, we might be able to get away with putting our static files directly
      in polls/static (rather than creating another polls subdirectory), but it would actually
      be a bad idea. Django will choose the first static file it finds whose name matches,
      and if you had a static file with the same name in a different application,
      Django would be unable to distinguish between them. We need to be able to point
      Django at the right one, and the easiest way to ensure this is by namespacing them.
      That is, by putting those static files inside another directory named for the application itself.


(tutorial-venv) [root@python3lang mysite]# mkdir -p polls/static/polls/images/

放置背景图片:   polls/static/polls/images/background.gif


    Warning:

        Of course the {% static %} template tag is not available for use in static files
        like your stylesheet which aren’t generated by Django. You should always use
        relative paths to link your static files between each other, because then you
        can change STATIC_URL (used by the static template tag to generate its URLs)
        without having to modify a bunch of paths in your static files as well.

https://docs.djangoproject.com/en/2.2/howto/static-files/
https://docs.djangoproject.com/en/2.2/ref/contrib/staticfiles/







---------------------------------------------------------------------------------------------------

Writing your first Django app, part 7

    https://docs.djangoproject.com/en/2.2/intro/tutorial07/






















