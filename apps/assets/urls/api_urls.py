# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-03 00:02
#   FileName = api_urls

from django.urls import path, re_path
from rest_framework_bulk.routes import BulkRouter
from assets.api import *


app_name = 'assets'


router = BulkRouter()
router.register('v1/asset', AssetViewSet, 'asset')
router.register('v1/node', NodeViewSet, 'node')
router.register('v1/admin_user', AdminUserViewSet, 'admin-user')
router.register('v1/system_user', SystemUserViewSet, 'system-user')
router.register('v1/label', LabelViewSet, 'label')
router.register('v1/domain', DomainViewSet, 'domain')
router.register('v1/gateway', GatewayViewSet, 'gateway')

urlpatterns = [
    re_path(r'^v1/nodes/(?P<pk>[0-9a-zA-Z\-]{36})/children/$', NodeChildrenCreateApi, 'node-children-create')
]

urlpatterns += router.urls
