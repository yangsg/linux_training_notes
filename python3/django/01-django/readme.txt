

https://www.djangoproject.com/

[root@python3lang ~]# mkdir workspace
[root@python3lang ~]# cd workspace/

[root@python3lang workspace]# python3 -m venv django-env
[root@python3lang workspace]# source django-env/bin/activate

#// 安装 Django  https://www.djangoproject.com/download/
#//              https://github.com/django/django.git
(django-env) [root@python3lang workspace]# pip install Django==2.2

#// https://docs.djangoproject.com/en/2.2/ref/django-admin/
(django-env) [root@python3lang workspace]# django-admin --help
(django-env) [root@python3lang workspace]# django-admin startproject web01

(django-env) [root@python3lang workspace]# tree web01/
        web01/
        ├── manage.py
        └── web01
            ├── __init__.py
            ├── settings.py
            ├── urls.py
            └── wsgi.py

(django-env) [root@python3lang workspace]# cd web01/

python manage.py runserver





















