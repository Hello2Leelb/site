from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from picture.forms import PublishImgForm


# Create your views here.


def imgs_list(request):
    return render(request, 'picture/img_publish_part.html', content_type='text/html')


@login_required(login_url=reverse('siteuser:login'))
def get_publication_img(request):
    new_pub_form = PublishImgForm(request.POST)
    if new_pub_form.is_valid():
        request.user.pictureentry_set.create(
            img_url=new_pub_form.cleaned_data['img_url'],
            description=new_pub_form['description'],
        )
