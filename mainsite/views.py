from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .forms import *

# Create your views here.


def login_view(request):
    if request.user.is_authenticated:
        login(request, request.user)


def logout_view(request):
    logout(request)


@login_required()
def get_publication_img(request):
    # type
    new_pub_form = PublishImgForm(request.POST)
    if new_pub_form.is_valid():
        new_pub_form.save()
