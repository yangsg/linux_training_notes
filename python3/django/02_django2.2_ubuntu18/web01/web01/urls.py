"""web01 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('httpresponse_action/', hello.httpresponse_action),  #// http://192.168.175.231:8000/httpresponse_action/
    path('redirect_action/', hello.redirect_action),          #// http://192.168.175.231:8000/redirect_action/
    path('render_action/', hello.render_action),              #// http://192.168.175.231:8000/render_action/
    path('', hello.index_action),                             #// http://192.168.175.231:8000
]
