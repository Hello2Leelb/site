# -*- coding: utf-8 -*-

from django.contrib.auth.backends import ModelBackend


class SiteBackend(ModelBackend):

    def _get_group_permissions(self, user_obj):
        return set()
