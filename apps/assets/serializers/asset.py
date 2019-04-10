# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-03 00:19
#   FileName = asset

from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer, BulkSerializerMixin
from assets.models import Asset


__all__ = ['AssetSerializers']


class AssetSerializers(BulkSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = Asset
        list_serializer_class = BulkListSerializer
        fields = '__all__'
        # TODO: 这里不明白为什么需要加下面这句
        validators = []  # If not set to [], partial bulk update will be error

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend([
            'hardware_info', 'is_connective'
        ])
        return fields


