from datetime import timedelta
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.decorators.http import require_POST
from django.utils import timezone
from picture.forms import PublishImgForm
from picture.models import PictureEntry, PicVoteLog


# Create your views here.


def list_limit_time():
    return timezone.localdate() - timedelta(days=30)


class ImgList(ListView):
    template_name = 'picture/img_list.html'
    queryset = PictureEntry.objects.select_related('uploader').filter(
        checked=True, pub_time__date__gt=list_limit_time()
    ).order_by('-pub_time')

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

            if paginator.num_pages-cur_num > 11:
                back_pages = [cur_num+1, cur_num+2, cur_num+3, cur_num+4, '...', paginator.num_pages]
            else:
                back_pages = list(range(cur_num+1, paginator.num_pages+1))

        content['front'] = front_pages
        content['back'] = back_pages

        return content


@require_POST
@login_required(login_url=reverse_lazy('siteuser:login'))
def get_publication_img(request):
    new_pub_form = PublishImgForm(request.POST)
    if new_pub_form.is_valid():
        request.user.pictureentry_set.create(
            img_url=new_pub_form.cleaned_data['img_url'],
            description=new_pub_form['description'],
        )


@require_POST
def pic_vote(request):
    try:
        pic_id = int(request.POST['pic'])
        pic = PictureEntry.objects.get(id=pic_id)
    except ValueError:
        return JsonResponse({'result': 'some error'})

    ip = request.META.get('REMOTE_ADDR ')
    vtype = 0
    if request.POST['type'] == 'pos':
        vtype = 1

    obj, created = pic.picvotelog_set.get_or_create(
        remote_ip=ip,
        type=vtype,
    )
    if not created:
        return JsonResponse({'result': '已投过票'}, json_dumps_params={
            'ensure_ascii': False
        })
    else:
        return JsonResponse({'result': 'ok'})
