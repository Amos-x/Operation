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

    # users
    path('list/', UserListView.as_view(), name='user-list'),

    # user group
    path('user-group/', UserGroupListView.as_view(), name='user-group-list'),
    path('user-group/create/', UserGroupCreateView.as_view(), name='user-group-create'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/$', UserGroupDetailView.as_view(), name='user-group-detail'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/update/$', UserGroupUpdateView.as_view(), name='user-group-update'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/delete/$', UserGroupDeleteView.as_view(), name='user-group-delete'),
    re_path(r'^user-group/(?P<pk>[0-9a-zA-Z\-]{36})/asstes/$', UserGroupGrantedAssetView.as_view(), name='user-group-granted-asset'),

]
