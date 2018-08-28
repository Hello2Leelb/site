from urllib.parse import urlparse

from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from siteuser.forms import *
from picture.views import imgs_list

# Create your views here.


def register(request):
    if request.method == 'POST':
        new_user_form = SiteUserCreationForm(request.POST)
        if new_user_form.is_valid():
            new_user_form.save()

            reged_user = authenticate(
                username=new_user_form.cleaned_data['username'],
                password=new_user_form.cleaned_data['password1'],
            )
            login(request, reged_user)
            # 携带request?
            return redirect(reverse('siteuser:index'))

    else:
        new_user_form = SiteUserCreationForm()

    return render(request, template_name='siteuser/register.html', context={
        'form': new_user_form
    })


def login_user(request):
    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        # logining_user = authenticate(request, username=username, password=password)

        auth_form = AuthSiteUserForm(request)
        if auth_form.is_valid():
            # 验证数据合法时，同时authenticate()验证返回对象实例
            logining_user = auth_form.get_user()
            if logining_user.is_authenticated:
                login(request, logining_user)

                qs = QueryDict(urlparse(request.url).query, mutable=True)
                login_from = qs.get('next')
                if login_from:
                    return redirect(login_from)
                else:
                    return redirect(reverse('siteuser:index'))

    else:
        auth_form = AuthSiteUserForm()

    return render(request, 'siteuser/login_page.html', context={
         'form': auth_form,
    },)

# 第一次登录，cookie中只有csrf_token，验证系统中间件返回AnonymousUser。后台的login_view中，验证表单通过账号密码获取用户对象。


def logout_user(request):
    logout(request)
    return redirect(reverse('siteuser:index'))


@login_required(login_url=reverse('siteuser:login'))
def change_password(request):
    if request.method == 'POST':
        change_form = UserPasswdChangeForm(request.user)
        if change_form.is_valid():
            change_form.save()
        return request(reverse('siteuser:login'))

    else:
        change_form = UserPasswdChangeForm(None)

    return render(request, template_name='siteuser/change_pwd.html', context={
        'form': change_form
    })


def index(request):
    imgs_list(request)
