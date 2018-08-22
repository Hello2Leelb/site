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
        reging_user = authenticate(
            username=new_user_form.cleaned_data['username'],
            password=new_user_form.cleaned_data['password1'],
        )
        login(request, reging_user)
        return redirect(reverse('siteuser:index'))


def login_user(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            login(request, request.user)
            return redirect(reverse('siteuser:index'))
    elif request.method == 'GET':
        return render(request, 'siteuser/login_page.html', {
             'form': SiteUser,
        },)


def logout_user(request):
    logout(request)
    return redirect(reverse('siteuser:index'))


def index(request):
    imgs_list(request)
