# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-01 10:58
#   FileName = permissions

from rest_framework import permissions


class IsValidUser(permissions.IsAuthenticated, permissions.BasePermission):
    """ Allow access to valid user, is active and not expired """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_valid


class IsSuperUser(IsValidUser):
    """ Allow access admin user """

    def has_permission(self, request, view):
        return super().has_permission(request, view) and request.user.is_superuser


class IsCurrentUserOrReadOnly(permissions.BasePermission):
    """ Allow access current user, otherwise only read """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj == request.user
