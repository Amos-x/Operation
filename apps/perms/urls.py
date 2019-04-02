# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-25 16:50
#   FileName = urls

from django.urls import path
from perms import views

app_name = 'perms'


urlpatterns = [
    path('asset-permission/', views.AssetPermissionListView.as_view(), name='asset-permission-list'),
    # path(r'^asset-permission/create/$', views.AssetPermissionCreateView.as_view(), name='asset-permission-create'),
    # path(r'^asset-permission/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.AssetPermissionUpdateView.as_view(), name='asset-permission-update'),
    # path(r'^asset-permission/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.AssetPermissionDetailView.as_view(),name='asset-permission-detail'),
    # path(r'^asset-permission/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.AssetPermissionDeleteView.as_view(), name='asset-permission-delete'),
    # path(r'^asset-permission/(?P<pk>[0-9a-zA-Z\-]{36})/user/$', views.AssetPermissionUserView.as_view(), name='asset-permission-user-list'),
    # path(r'^asset-permission/(?P<pk>[0-9a-zA-Z\-]{36})/asset/$', views.AssetPermissionAssetView.as_view(), name='asset-permission-asset-list'),
]
