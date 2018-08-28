# -*- coding: utf-8 -*-

from django.urls import path
from siteuser import views

app_name = 'siteuser'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('password', views.change_password, app_name='changepwd'),
]
