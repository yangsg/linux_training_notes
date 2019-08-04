from django.contrib import admin

# Register your models here.
from .models import Question

# https://docs.djangoproject.com/en/2.2/intro/tutorial02/#make-the-poll-app-modifiable-in-the-admin
# https://docs.djangoproject.com/en/2.2/intro/tutorial02/#explore-the-free-admin-functionality
# to tell the admin that Question objects have an admin interface.
# 在 Django administration 网页 为  'Question' model 提供 管理接口(即管理 'Question' model 用的增删改查的 html 控件)
admin.site.register(Question)
