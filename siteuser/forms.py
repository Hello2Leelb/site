# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from siteuser.models import User


# 参考自带表单设计，用于自定义网站用户model
class AuthSiteUserForm(AuthenticationForm):

    class Meta(AuthenticationForm.Meta):
        model = User
        fields = ['username', 'password']


# todo
class SiteUserCreationForm(forms.ModelForm):
    pass
