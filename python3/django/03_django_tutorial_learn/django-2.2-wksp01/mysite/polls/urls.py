from django.urls import path

from . import views

'''
Namespacing URL names

    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#namespacing-url-names

The tutorial project has just one app, polls. In real Django projects, there might be five,
ten, twenty apps or more. How does Django differentiate the URL names between them? For example,
the polls app has a detail view, and so might an app on the same project that is
for a blog. How does one make it so that Django knows which app view to create
for a url when using the {% url %} template tag?

The answer is to add namespaces to your URLconf. In the polls/urls.py file,
go ahead and add an app_name to set the application namespace:

'''
# 定义 app 的 application namespace
# 有了 app 的 名字空间后, 就可以使用如:
#  <li><a href="{% url 'polls:detail' question.id %}">{{ question.question_text }}</a></li>
#  的方式来 引用 url 而不用再担心 不同 app 的 url 名字冲突的问题
app_name = 'polls'  # 定义 app 的 名字空间(app namespace)

'''
urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),  # https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.path
    # https://docs.djangoproject.com/en/2.2/intro/tutorial03/#writing-more-views
    # ex: /polls/5/
    # https://docs.djangoproject.com/en/2.2/intro/tutorial03/#removing-hardcoded-urls-in-templates
    # the 'name' value as called by the {% url %} template tag
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
'''
# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#use-generic-views-less-code-is-better
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # 注意如下 2 行代码中的 url pattern 从  <question_id> 修改为了 <pk>
    # https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
    # The DetailView generic view expects the primary key value captured
    # from the URL to be called "pk", so we’ve changed question_id to pk for the generic views.
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]


'''
    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#writing-more-views

 url 匹配 处理流程:
     When somebody requests a page from your website – say,
     “/polls/34/”, Django will load the mysite.urls Python module
     because it’s pointed to by the ROOT_URLCONF setting.
     It finds the variable named urlpatterns and traverses the patterns
     in order. After finding the match at 'polls/', it strips off
     the matching text ("polls/") and sends the remaining
     text – "34/" – to the ‘polls.urls’ URLconf for further processing.
     There it matches '<int:question_id>/', resulting
     in a call to the detail() view like so:

     detail(request=<HttpRequest object>, question_id=34)

     The question_id=34 part comes from <int:question_id>.
     Using angle brackets “captures” part of the URL and sends it as
     a keyword argument to the view function. The :question_id> part
     of the string defines the name that will be used to identify the matched pattern,
     and the <int: part is a converter that determines what patterns
     should match this part of the URL path.
'''
