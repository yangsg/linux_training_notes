from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.template import loader
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Question, Choice

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

''' 改用 IndexView
# https://docs.djangoproject.com/en/2.2/intro/tutorial03/#a-shortcut-render
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)
'''


# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#use-generic-views-less-code-is-better
# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
# https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#django.views.generic.list.ListView
#  更多 generic views 的信息, 见:
#     https://docs.djangoproject.com/en/2.2/topics/class-based-views/
class IndexView(generic.ListView):
    # https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
    # 类似于 DetailView, the ListView generic view 默认使用
    # 的 template 名为 <app name>/<model name>_list.html, 在我们的例子中
    # 即为 polls/question_list.html,
    # 我们可以使用 template_name 告诉 ListView 使用指定的 template 'polls/index.html'
    template_name = 'polls/index.html'
    # 修改 属性 context_object_name (如果不修改, 其值此处 默认为  'question_list')
    # In previous parts of the tutorial, the templates have
    # been provided with a context that contains the question
    # and latest_question_list context variables. For DetailView the question
    # variable is provided automatically – since we’re using a Django model(Question),
    # Django is able to determine an appropriate name for the context variable.
    # However, for ListView, the automatically generated context variable is question_list.
    # To override this we provide the context_object_name attribute, specifying
    # that we want to use latest_question_list instead. As an alternative approach,
    # you could change your templates to match the new default context variables – but
    # it’s a lot easier to just tell Django to use the variable you want.
    context_object_name = 'latest_question_list'

    '''
    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]
    '''

    # https://docs.djangoproject.com/en/2.2/intro/tutorial05/#improving-our-view
    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')[:5]


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

''' 改用 DetailView
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})
'''

'''
# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#use-generic-views-less-code-is-better
# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
# https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
#  更多 generic views 的信息, 见:
#     https://docs.djangoproject.com/en/2.2/topics/class-based-views/

We’re using two generic views here: ListView and DetailView.
Respectively, those two views abstract the concepts of
“display a list of objects” and “display a detail page for a particular type of object.”

修改 model 属性
- Each generic view needs to know what model it will be acting upon.
  This is provided using the model attribute.

- The DetailView generic view expects the primary key value captured
  from the URL to be called "pk", so we’ve changed question_id to pk for the generic views.

        path('<int:pk>/', views.DetailView.as_view(), name='detail'),


'''


class DetailView(generic.DetailView):
    # https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
    # In previous parts of the tutorial, the templates have been provided with
    # a context that contains the question and latest_question_list context variables.
    # For DetailView the question variable is provided automatically – since
    # we’re using a Django model (Question), Django is able to determine an
    # appropriate name for the context variable.
    model = Question
    # https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
    #   默认 the DetailView generic view 使用的 template 名为
    #   <app name>/<model name>_detail.html, 在我们的的应用中,
    #   则 默认为 polls/question_detail.html, 而属性 template_name
    #   可用于告诉 Django 使用指定的 template name 非不是使用自动生成的
    #   default template name.
    template_name = 'polls/detail.html'

    # https://docs.djangoproject.com/en/2.2/intro/tutorial05/#testing-the-detailview
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


'''
def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)
'''

''' 改用 ResultsView
# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#write-a-simple-form
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})
'''


# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#use-generic-views-less-code-is-better
# https://docs.djangoproject.com/en/2.2/intro/tutorial04/#amend-views
# https://docs.djangoproject.com/en/2.2/ref/class-based-views/generic-display/#django.views.generic.detail.DetailView
class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


'''
def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
'''

'''
该 注释 用于解释 如下 的 vote 函数

https://docs.djangoproject.com/en/2.2/intro/tutorial04/#write-a-simple-form

This code includes a few things we haven’t covered yet in this tutorial:

    https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest.POST

request.POST 是一个类似 dictionary 的对象,request.POST 中的 values 总是 strings.
    request.POST is a dictionary-like object that lets you access submitted
    data by key name. In this case, request.POST['choice'] returns the
    ID of the selected choice, as a string. request.POST values are always strings.

        https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpRequest.GET

    Note that Django also provides request.GET for accessing GET data in the same way
    – but we’re explicitly using request.POST in our code, to ensure
    that data is only altered via a POST call.

如果 在 POST data 中没有提供 choice, 则 request.POST['choice'] 将 raise KeyError
    request.POST['choice'] will raise KeyError if choice wasn’t provided in POST data.
    The above code checks for KeyError and redisplays the question form with
    an error message if choice isn’t given.

https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.HttpResponseRedirect

使用 HttpResponseRedirect 执行重定向
    After incrementing the choice count, the code returns an HttpResponseRedirect
    rather than a normal HttpResponse. HttpResponseRedirect takes a single argument:
    the URL to which the user will be redirected (see the following point
    for how we construct the URL in this case).

    As the Python comment above points out, you should always return an
    HttpResponseRedirect after successfully dealing with POST data.
    This tip isn’t specific to Django; it’s just good Web development practice.

    https://docs.djangoproject.com/en/2.2/ref/urlresolvers/#django.urls.reverse
利用 函数 reverse() 可以避免 硬编码 url
    We are using the reverse() function in the HttpResponseRedirect constructor
    in this example. This function helps avoid having to hardcode a URL
    in the view function. It is given the name of the view that we want
    to pass control to and the variable portion of the URL pattern that
    points to that view. In this case, using the URLconf we set up in Tutorial 3,
    this reverse() call will return a string like

        '/polls/3/results/'

关于 HttpRequest 的更多信息见:
    https://docs.djangoproject.com/en/2.2/ref/request-response/


一个并发问题:
    Note

        The code for our vote() view does have a small problem.
        It first gets the selected_choice object from the database,
        then computes the new value of votes, and then saves it back
        to the database. If two users of your website try to vote
        at exactly the same time, this might go wrong: The same value,
        let’s say 42, will be retrieved for votes. Then, for both users
        the new value of 43 is computed and saved, but 44 would be the expected value.

        This is called a race condition. If you are interested, you can read
        Avoiding race conditions using F() to learn how you can solve this issue.

Avoiding race conditions using F()
    https://docs.djangoproject.com/en/2.2/ref/models/expressions/#avoiding-race-conditions-using-f
'''


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # 注: 此处 没有 考虑并发的问题,
        # 解决方案见 Avoiding race conditions using F()
        #   https://docs.djangoproject.com/en/2.2/ref/models/expressions/#avoiding-race-conditions-using-f
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
