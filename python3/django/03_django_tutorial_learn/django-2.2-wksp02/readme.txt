

python3.6.8 安装
    https://github.com/yangsg/linux_training_notes/tree/master/python3/basic01_install


Django2.2 安装
    https://github.com/yangsg/linux_training_notes/tree/master/python3/django/03_django_tutorial_learn


CREATE DATABASE db_django_02 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;



(tutorial-venv) [root@python3lang mysite]# python manage.py startapp myapp

(tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000

浏览器访问: http://192.168.175.20:8000/myapp/


(tutorial-venv) [root@python3lang mysite]# mkdir -p  myapp/templates/myapp

(tutorial-venv) [root@python3lang mysite]# python manage.py makemigrations
(tutorial-venv) [root@python3lang mysite]# python manage.py sqlmigrate myapp 0001
(tutorial-venv) [root@python3lang mysite]# python manage.py check myapp
(tutorial-venv) [root@python3lang mysite]# python manage.py migrate




关于 static file 的 cache 问题:
      https://stackoverflow.com/questions/23215581/unable-to-perform-collectstatic
      https://stackoverflow.com/questions/27911070/django-wont-refresh-staticfiles
      https://stackoverflow.com/questions/6014663/django-static-file-not-found

      (tutorial-venv) [root@python3lang mysite]# python manage.py collectstatic --noinput --clear
      (tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000
























