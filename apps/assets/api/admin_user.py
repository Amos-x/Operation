# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-07 00:44
#   FileName = admin_user

from rest_framework.pagination import LimitOffsetPagination
from rest_framework_bulk import BulkModelViewSet
from assets.models import AdminUser
from assets.serializers import *
from common.mixins import IDInFilterMixin
from users.permissions import IsSuperUser


__all__ = ['AdminUserViewSet']


class AdminUserViewSet(IDInFilterMixin, BulkModelViewSet):
    """ Admin user api set, for add,delete,update,list,retrieve resource """
    queryset = AdminUser.objects.all()
    serializer_class = AdminUserSerializer
    permission_classes = (IsSuperUser,)
