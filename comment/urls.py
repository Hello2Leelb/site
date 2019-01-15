from django.urls import path
from comment import views


app_name = 'comment'
urlpatterns = [
    path('/comment/pub', views.pub_comment, name='comment'),
    path('/comment/<int>/<int>', views.get_all_comments, name='comments'),
    path('/comment/vote', views.vote_comment, name='vote'),
]
