"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b1h1flpp^*0yemx*-0*#5e6)!*jb@56=gzsb9n9s2=j5$9huj@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# https://docs.djangoproject.com/en/2.2/ref/settings/#allowed-hosts
ALLOWED_HOSTS = [
    # '*',
    '192.168.175.20',
    'localhost',
    '127.0.0.1',
    '[::1]',
]

# Application definition

# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-INSTALLED_APPS
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/
# Django 为了方便 默认会 包含一些 常用的 apps
INSTALLED_APPS = [
    # 通过包含 polls app 的 配置类 PollsConfig 的引用信息,
    # 告诉 Django 安装了 polls app.
    # 相关的命令:
    #        python manage.py startapp myapp
    #        python manage.py makemigrations myapp
    #        python manage.py sqlmigrate myapp 0001
    #        python manage.py check myapp
    #        python manage.py migrate
    #  https://docs.djangoproject.com/en/2.2/ref/django-admin/#makemigrations
    #  https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-sqlmigrate
    #  https://docs.djangoproject.com/en/2.2/ref/django-admin/#check
    #  https://docs.djangoproject.com/en/2.2/ref/django-admin/#django-admin-migrate
    'myapp.apps.MyappConfig',  # <------

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

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

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

# 使用 mysql 数据库
# 在 mysql server 上创建 一个 学习用的 database
# 参考:
# https://github.com/yangsg/linux_training_notes/tree/master/python3/basic02_syntax/mod_SQLAlchemy
# https://github.com/yangsg/linux_training_notes/tree/master/python3/django/03_django_tutorial_learn
# mysql> CREATE DATABASE db_django_02 CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
# (tutorial-venv) [root@python3lang mysite]# python manage.py migrate
# (tutorial-venv) [root@python3lang mysite]# python manage.py runserver 192.168.175.20:8000
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_django_02',
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

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "staticfiles"),
]
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

print(os.path.join(BASE_DIR, "staticfiles"))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
