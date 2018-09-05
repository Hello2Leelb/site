from django.db import models
from django.utils import timezone

# Create your models here.


class PictureEntry(models.Model):
    uploader = models.ForeignKey('siteuser.User', on_delete=models.CASCADE)
    # img_file = models.ImageField(upload_to='')
    img_url = models.URLField(max_length=300)
    description = models.CharField(max_length=500, null=True, blank=True)
    pub_time = models.DateTimeField(default=timezone.now)
    positive = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)
    checked = models.BooleanField(default=False)

    def __str__(self):
        return str(self.pk)

    # @property
    # def positive(self):
    #     return PicVoteLog.objects.filter(pic=self.pk, type=1).count()

    # @property
    # def negative(self):
    #     return PicVoteLog.objects.filter(pic=self.pk, type=0).count()

    def totaly_bad(self):
        if self.negative > 3 * self.positive:
            return True


class PicVoteLog(models.Model):
    pic = models.ForeignKey(PictureEntry, on_delete=models.CASCADE)
    src = models.CharField(max_length=50, null=True)
    type = models.IntegerField()
