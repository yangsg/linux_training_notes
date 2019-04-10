from django.shortcuts import HttpResponse, redirect, render
from django.utils.html import escape


def httpresponse_action(request):
    return HttpResponse('<h1>hello world</h1>')


def redirect_action(request):
    return redirect('http://www.baidu.com')

def render_action(request):
    return render(request, 'hello.html')


def index_action(request):
    return render(request, 'index.html')


def get_request_form(request):
    return render(request, 'hello/get_request_input_form.html')

def get_request_action(request):
    #// https://docs.djangoproject.com/en/2.2/ref/request-response/
    #// https://docs.djangoproject.com/en/2.2/ref/request-response/#django.http.QueryDict
    username = request.GET.get('username')
    username = request.GET.get('us')
    hobbies = request.GET.getlist('hobbies')
    print(username)
    print(type(username))

    #// http://python.astrotech.io/data-types/none.html
    #// https://stackoverflow.com/questions/23086383/how-to-test-nonetype-in-python
    #// 判断None时应该使用is 或 is not, 而不应该使用 == 或 !=
    #// None 是一个NoneType的唯一的单例对象
    if username is None or password is None:
        return HttpResponse('username or password is empty!')


    result = f'username: {username}, password: {password}'
    return HttpResponse(result)


def post_request_action(request):
    if request.method == 'GET':
        return render(request, 'hello/post_request_input_form.html')
    elif request.method == 'POST':
        return render(request, 'hello/post_request_input_form.html')

def urlparam_pattern(request):
    return HttpResponse(r"path('urlparam/\d+', hello.urlparam_id)")


#// re_path('urlparam_pattern_group/(\d+)/(\d+)', hello.urlparam_pattern_group),
#// 对于url pattern中的非命名group, 处理函数中变量的名字是随意的
def urlparam_pattern_group(request, a, b):
    return HttpResponse(f'a: {a}, b: {b}')

#// re_path('urlparam_named_pattern_group/(?P<user_id>\d+)/(?P<book_id>\d+)', hello.urlparam_named_pattern_group),
#// 此处函数中变量名必须与url pattern中的group的名字一致, 不过函数参数变量的顺序是随意的
def urlparam_named_pattern_group(request, user_id, book_id):
    return HttpResponse(f'user_id: {user_id}, book_id: {book_id}')

def urlparam_var_args(request, *args):
    return HttpResponse(escape(str(args)))


def urlparam_var_kwargs(request, **kwargs):
    return HttpResponse(escape(str(kwargs)))


