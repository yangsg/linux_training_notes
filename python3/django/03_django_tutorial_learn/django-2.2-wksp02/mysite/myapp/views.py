import logging

from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.views import View

from .forms import UserCreateForm, UserUpdateForm
from .models import User

logger = logging.getLogger('django')


def index(request):
    return HttpResponse('index page')


class UserList(View):
    def get(self, request):
        user_list = User.objects.all()
        return render(request, 'myapp/user_list.html', {'user_list': user_list})


class UserDetail(View):
    def get(self, request):
        pass
        # user_list = User.objects.get(pk=)


class UserNameExistedCheck(View):
    def post(self, request):
        name = request.POST.get('name')
        if not name:
            return JsonResponse({
                'error_msg': '没有提供用户名'
            }, status=400)

        is_existed = User.objects.filter(name__iexact=name).exists()

        if request.is_ajax():
            return JsonResponse({'is_existed': is_existed})
        else:
            return HttpResponse(f'is_existed: {is_existed}')


class UserCreate(View):
    def get(self, request):
        form = UserCreateForm()
        return render(request, 'myapp/user_create_input_form.html', {'form': form})

    def post(self, request):
        form = UserCreateForm(request.POST)
        if not form.is_valid():
            return render(request, 'myapp/user_create_input_form.html', {'form': form})

        name = form.cleaned_data['name']
        password = form.cleaned_data['password']

        user = User(name=name,
                    password=password)
        user.save()

        # logger.debug(name)
        # logger.debug(password)

        return HttpResponseRedirect(reverse('myapp:user_list'))


class UserUpdate(View):
    def get(self, request, id):
        user = User.objects.get(id=id)

        user_data = dict(
            id=user.id,
            name=user.name,
            password=user.password,
        )
        form = UserUpdateForm(user_data)

        return render(request, 'myapp/user_update_input_form.html', {'form': form})
        # return HttpResponse('update page')

    def post(self, request, id):
        form = UserUpdateForm(request.POST)

        if not form.is_valid():
            return render(request, 'myapp/user_update_input_form.html', {'form': form})

        user = User(
            id=form.cleaned_data['id'],
            name=form.cleaned_data['name'],
            password=form.cleaned_data['password'],
        )
        user.save()

        return HttpResponseRedirect(reverse('myapp:user_list'))


class UserDelete(View):
    def get(self, request, id):
        user = User.objects.get(id=id)

        user_data = dict(
            id=user.id,
            name=user.name,
            password=user.password,
        )
        form = UserUpdateForm(user_data)

        return render(request, 'myapp/user_delete_confirm.html', {'form': form})
        # return HttpResponse('update page')

    def post(self, request, id):
        user = User.objects.get(id=id)
        user.delete()

        return HttpResponseRedirect(reverse('myapp:user_list'))
