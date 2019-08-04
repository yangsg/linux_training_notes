from django.urls import path

from . import views

urlpatterns = [
    # ex: /polls/
    path('', views.index, name='index'),  # https://docs.djangoproject.com/en/2.2/ref/urls/#django.urls.path
    # https://docs.djangoproject.com/en/2.2/intro/tutorial03/#writing-more-views
    # ex: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),
    # ex: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),
    # ex: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),

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
    '''
]
