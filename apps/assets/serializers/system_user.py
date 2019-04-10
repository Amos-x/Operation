# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 10:54
#   FileName = system_user

from rest_framework import serializers
from assets.models import SystemUser

__all__ = ['SystemUserSerializer']


class SystemUserSerializer(serializers.ModelSerializer):
    assets_amount = serializers.SerializerMethodField()
    reachable_amount = serializers.SerializerMethodField()
    unreachable_amount = serializers.SerializerMethodField()

    class Meta:
        model = SystemUser
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend([
            'get_login_mode_display'
        ])
        return [f for f in fields if not f.startswith('_')]

    def get_assets_amount(self, obj):
        return len(obj.get_assets())

    def get_reachable_amount(self, obj):
        return len(obj.reachable_assets)

    def get_unreachable_assets(self, obj):
        return len(obj.unreachable_assets)
