# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend
from siteuser.models import User as SiteUser


class SiteBackend(ModelBackend):

    def get_user(self, user_id):
        """
        :param user_id: primary key
        :return: a user object
        """
        try:
            return SiteUser.objects.get(pk=user_id)
        except SiteUser.DoesNotExist:
            return None

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request: HttpRequest and may be None
        :param username:
        :param password:
        :return: a user object that matches those credentials if the credentials are valid.
                    If they’re not valid, it should return None.
        """
        if username is None:
            username = kwargs.get(SiteUser.USERNAME_FIELD)
        try:
            user = SiteUser.objects.get_by_natural_key(username)
        except SiteUser.DoesNotExist:
            SiteUser().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user
