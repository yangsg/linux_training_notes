"""mysite URL Configuration

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
from django.urls import path, include

urlpatterns = [
    #https://docs.djangoproject.com/en/2.2/intro/tutorial01/#path-argument-route
    #格式: path(route, view, kwargs=None, name=None)

    #    route is a string that contains a URL pattern. When processing a request,
    #    Django starts at the first pattern in urlpatterns and makes its way down the list,
    #    comparing the requested URL against each pattern until it finds one that matches.

    #    Patterns don’t search GET and POST parameters, or the domain name.
    #    For example, in a request to https://www.example.com/myapp/,
    #    the URLconf will look for myapp/.
    #    In a request to https://www.example.com/myapp/?page=3,
    #    the URLconf will also look for myapp/.
    path('polls/', include('polls.urls')),  # https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.include
    path('admin/', admin.site.urls),
]
