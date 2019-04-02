# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-29 19:15
#   FileName = user

from django.core.cache import cache
from rest_framework.generics import UpdateAPIView, RetrieveUpdateAPIView
from rest_framework_bulk import BulkModelViewSet
from users.permissions import IsSuperUser
from users.models import User, UserGroup
from users.serializers import UserSerializer, UserUpdateGroupSerializer, UserGroupUpdateUserSerializer, UserGroupSerializer
from users.utils import send_reset_password_mail, send_reset_ssh_key_mail
from common.mixins import IDInFilterMixin


__all__ = ['UserSendMailRestPasswordAPI', 'UserSendMailRestPKAPI', 'UserUnblockLoginApi', 'UserUpdateGroupApi',
           'UserGroupUpdateUserApi', 'UserViewSet', 'UserGroupViewSet']


class UserSendMailRestPasswordAPI(UpdateAPIView):
    """ 发送重置密码邮件 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)

    def perform_update(self, serializer):
        user = self.get_object()
        send_reset_password_mail(user)


class UserSendMailRestPKAPI(UpdateAPIView):
    """ 重置用户公钥为空，并发送邮件提醒用户重新设置公钥 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)

    def perform_update(self, serializer):
        user = self.get_object()
        user.is_public_key_valid = False
        user.save()
        send_reset_ssh_key_mail(user)


class UserUnblockLoginApi(UpdateAPIView):
    """ 解除用户登录限制的api接口 """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
    key_prefix_limit = "_LOGIN_LIMIT_{}_{}"  # 缓存key，个人用户登录次数限制的key，后跟username+ip
    key_prefix_block = "_LOGIN_BLOCK_{}"  # 缓存key，是否已限制用户登录，后跟username

    def perform_update(self, serializer):
        user = self.get_object()
        username = user.username if user else ''
        cache.delete(self.key_prefix_block.format(username))
        cache.delete_pattern(self.key_prefix_limit.format(username, '*'))


class UserUpdateGroupApi(RetrieveUpdateAPIView):
    """ 用户更新用户组的接口 """
    queryset = User.objects.all()
    serializer_class = UserUpdateGroupSerializer
    permission_classes = (IsSuperUser,)


class UserGroupUpdateUserApi(RetrieveUpdateAPIView):
    """ 用户组更新用户接口 """
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupUpdateUserSerializer
    permission_classes = (IsSuperUser,)


class UserViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = User.objects.exclude(role=User.ROLE_APP)
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)
    filter_fields = ('username', 'email', 'name', 'id')


class UserGroupViewSet(IDInFilterMixin, BulkModelViewSet):
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    permission_classes = (IsSuperUser,)
