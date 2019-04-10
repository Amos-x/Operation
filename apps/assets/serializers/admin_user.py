# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-07 00:50
#   FileName = admin_user

from rest_framework import serializers
from assets.models import AdminUser


__all__ = ['AdminUserSerializer']


class AdminUserSerializer(serializers.ModelSerializer):
    assets_amount = serializers.SerializerMethodField()
    reachable_amount = serializers.SerializerMethodField()    # 可达资产数量
    unreachable_amount = serializers.SerializerMethodField()    # 不可达资产数量

    class Meat:
        model = AdminUser
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        return [f for f in fields if not f.startswith('_')]

    def get_assets_amount(self, obj):
        return obj.assets_amount

    def get_reachable_amount(self, obj):
        return obj.reachable_amount

    def get_unreachable_amount(self, obj):
        return obj.unreachable_amount
