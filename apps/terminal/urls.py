# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-25 17:29
#   FileName = urls

from django.urls import path
from terminal.views import *

app_name = 'perms'


urlpatterns = [
    path(r'session-online/', SessionOnlineListView.as_view(), name='session-online-list'),

]
