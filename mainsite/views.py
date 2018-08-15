from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import *

# Create your views here.


def register_view(request):
    pass


def login_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            login(request, request.user)
            return redirect(reverse('mainsite:index'))
    elif request.method == 'GET':
        return render(request, 'mainsite/login_page.html', {
             'form': PublishImgForm,
        },)


def logout_view(request):
    logout(request)
    return redirect(reverse('mainsite:index'))


@login_required(login_url=reverse('mainsite:login'))
def get_publication_img(request):
    # 之后可以添加类型type，处理多种上传
    new_pub_form = PublishImgForm(request.POST)
    if new_pub_form.is_valid():
        request.user.pictureentry_set.create(
            img_url=new_pub_form.cleaned_data['img_url'],
            description=new_pub_form['description'],
        )
