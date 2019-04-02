# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 14:14
#   FileName = urls

from django.urls import path, re_path
from users.views import *


app_name = 'users'


urlpatterns = [
    # login
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('password/reset/', UserResetPasswordView.as_view(), name='reset-password'),
    path('password/reset/success/', UserResetPasswordSuccessView.as_view(), name='reset-password-success'),
    path('password/forgot/', UserForgotPasswordView.as_view(), name='forgot-password'),
    path('password/forgot/sendmail-success/', UserForgotPasswordSuccessView.as_view(), name='forgot-password-sendmail-success'),

    # login-log
    path('login-log/', LoginLogListView.as_view(), name='login-log-list'),

    # User Profile Page
    path('user-profile/', UserProfileView.as_view(), name='user-profile'),
    path('user-profile/update/', UserProfileUpdateView.as_view(), name='user-profile-update'),
    path('user-profile/password/update/', UserPasswordUpdateView.as_view(), name='user-profile-password-update'),
    path('user-profile/publick-key/update/', UserPublicKeyUpdateView.as_view(), name='user-profile-pubkey-update'),
    path('user-profile/publick-key/generate/', UserPublicKeyGenerateView.as_view(), name='user-profile-pubkey-generate'),

    # users
    path('list/', UserListView.as_view(), name='user-list'),
    path('user/export/', UserExportView.as_view(), name='user-export'),
    path('user/import/', UserBulkImportView.as_view(), name='user-import'),
    path('user/create/', UserCreateView.as_view(), name='user-create'),
    path('user/update/', UserBulkUpdateView.as_view(), name='user-bulk-update'),
    re_path(r'^user/(?P<pk>[0-9a-zA-Z\-]{36})/$', UserDetailView.as_view(), name='user-detail'),
    re_path(r'^user/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', UserUpdateView.as_view(), name='user-update'),
    re_path(r'^user/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', UserDeleteView.as_view(), name='user-delete'),
    re_path(r'^user/(?P<pk>[0-9a-zA-Z\-]{36})/assets/$', UserGrantedAssetView.as_view(), name='user-granted-asset'),

    # user group
    path('user-group/', UserGroupListView.as_view(), name='user-group-list'),
    path('user-group/create/', UserGroupCreateView.as_view(), name='user-group-create'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/$', UserGroupDetailView.as_view(), name='user-group-detail'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', UserGroupUpdateView.as_view(), name='user-group-update'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', UserGroupDeleteView.as_view(), name='user-group-delete'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/asstes/$', UserGroupGrantedAssetView.as_view(), name='user-group-granted-asset'),

]
