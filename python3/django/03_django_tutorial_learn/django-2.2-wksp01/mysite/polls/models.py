from django.db import models

# Create your models here.

# https://docs.djangoproject.com/en/2.2/ref/models/instances/#django.db.models.Model
# https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.Field
# https://docs.djangoproject.com/en/2.2/ref/models/fields/#charfield

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


class Choice(models.Model):
    # 外键
    # https://docs.djangoproject.com/en/2.2/ref/models/fields/#django.db.models.ForeignKey
    # Django supports all the common database relationships: many-to-one, many-to-many, and one-to-one.
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
