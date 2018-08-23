# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from siteuser.models import User


# 继承于自带的User相关表单，用于自定义网站用户model

class AuthSiteUserForm(AuthenticationForm):

    class Meta(AuthenticationForm.Meta):
        model = User
        fields = ['username', 'password']


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User



