# -*- coding: utf-8 -*-

from .models import User


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

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        :param request: HttpRequest and may be None
        :param username:
        :param password:
        :return: a user object that matches those credentials if the credentials are valid.
                    If they’re not valid, it should return None.
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)
        try:
            # user = User._default_manager.get_by_natural_key(username)
            user = User.objects.get(username)
        except User.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            User().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
