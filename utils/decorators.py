# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

__author__ = 'antonio'


def login_required_or_403(function=None):

    def test_auth(user):
        if not user.is_authenticated():
            raise PermissionDenied

        return True

    actual_decorator = user_passes_test(test_auth)
    if function:
        return actual_decorator(function)

    return actual_decorator
