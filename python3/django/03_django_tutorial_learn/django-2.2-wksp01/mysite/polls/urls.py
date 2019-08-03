from django.urls import path

from mysite.polls import views

urlpatterns = [
    path('', views.index, name='index'),  # https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.path
]
