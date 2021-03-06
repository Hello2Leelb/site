# -*- coding: utf-8 -*-

from django.urls import path
from picture import views


app_name = 'picture'
urlpatterns = [
    path('', views.ImgList.as_view(), name='images'),
    path('publish/', views.get_publication_img, name='publish'),
    path('vote/', views.pic_vote),
]
