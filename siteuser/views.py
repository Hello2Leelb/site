from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from siteuser.forms import *
from picture.views import imgs_list

# Create your views here.


def register(request):
    new_user_form = SiteUserCreationForm(request.POST)
    if new_user_form.is_valid():
        new_user_form.save()

        reged_user = authenticate(
            username=new_user_form.cleaned_data['username'],
            password=new_user_form.cleaned_data['password1'],
        )
        login(request, reged_user)
        return redirect(reverse('siteuser:index'))


def login_user(request):
    if request.method == 'POST':
        # username = request.POST['username']
        # password = request.POST['password']
        # logining_user = authenticate(request, username=username, password=password)
        # 自带表单验证数据合法时(username,password)，也authenticate验证用户模型实例
        auth_form = AuthSiteUserForm(request)
        if auth_form.is_valid():
            logining_user = auth_form.get_user()
            if logining_user.is_authenticated:
                login(request, request.user)
                return redirect(reverse('siteuser:index'))

    elif request.method == 'GET':
        return render(request, 'siteuser/login_page.html', {
             'form': AuthSiteUserForm,
        },)


def logout_user(request):
    logout(request)
    return redirect(reverse('siteuser:index'))


def index(request):
    imgs_list(request)
