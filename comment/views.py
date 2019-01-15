from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from comment.models import UserComment


@require_POST
@login_required(login_url=reverse_lazy('siteuser:login'))
def pub_comment(request):
    new_com = UserComment(
        user=request.user,
        target_type=request.POST['ttype'],
        target_id=request.POST['tid'],
        content=request.POST['content'],
    )
    if 'reply' in request.POST:
        new_com.reply = UserComment.objects.get(pk=request.POST['reply'])
    new_com.save()

    return JsonResponse({'status': 'ok'})


# 可能要考虑用分页
def get_all_comments(request, o_type, o_key):
    comments = UserComment.objects.select_related('user').filter(target_type=o_type, target_id=o_key)
    tops = comments.filter(positive__lte=10).order_by('-positive', 'negative')
    comments_list = []
    for comment in comments:
        tmp = {
            'cid': comment.pk,
            'user': comment.user.username,
            'content': comment.content,
            'pos': comment.positive,
            'neg': comment.negative,
        }
        if comment.reply != -1:
            tmp['reply'] = '@ %s' % comment.reply.user.username
        else:
            tmp['reply'] = ''
        comments_list.append(tmp)

    n_comments_10 = len(comments) // 10
    n_tops = n_comments_10 if n_comments_10 <= 10 else 10
    tops_list = [comment.pk for comment in tops[:n_tops]]

    return JsonResponse({'commets': comments_list, 'hot': tops_list})


@require_POST
@login_required(login_url=reverse_lazy('siteuser:login'))
def vote_comment(request):
    vote_type = 0
    if request.POST['type'] == 'pos':
        vote_type = 1

    com_obg = UserComment.objects.get(pk=request.POST['cid'])
    if com_obg.commnetvotelog_set.filter(voter=request.user).exsits():
        return JsonResponse({'status': '已投过票'}, json_dumps_params={
            'ensure_ascii': False
        })
    else:
        com_obg.commnetvotelog_set.create(comment=com_obg, voter=request.user)
        if vote_type:
            com_obg.positive += 1
        else:
            com_obg.negative += 1
        com_obg.save()

        return JsonResponse({'status': 'ok'})
