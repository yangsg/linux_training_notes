from django.urls import path, re_path, include
from app01 import views

urlpatterns = [
    path('url_dispatcher_demo01/', views.url_dispatcher_demo01, name='url_dispatcher_demo01'),
]


