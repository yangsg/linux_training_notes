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
from django.urls import path, re_path, include
from . import hello

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', hello.index_action),
    path('httpresponse_action/', hello.httpresponse_action),
    path('redirect_action/', hello.redirect_action),
    path('render_action/', hello.render_action),

    path('get_request_form/', hello.get_request_form),
    path('get_request_action/', hello.get_request_action),
    path('post_request_action/', hello.post_request_action),


    #// 包含正则表达式的url
    re_path('urlparam_pattern/\d+', hello.urlparam_pattern),
    re_path('urlparam_pattern_group/(\d+)/(\d+)', hello.urlparam_pattern_group),
    re_path('urlparam_named_pattern_group/(?P<user_id>\d+)/(?P<book_id>\d+)', hello.urlparam_named_pattern_group),
    re_path('urlparam_var_args/(\d+)/(\d+)', hello.urlparam_var_args),
    re_path('urlparam_var_kwargs/(?P<userid>\d+)/(?P<bookid>\d+)', hello.urlparam_var_kwargs),

    #// https://docs.djangoproject.com/en/2.2/topics/http/urls/#naming-url-patterns
    #// https://docs.djangoproject.com/en/2.2/ref/urlresolvers/
    re_path(r'url_tag_demo01/', hello.url_tag_demo01),
    re_path(r'url_tag_demo02/(\d+)/(\d+)', hello.url_tag_demo02, name='url_reverse_name_ref'),
    re_path(r'url_reverse_fn01/(\d+)/(\d+)', hello.url_reverse_fn01, name='url_reverse_fn01'),
    re_path(r'url_reverse_fn02/(?P<user_id>\d+)/(?P<group_id>\d+)', hello.url_reverse_fn02, name='url_reverse_fn02'),

    re_path(r'url_reverse_fn03/(\d+)/(\d+)', hello.url_reverse_fn03, name='url_reverse_fn03'),
    re_path(r'url_reverse_fn04/(?P<user_id>\d+)/(?P<group_id>\d+)', hello.url_reverse_fn04, name='url_reverse_fn04'),

    #// url dispatcher  url分发
    #// https://docs.djangoproject.com/en/2.2/topics/http/urls/#url-dispatcher
    #// https://docs.djangoproject.com/en/2.2/topics/http/urls/#including-other-urlconfs
     path('app01/', include('app01.urls')),


    re_path(r'escape_html_demo/', hello.escape_html_demo, name='escape_html_demo'),

]


