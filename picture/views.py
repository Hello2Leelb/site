from datetime import timedelta
from django.shortcuts import redirect
from django.http import JsonResponse
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.views.decorators.http import require_POST
from django.utils import timezone
# from django.db.models import F
from picture.forms import PublishImgForm
from picture.models import PictureEntry


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
    extra_context = {
        'form': PublishImgForm(),
    }

    def get_context_data(self, *, object_list=None, **kwargs):
        content = super().get_context_data(**kwargs)
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
@login_required(redirect_field_name=None, login_url=reverse_lazy('siteuser:login'))
def get_publication_img(request):
    new_pub_form = PublishImgForm(request.POST)
    if new_pub_form.is_valid():
        request.user.pictureentry_set.create(
            img_url=new_pub_form.cleaned_data['img_url'],
            description=new_pub_form.cleaned_data['description'],
        )
    # return JsonResponse({'status': 'ok'})
    return redirect(reverse('picture:images'))


@require_POST
def pic_vote(request):
    if request.user.is_authenticated:
        voter = str(request.user.pk)
    else:
        voter = request.META.get('REMOTE_ADDR')
        # ip = request.META.get('HTTP_X_FORWARDED_FOR')
    vtype = 0
    if request.POST['type'] == 'pos':
        vtype = 1

    try:
        # pic_id = int(request.POST['pic'])
        pic_obj = PictureEntry.objects.get(id=int(request.POST['pic']))
    except ValueError:
        return JsonResponse({'status': 'some error'})
    except PictureEntry.DoesNotExist:
        return JsonResponse({'status': 'some error'})

    if pic_obj.picvotelog_set.filter(src=voter).exists():
        return JsonResponse({'status': '已投过票'}, json_dumps_params={
            'ensure_ascii': False
        })
    else:
        pic_obj.picvotelog_set.create(src=voter, type=vtype)
        if vtype:
            # PictureEntry.objects.filter(id=pic_id).update(positive=F('positive') + 1)
            pic_obj.positive += 1
        else:
            # PictureEntry.objects.filter(id=pic_id).update(negative=F('negative') + 1)
            pic_obj.negative += 1
        pic_obj.save()

        return JsonResponse({'status': 'ok'})
