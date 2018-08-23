from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Create your models here.


class SiteUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, password, **extra_fields)


class User(AbstractUser):

    username = models.CharField(
        _('username'),
        max_length=150,
        primary_key=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[AbstractUser.username_validator],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )

    is_active = True

    # 账号信息去除部分，email不用于注册登陆
    # email = None
    first_name = None
    last_name = None
    # 权限部分信息
    groups = None

    objects = SiteUserManager()


# class User(AbstractBaseUser):
#     username_validator = UnicodeUsernameValidator()
#
#     username = models.CharField(
#         _('username'),
#         max_length=20,
#         primary_key=True,
#         help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
#         validators=[username_validator],
#         error_messages={
#               'unique': _("A user with that username already exists."),
#         }
#     )
#     password = models.CharField(_('password'), max_length=32)
#     date_join = models.DateTimeField(_('date joined'), auto_created=True)
#
#     objects = SiteUserManager()
#
#     USERNAME_FIELD = 'username'
