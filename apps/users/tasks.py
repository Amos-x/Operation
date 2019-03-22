# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-21 19:49
#   FileName = tasks


from celery import shared_task
from users.utils import write_login_log


@shared_task
def write_login_log_async(*args, **kwargs):
    write_login_log(*args, **kwargs)
