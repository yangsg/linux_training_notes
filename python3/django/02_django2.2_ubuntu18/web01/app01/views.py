from django.shortcuts import render
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse


def url_dispatcher_demo01(request):
    new_url = reverse("url_dispatcher_demo01")
    return render(request, 'app01/url_dispatcher_demo01_output.html', {'new_url': new_url})

