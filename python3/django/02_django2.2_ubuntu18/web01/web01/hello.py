from django.shortcuts import HttpResponse, redirect, render
from django.utils.html import escape
from django.urls import reverse


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
    username = request.GET.get('username')  #//这里不用request.GET['username']是为了避免不用username参数时抛出异常
    password = request.GET.get('password')
    #username = request.GET.get('us')
    hobbies = request.GET.getlist('hobbies')
    #hobbies = request.GET.getlist('xxx')
    #result = fr'{type(hobbies)} <br /> {hobbies}'
    #return HttpResponse(escape(result))


    #// http://python.astrotech.io/data-types/none.html
    #// https://stackoverflow.com/questions/23086383/how-to-test-nonetype-in-python
    #// 判断None时应该使用is 或 is not, 而不应该使用 == 或 !=
    #// None 是一个NoneType的唯一的单例对象
    if username is None or password is None:  # username没填写时为空字符串'', 如果没有提供username的参数，则为None
        return HttpResponse('username or password is not provided!')

    if username is None or password is None:  # username没填写时为空字符串'', 如果没有提供username的参数，则为None
        return HttpResponse('username or password is not provided!')

    if username == '' or password == '':  # username没填写时为空字符串'', 如果没有提供username的参数，则为None
        return HttpResponse('username or password is empty!')

    #// https://www.geeksforgeeks.org/python-program-to-check-if-string-is-empty-or-not/
    if username.isspace() or password.isspace():  # username没填写时为空字符串'', 如果没有提供username的参数，则为None
        return HttpResponse('username or password is blank!')

    result = f'username: {username}, password: {password}'
    return HttpResponse(result)


def post_request_action(request):
    if request.method == 'GET':
        return render(request, 'hello/post_request_input_form.html')
    elif request.method == 'POST':

        username = request.POST.get('username')  #//这里不用request.POST['username']是为了避免不用username参数时抛出异常
        password = request.POST.get('password')
        hobbies = request.POST.getlist('hobbies')

        return render(request, 'hello/post_request_output.html', {
            'username': username,
            'password': password,
            'hobbies': hobbies,
        })

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

def url_tag_demo01(request):
    #// return render(request, 'hello/url_tag_demo01.html')
    return HttpResponse('dummy')

def url_tag_demo02(request, id01, id02):
    return render(request, 'hello/url_tag_demo01.html', { 'id01': id01, 'id02': id02 })


#// https://docs.djangoproject.com/en/2.2/ref/urlresolvers/#reverse
def url_reverse_fn01(request, id01, id02):
    new_url = reverse("url_reverse_fn01", args=[id01, id02])
    return HttpResponse(new_url)


def url_reverse_fn02(request, user_id, group_id):
    new_url = reverse("url_reverse_fn02", kwargs={'user_id': user_id, 'group_id': group_id})
    return HttpResponse(new_url)

def url_reverse_fn03(request, *args):
    new_url = reverse("url_reverse_fn02", args=args)

    #// 简单的 Template 与 RequestContext 使用例子
    #// https://docs.djangoproject.com/en/2.2/ref/templates/api/#django.template.RequestContext
    from django.template import RequestContext, Template
    template = Template('new_url: {{new_url}}')
    context = RequestContext(request, {
        'new_url': new_url,
    })
    return HttpResponse(template.render(context))


def url_reverse_fn04(request, **kwargs):
    new_url = reverse("url_reverse_fn04", kwargs=kwargs)
    return HttpResponse(new_url)


























