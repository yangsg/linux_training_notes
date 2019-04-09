from django.shortcuts import HttpResponse, redirect, render


def httpresponse_action(request):
    return HttpResponse('<h1>hello world</h1>')


def redirect_action(request):
    return redirect('http://www.baidu.com')

def render_action(request):
    return render(request, 'hello.html')


def index_action(request):
    return render(request, 'index.html')









