import datetime

from django.db import models

# Create your models here.

# https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model
# https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.Field
# https://docs.djangoproject.com/en/2.2/ref/models/fields/#charfield
from django.utils import timezone

'''
The name of each Field instance (e.g. question_text or pub_date) is the field’s name,
in machine-friendly format. You’ll use this value in your Python code,
and your database will use it as the column name.
'''


class Question(models.Model):
    # 如下 必选的关键字参数 'max_length=200' 不仅会用于 database schema, 还会用于 validation
    question_text = models.CharField(max_length=200)
    # 如下 可选的第一个位置参数 'date published' 用于指定 a human-readable name
    #  That’s used in a couple of introspective parts of Django, and it doubles as documentation.
    #  If this field isn’t provided, Django will use the machine-readable name.
    pub_date = models.DateTimeField('date published')

    '''
    添加 __str__ 方法
    https://docs.djangoproject.com/en/2.2/intro/tutorial02/#playing-with-the-api
        It’s important to add __str__() methods to your models,
        not only for your own convenience when dealing with the interactive prompt,
        but also because objects’ representations are used throughout
        Django’s automatically-generated admin.
    '''

    def __str__(self):
        return self.question_text

    '''
    添加 一个 仅用于 演示用的  was_published_recently 方法:
        https://docs.djangoproject.com/en/2.2/intro/tutorial02/#playing-with-the-api

        Note the addition of import datetime and from django.utils import timezone,
        to reference Python’s standard datetime module and Django’s time-zone-related
        utilities in django.utils.timezone, respectively. If you aren’t familiar with
        time zone handling in Python, you can learn more in the time zone support docs.

        关于 Time zones:
            https://docs.djangoproject.com/en/2.2/topics/i18n/timezones/
    '''

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    # 外键
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey
    # Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    '''
    添加 __str__ 方法
        https://docs.djangoproject.com/en/2.2/intro/tutorial02/#playing-with-the-api
    '''

    def __str__(self):
        return self.choice_text
