# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-01 11:28
#   FileName = api_urls

from django.urls import re_path
from rest_framework_bulk.routes import BulkRouter
from users.api import *


app_name = 'users'

router = BulkRouter()
router.register('v1/users', UserViewSet, 'user')
router.register('v1/groups', UserGroupViewSet, 'user-group')


urlpatterns = [
    re_path(r'^v1/users/(?P<pk>[0-9a-zA-Z\-]{36})/password/reset/$', UserSendMailRestPasswordAPI.as_view(), name='user-reset-password'),
    re_path(r'^v1/users/(?P<pk>[0-9a-zA-Z\-]{36})/pubkey/reset/$', UserSendMailRestPKAPI.as_view(), name='user-public-key-reset'),
    re_path(r'^v1/users/(?P<pk>[0-9a-zA-Z\-]{36})/unblock/$', UserUnblockLoginApi.as_view(), name='user-unblock'),
    re_path(r'^v1/users/(?P<pk>[0-9a-zA-Z\-]{36})/groups/$', UserUpdateGroupApi.as_view(), name='user-update-group'),
    re_path(r'^v1/groups/(?P<pk>[0-9a-zA-Z\-]{36})/users/$', UserGroupUpdateUserApi.as_view(), name='user-group-update-user'),
]

urlpatterns += router.urls
