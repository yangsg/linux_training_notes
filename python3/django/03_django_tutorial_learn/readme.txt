


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


---------------------------------------------------------------------------------------------------



















