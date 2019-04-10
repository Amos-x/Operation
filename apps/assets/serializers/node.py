# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-04 10:57
#   FileName = Node

from rest_framework import serializers
from rest_framework_bulk import BulkSerializerMixin, BulkListSerializer
from assets.models import Node


class NodeSerializers(BulkSerializerMixin, serializers.ModelSerializer):
    parent = serializers.SerializerMethodField()
    assets_amount = serializers.SerializerMethodField()

    class Meta:
        model = Node
        list_serializer_class = BulkListSerializer
        fields = ['id', 'key', 'value', 'parent', 'is_node', 'assets_amount']

    def get_parent(self, obj):
        """ 对于假节点来说，返回parent_id 属性，生产假节点时需要赋值 """
        return obj.parent.id if obj.is_node else obj.parent_id

    def get_assets_amount(self, obj):
        """ 返回节点下所有资产数量，包括子孙节点 """
        return obj.get_all_assets.count() if obj.is_node else 0

    def get_fields(self):
        fields = super().get_fields()
        field = fields.get('key')
        field.required = False
        return fields
