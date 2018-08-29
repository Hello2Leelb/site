from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from picture.forms import PublishImgForm
from picture.models import PictureEntry


# Create your views here.


# def imgs_list(request):
#     return render(request, 'picture/img_list.html', content_type='text/html')

class ImgsList(ListView):
    template_name = 'picture/img_list.html'
    queryset = PictureEntry.objects.select_related('uploader').filter(checked=True).order_by('-upload_time')
    paginate_by = 10
    context_object_name = 'entry_list'
    extra_context = {'form': PublishImgForm()}

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data()
        if not content['is_paginated']:
            content['front'] = []
            content['back'] = []
            return content

        paginator = content['paginator']
        cur_page = content['page_obj']
        cur_num = cur_page.number
        if paginator.num_pages <= 13:
            front_pages = list(range(1, cur_num))
            back_pages = list(range(cur_num+1, paginator.num_pages+1))
        else:
            if cur_num-1 <= 6:
                front_pages = list(range(1, cur_num))
            else:
                front_pages = [1, '...', cur_num-4, cur_num-3, cur_num-2, cur_num-1]

            if paginator.num_pages-cur_num > 13:
                back_pages = [cur_num+1, cur_num+2, cur_num+3, cur_num+4, '...', paginator.num_pages]
            else:
                back_pages = list(range(cur_num+1, paginator.num_pages+1))

        content['front'] = front_pages
        content['back'] = back_pages

        return content


@login_required(login_url=reverse('siteuser:login'))
def get_publication_img(request):
    new_pub_form = PublishImgForm(request.POST)
    if new_pub_form.is_valid():
        request.user.pictureentry_set.create(
            img_url=new_pub_form.cleaned_data['img_url'],
            description=new_pub_form['description'],
        )
