from django.db import models

# Create your models here.


class PictureEntry(models.Model):
    uploader = models.ForeignKey('siteuser.User', on_delete=models.CASCADE)
    # img_file = models.ImageField(upload_to='')
    img_url = models.URLField(max_length=300)
    description = models.CharField(max_length=500, null=True, blank=True)
    upload_time = models.DateTimeField(auto_now_add=True)
    approval = models.IntegerField(default=0)
    negative = models.IntegerField(default=0)

    def __str__(self):
        pass

    def totaly_bad(self):
        if self.negative > 3 * self.approval:
            return True
