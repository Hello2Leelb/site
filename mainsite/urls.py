# -*- coding: utf-8 -*-

from django.urls import path
from . import views

app_name = 'miansite'
urlpatterns = [
    path('', '', name='index'),
    path('user/register/', views.register_view, name='register'),
    path('user/login/', views.login_view, name='login'),
    path('user/logout/', views.logout_view, name='logout')
]
