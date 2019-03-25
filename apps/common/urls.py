# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-09 19:00
#   FileName = urls

from django.urls import path
from common.views import *


app_name = 'common'


urlpatterns = [
    path('basic-setting/', BasicSettingView.as_view(), name='basic-setting'),
    path('email-setting/', EmailSettingView.as_view(), name='email-setting'),
    path('security-setting/', SecuritySettingView.as_view(), name='security-setting'),
]