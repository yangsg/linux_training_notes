from django.http import HttpResponse
from django.shortcuts import render

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
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


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


# https://docs.djangoproject.com/en/2.2/intro/tutorial03/#writing-more-views
def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
