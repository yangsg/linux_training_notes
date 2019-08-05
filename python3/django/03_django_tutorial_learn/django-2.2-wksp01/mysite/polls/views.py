from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader

from .models import Question

'''
def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")
'''

'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
'''

# https://docs.djangoproject.com/en/2.2/intro/tutorial03/#write-views-that-actually-do-something
'''
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))
'''


# https://docs.djangoproject.com/en/2.2/intro/tutorial03/#a-shortcut-render
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)


'''
https://docs.djangoproject.com/en/2.2/intro/tutorial03/

  In Django, web pages and other content are delivered by views. Each view is represented
  by a simple Python function (or method, in the case of class-based views).
  Django will choose a view by examining the URL that’s requested
  (to be precise, the part of the URL after the domain name).

  A URL pattern is simply the general form of a URL - for example: /newsarchive/<year>/<month>/.

  To get from a URL to a view, Django uses what are known as ‘URLconfs’. A URLconf maps URL patterns to views.

  更多关于 URLconf 的信息见:
        https://docs.djangoproject.com/en/2.2/topics/http/urls/


'''

'''
# https://docs.djangoproject.com/en/2.2/intro/tutorial03/#writing-more-views
# https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpResponse
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)
'''

'''
# https://docs.djangoproject.com/en/2.2/intro/tutorial03/#raising-a-404-error
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question': question})
'''

'''
    https://docs.djangoproject.com/en/2.2/intro/tutorial03/#a-shortcut-get-object-or-404
    https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/#django.shortcuts.get_object_or_404
    https://docs.djangoproject.com/en/2.2/topics/http/shortcuts/#django.shortcuts.get_list_or_404

The get_object_or_404() function takes a Django model as its first argument
and an arbitrary number of keyword arguments, which it passes to the get()
function of the model’s manager. It raises Http404 if the object doesn’t exist.

Django 提供 get_object_or_404() 是基于 Django 的松耦合的 设计哲学
Philosophy

        Why do we use a helper function get_object_or_404() instead of automatically
        catching the ObjectDoesNotExist exceptions at a higher level, or having
        the model API raise Http404 instead of ObjectDoesNotExist?

        Because that would couple the model layer to the view layer.
        One of the foremost design goals of Django is to maintain loose coupling.
        Some controlled coupling is introduced in the django.shortcuts module.

There’s also a get_list_or_404() function, which works just as get_object_or_404()
– except using filter() instead of get(). It raises Http404 if the list is empty.
'''


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
