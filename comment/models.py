from django.db import models
# from django.utils.translation import ugettext_lazy as _
from django.utils import timezone


CommentAttachType = {
    1: 'picturex.models.PictureEntry',
}


# id target user reply content time positive negative
class UserComment(models.Model):
    user = models.ForeignKey('siteuser.User', on_delete=models.DO_NOTHING)
    target_type = models.IntegerField()
    target_id = models.IntegerField()
    reply = models.ForeignKey('self', on_delete=models.DO_NOTHING, default=-1)
    content = models.TextField()
    time = models.DateTimeField(default=timezone.now)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)

    def __str__(self):
        return self.content

    class Meta:
        indexes = [
            models.Index(fields=['target_type', 'target_id'])
        ]
        ordering = ['-time']


class CommnetVoteLog(models.Model):
    comment = models.ForeignKey(UserComment, on_delete=models.DO_NOTHING)
    voter = models.ForeignKey('siteuser.User', on_delete=models.DO_NOTHING)

