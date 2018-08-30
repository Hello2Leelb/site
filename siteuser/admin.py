from django.contrib import admin
from django.contrib.auth.models import Group
from siteuser.models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'last_login')
    list_per_page = 50


admin.site.register(User, UserAdmin)
# admin.site.unregister(Group)
