# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 11:23
#   FileName = label

from rest_framework_bulk import BulkListSerializer
from rest_framework import serializers
from assets.models import Label

__all__ = ['LabelSerializer']


class LabelSerializer(serializers.ModelSerializer):
    asset_count = serializers.SerializerMethodField()

    class Meta:
        model = Label
        fields = '__all__'
        list_serializer_class = BulkListSerializer

    def get_asset_count(self, obj):
        return obj.label_assets.count()
