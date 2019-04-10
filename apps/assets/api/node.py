# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-04 10:52
#   FileName = node

from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, CreateAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework_bulk import BulkModelViewSet, BulkListSerializer
from common.mixins import IDInFilterMixin
from users.permissions import IsSuperUser
from assets.models import Node
from assets.serializers import NodeSerializers


class NodeViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = Node.objects.all()
    serializer_class = NodeSerializers
    permission_classes = (IsSuperUser,)
    pagination_class = LimitOffsetPagination


class NodeChildrenCreateApi(CreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializers
    permission_classes = (IsSuperUser,)

    def post(self, request, *args, **kwargs):
        if not request.data.get("value"):
            request.data["value"] = _("New node {}").format(self.get_object().child_mark)
        return super().post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        value = request.data.get('value')
        values = [child.value for child in instance.get_children()]
        if value in values:
            raise ValidationError(
                'The same level node name cannot be the same'
            )
        node = instance.create_child(value=value)
        return Response({
            'id': node.id,
            'key': node.key,
            'value': node.value
        }, status.HTTP_201_CREATED)


class NodeChildrenApi(ListCreateAPIView):
    queryset = Node.objects.all()
    serializer_class = NodeSerializers
    permission_classes = (IsSuperUser,)

    def post(self, request, *args, **kwargs):
        if not request.data.get('value'):
            request.data['value'] = _('new node {}'.format(self.get_object().child_mark))
        return super().post(request, *args, **kwargs)

