# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from siteuser.models import User as SiteUser


# 参考自带表单设计，用于自定义网站用户model
class AuthSiteUserForm(AuthenticationForm):
    pass


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ['username', 'email']


# todo
