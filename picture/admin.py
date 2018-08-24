from django.contrib import admin
from picture.models import PictureEntry

# Register your models here.


class PictureAdmin(admin.ModelAdmin):
    pass


admin.site.register(PictureEntry, PictureAdmin)
