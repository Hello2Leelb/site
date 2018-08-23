from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from siteuser.models import User
from siteuser.forms import AuthSiteUserForm, SiteUserCreationForm

# Register your models here.


class UserAdmin(BaseUserAdmin):
    # 自带的这两个表单与自带User模型绑定，使用自定模型对应的form
    form = AuthSiteUserForm
    add_form = SiteUserCreationForm

    list_display = ('username', 'email', 'last_login')
    # list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ()}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
