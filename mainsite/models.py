from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        """
        Create and save a user with the given username and password.
        """
        if not username:
            raise ValueError('The given username must be set')
        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


# class User(models.Model):
#     """
#     username password is_active last_login date_join
#     """
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
#     last_login = models.DateTimeField()
#
#     objects = UserManager()
#
#     def __str__(self):
#         return self.username


class User(AbstractBaseUser):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=20,
        primary_key=True,
        help_text=_('Required. 20 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
              'unique': _("A user with that username already exists."),
        }
    )
    password = models.CharField(_('password'), max_length=32)
    date_join = models.DateTimeField(_('date joined'), auto_created=True)

    objects = UserManager()

    USERNAME_FIELD = 'username'


class UserAuthBackend:
    def get_user(self, user_id):
        """
        :param user_id: primary key
        :return: a user object
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None):
        """
        :param request: HttpRequest and may be None
        :param username:
        :param password:
        :return: a user object that matches those credentials if the credentials are valid.
                    If they’re not valid, it should return None.
        """
        pass
        # todo

