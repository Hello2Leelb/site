#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, PictureEntry


class SiteUser(AuthenticationForm):

    class Meta(AuthenticationForm.Meta):
        model = User
        fields = ['username', 'password']


class SiteUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ['username', 'password']


class PublishImgForm(ModelForm):

    class Meta:
        model = PictureEntry
        fields = ['img_url', 'description']
        widgets = {
            'img_url': Textarea(attrs={'cols': 50, 'rows': 10}),
            'description': Textarea(attrs={'cols': 50, 'rows': 20}),
        }
