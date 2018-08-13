#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class SiteUser(AuthenticationForm):

    class Meta(AuthenticationForm.Meta):
        model = User
        fields = ['username', 'password']


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'password']
