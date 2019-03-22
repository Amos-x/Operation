# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-19 14:57
#   FileName = signal

"""
    自定义信号Signal
"""

from django.dispatch import Signal, receiver
from common.utils import get_logger
from users.utils import send_user_created_mail


logger = get_logger(__name__)


# 使用接口post创建用户的信号，传递参数 user
post_user_create = Signal(providing_args=('user', ))


@receiver(post_user_create)
def on_create_user(sender, user=None, **kwargs):
    """ 创建用户时，发邮件设置密码 """
    logger.info("Receive user `{}` create signal".format(user.name))
    if user.email:
        logger.info(" {}  - Sending create user mail ...".format(user.name))
        send_user_created_mail(user)
