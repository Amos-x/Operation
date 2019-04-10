# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-03 00:08
#   FileName = assets

from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.generics import UpdateAPIView
from rest_framework_bulk import BulkModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from common.mixins import IDInFilterMixin
from assets.models import Asset, AdminUser, Node
from assets.serializers import AssetSerializers
from users.permissions import IsSuperUser


__all__ = ['AssetViewSet']


class AssetViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializers
    permission_classes = (IsSuperUser,)
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        """ 根据接口给请求后的传参来返回查询集 """
        queryset = super().get_queryset().select_related('domain', 'admin_user').prefetch_related('nodes', 'labels')
        admin_user_id = self.request.query_params.get('admin_user_id')
        node_id = self.request.query_params.get('node_id')
        show_current_asset = self.request.query_params.get('show_current_asset')

        if admin_user_id:
            admin_user = get_object_or_404(AdminUser, id=admin_user_id)
            queryset = queryset.filter(admin_user=admin_user)

        if node_id:
            node = get_object_or_404(Node, node_id)
            if show_current_asset:
                if node.is_root():
                    queryset = queryset.filter(Q(nodes=node_id) | Q(nodes__isnull=True))
                else:
                    queryset = queryset.filter(nodes=node_id).distinct()
            else:
                if node.is_root():
                    queryset = Asset.objects.all()
                else:
                    queryset = queryset.filter(nodes__key__regex='^{}(:[0-9]+)*$'.format(node.key)).distinct()

        return queryset
