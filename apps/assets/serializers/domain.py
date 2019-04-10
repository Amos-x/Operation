# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 11:37
#   FileName = domain

from rest_framework import serializers
from assets.models import Domain, Gateway

__all__ = ['DomainSerializer', 'GatewaySerializer']


class DomainSerializer(serializers.ModelSerializer):
    assets_amount = serializers.SerializerMethodField()
    gateways_amount = serializers.SerializerMethodField()

    class Meta:
        model = Domain
        fields = '__all__'

    def get_assets_amount(self, obj):
        return obj.domain_assets.count()

    def get_gateways_amount(self, obj):
        return obj.gateways.count()


class GatewaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Gateway
        fields = '__all__'

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        return [f for f in fields if not f.startswith('_')]
