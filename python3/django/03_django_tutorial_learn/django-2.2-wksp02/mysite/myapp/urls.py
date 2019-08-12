from django.urls import path

from . import views

app_name = 'myapp'  # 定义 app 的 名字空间(app namespace)

urlpatterns = [
    # (tutorial-venv) [root@python3lang mysite]# vim myapp/urls.py
    path('', views.index, name='index'),  # https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.path
    path('user/list/', views.UserList.as_view(), name='user_list'),
    path('user/detail/<int:id>/', views.UserDetail.as_view(), name='user_detail'),
    path('user/create/', views.UserCreate.as_view(), name='user_create'),
    path('user/update/<int:id>/', views.UserUpdate.as_view(), name='user_update'),
    path('user/delete/<int:id>/', views.UserDelete.as_view(), name='user_delete'),
    path('user/name_existed_check/', views.UserNameExistedCheck.as_view(), name='name_existed_check'),
]
