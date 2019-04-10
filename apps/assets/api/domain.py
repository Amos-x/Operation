# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 11:35
#   FileName = domain

from rest_framework_bulk import BulkModelViewSet
from common.mixins import IDInFilterMixin
from assets.models import Domain, Gateway
from users.permissions import IsSuperUser
from assets.serializers import DomainSerializer, GatewaySerializer

__all__ = ['DomainViewSet', 'GatewayViewSet']


class DomainViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = Domain.objects.all()
    serializer_class = DomainSerializer
    permission_classes = (IsSuperUser,)


class GatewayViewSet(IDInFilterMixin, BulkModelViewSet):
    # search_fields =
    queryset = Gateway.objects.all()
    serializer_class = GatewaySerializer
    permission_classes = (IsSuperUser,)
