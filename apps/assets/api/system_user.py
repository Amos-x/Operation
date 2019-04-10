# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 10:51
#   FileName = system_user

from rest_framework_bulk import BulkModelViewSet
from assets.models import SystemUser
from assets.serializers import SystemUserSerializer
from common.mixins import IDInFilterMixin
from users.permissions import IsSuperUser


__all__ = ['SystemUserViewSet']


class SystemUserViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = SystemUser.objects.all()
    serializer_class = SystemUserSerializer
    permission_classes = (IsSuperUser,)