# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-15 19:04
#   FileName = tasks

from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from celery import shared_task
from common.utils import get_logger
from common.models import Setting


logger = get_logger(__file__)


@shared_task
def send_email_async(*args, **kwargs):
    """
    使用celery消息队列，异步发送邮件

    Example:
    send_mail_async.delay(subject, message, from_mail, recipient_list, fail_silently=False, html_message=None)

    Also you can ignore the from_mail, unlike django send_mail, from_email is not a require args:

    Example:
    send_mail_async.delay(subject, message, recipient_list, fail_silently=False, html_message=None)
    """
    configs = Setting.objects.filter(name__startswith="EMAIL")
    for config in configs:
        setattr(settings, config.name, config.cleaned_value)

    if len(args) == 3:
        args = list(args)
        args[0] = settings.EMAIL_SUBJECT_PREFIX + args[0]
        args.insert(2, settings.EMAIL_HOST_USER)
        args = tuple(args)

    try:
        send_mail(*args, **kwargs)
    except Exception as e:
        logger.error("Send mail error: {}".format(e))






