# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 11:21
#   FileName = label

from rest_framework_bulk import BulkModelViewSet
from assets.models import Label
from assets.serializers import LabelSerializer
from common.mixins import IDInFilterMixin
from users.permissions import IsSuperUser

__all__ = ['LabelViewSet']


class LabelViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = Label.objects.all()
    serializer_class = LabelSerializer
    permission_classes = (IsSuperUser,)
