


yangsg@vm:~$ mkdir workspace
yangsg@vm:~$ cd workspace/
yangsg@vm:~/workspace$ sudo apt install python3-venv
yangsg@vm:~/workspace$ python3 -m venv django-env
yangsg@vm:~/workspace$ source django-env/bin/activate
(django-env) yangsg@vm:~/workspace$ pip install Django==2.2
(django-env) yangsg@vm:~/workspace$ django-admin startproject web01
(django-env) yangsg@vm:~/workspace$ tree web01/
web01/
├── manage.py
└── web01
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py

(django-env) yangsg@vm:~/workspace/web01$ python manage.py migrate
(django-env) yangsg@vm:~/workspace/web01$ python manage.py runserver 192.168.175.231:8000


(django-env) yangsg@vm:~/linux_training_notes/python3/django/02_django2.2_ubuntu18$ django-admin startproject web01
(django-env) yangsg@vm:~/linux_training_notes/python3/django/02_django2.2_ubuntu18$ tree web01/
			web01/
			├── manage.py
			└── web01
					├── __init__.py
					├── settings.py
					├── urls.py
					└── wsgi.py



















