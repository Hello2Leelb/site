# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from siteuser.models import User as SiteUser


# 参考自带表单设计，用于自定义网站用户model
class AuthSiteUserForm(AuthenticationForm):
    """
    登录验证表单，包括 username, password
    """
    pass


class SiteUserCreationForm(UserCreationForm):
    """
    注册账户，基于model User，包括 username, email, password1, password2
    其中，email非必需
    """

    class Meta(UserCreationForm.Meta):
        model = SiteUser
        fields = ['username', 'email']


class UserPasswdChangeForm(PasswordChangeForm):
    pass
