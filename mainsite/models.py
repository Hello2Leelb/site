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


class PictureEntry(models.Model):
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
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


class Comment:
    pass
