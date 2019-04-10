# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-02 18:40
#   FileName = urls

from django.urls import path, re_path
from assets import views


app_name = 'assets'

urlpatterns = [
    # asset
    path('', views.AssetListView.as_view(), name='asset-list'),
    path('asset/create/', views.AssetCreateView.as_view(), name='asset-create'),
    re_path(r'^asset/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.AssetDetailView.as_view(), name='asset-detail'),
    re_path(r'^asset/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.AssetUpdateView.as_view(), name='asset-update'),
    re_path(r'^asset/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.AssetDeleteView.as_view(), name='asset-delete'),
    path('asset/updates/', views.AssetBulkUpdateView.as_view(), name='asset-bulk-update'),

    # assets import export
    path('asset/export/', views.AssetExportView.as_view(), name='asset-export'),
    path('asset/import/', views.BulkImportAssetView.as_view(), name='asset-import'),

    # user asset view
    path('user-asset/', views.UserAssetListView.as_view(), name='user-asset-list'),

    # admin user
    path('admin-user/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin-user/create/', views.AdminUserCreateView.as_view(), name='admin-user-create'),
    re_path(r'^admin-user/(?P<pk>[0-9a-zA-Z\-]{36})/$', views.AdminUserDetailView.as_view(), name='admin-user-detail'),
    re_path(r'^admin-user/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.AdminUserUpdateView.as_view(), name='admin-user-update'),
    re_path(r'^admin-user/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.AdminUserDeleteView.as_view(), name='admin-user-delete'),
    re_path(r'^admin-user/(?P<pk>[0-9a-zA-Z\-]{36})/assets/$', views.AdminUserAssetView.as_view(), name='admin-user-asset'),

    # system user
    path('system-user/', views.SystemUserListView.as_view(), name='system-user-list'),
    path('system-user/create/', views.SystemUserCreateView.as_view(), name='system-user-create'),
    re_path(r'system-user/(?P<pk>[0-9a-zA-Z\-]{36})/', views.SystemUserDetailView.as_view(), name='system-user-detail'),
    re_path(r'system-user/(?P<pk>[0-9a-zA-Z\-]{36})/create/', views.SystemUserCreateView.as_view(), name='system-user-create'),
    re_path(r'system-user/(?P<pk>[0-9a-zA-Z\-]{36})/update/', views.SystemUserUpdateView.as_view(), name='system-user-update'),
    re_path(r'system-user/(?P<pk>[0-9a-zA-Z\-]{36})/delete/', views.SystemUserDetailView.as_view(), name='system-user-delete'),
    re_path(r'system-user/(?P<pk>[0-9a-zA-Z\-]{36})/assets/', views.SystemUserAssetView.as_view(), name='system-user-asset'),

    # label
    path('label/', views.LabelListView.as_view(), name='label-list'),
    path('label/create/', views.LabelCreateView.as_view(), name='label-create'),
    re_path(r'label/(?P<pk>[0-9a-zA-Z\-]{36})/update/', views.LabelUpdateView.as_view(), name='label-update'),
    re_path(r'label/(?P<pk>[0-9a-zA-Z\-]{36})/delete/', views.LabelDeleteView.as_view(), name='label-delete'),


    # doamin
    path('domain/', views.DomainListView.as_view(), name='domain-list'),
    path('domain/create/', views.DomainCreateView.as_view(), name='domain-create'),
    re_path(r'domain/(?P<pk>[0-9a-zA-Z\-]{36})/', views.DomainDetailView.as_view(), name='domain-detail'),
    re_path(r'domain/(?P<pk>[0-9a-zA-Z\-]{36})/update/', views.DomainUpdateView.as_view(), name='domain-update'),
    re_path(r'domain/(?P<pk>[0-9a-zA-Z\-]{36})/delete/', views.DomainDeleteView.as_view(), name='domain-delete'),

    # gateway
    re_path(r'^domain/(?P<pk>[0-9a-zA-Z\-]{36})/gateway/$', views.DomainGatewayListView.as_view(), name='domain-gateway-list'),
    re_path(r'^domain/(?P<pk>[0-9a-zA-Z\-]{36})/gateway/create/$', views.DomainGatewayCreateView.as_view(), name='domain-gateway-create'),
    re_path(r'^domain/gateway/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', views.DomainGatewayUpdateView.as_view(), name='domain-gateway-update'),
    re_path(r'^domain/gateway/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', views.DomainGatewayDeleteView.as_view(), name='domain-gateway-delete'),
]
