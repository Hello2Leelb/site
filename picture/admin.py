from django.contrib import admin
from picture.models import PictureEntry

# Register your models here.


class PictureAdmin(admin.ModelAdmin):
    actions = ['make_published']
    actions_on_bottom = True
    list_display = ('uploader', 'img_url', 'pub_time', 'checked')
    list_editable = ('checked',)
    list_per_page = 50

    def make_published(self, request, queryset):
        queryset.update(checked=True)
    make_published.short_description = 'Mark selected stories as checked'


admin.site.register(PictureEntry, PictureAdmin)
