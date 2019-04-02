# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-29 15:17
#   FileName = serializers

from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer
from common.mixins import BulkSerializerMixin
from users.models import UserGroup, User


__all__ = ['UserSerializer', 'UserUpdateGroupSerializer', 'UserGroupUpdateUserSerializer', 'UserGroupSerializer']


class UserSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    groups_display = serializers.SerializerMethodField()
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=UserGroup.objects.all(), required=False)

    class Meta:
        model = User
        list_serializer_class = BulkListSerializer
        exclude = [
            'first_name', 'last_name', 'password', '_private_key',
            '_public_key', 'user_permissions'
        ]

    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)
        fields.extend([
            'groups_display', 'get_role_display', 'is_valid'
        ])
        return fields

    @staticmethod
    def get_groups_display(obj):
        return ' '.join([group.name for group in obj.groups.all()])


class UserGroupSerializer(BulkSerializerMixin, serializers.ModelSerializer):
    users = serializers.SerializerMethodField()

    class Meta:
        model = UserGroup
        list_serializers_class = BulkListSerializer
        fields = '__all__'

    def get_users(self, obj):
        return [user.name for user in obj.users.all()]


class UserUpdateGroupSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=UserGroup.objects.all())

    class Meta:
        model = User
        fields = ['id', 'groups']


class UserGroupUpdateUserSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(many=True, queryset=User.objects.all())

    class Meta:
        model = UserGroup
        fields = ['id', 'users']
