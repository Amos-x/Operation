# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 17:02
#   FileName = authentication

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ['LoginLog']


class LoginLog(models.Model):
    LOGIN_TYPE_CHOICES = (
        ('T', _('Terminal')),
        ('W', _('Web')),
    )
    LOGIN_STATUS_CHOICES = (
        (0, _('Success')),
        (1, _('Username/password check failed')),
        (2, _('Public key check failed')),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    username = models.CharField(max_length=128, verbose_name=_('Username'))
    type = models.CharField(choices=LOGIN_TYPE_CHOICES, max_length=2, verbose_name=_('Login type'))
    ip = models.GenericIPAddressField(verbose_name=_("Login ip"))
    city = models.CharField(max_length=64, verbose_name=_('Login city'), blank=True, null=True)
    user_agent = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("User agent"))
    status = models.SmallIntegerField(choices=LOGIN_STATUS_CHOICES, default=0, verbose_name=_('Login status'))
    datetime = models.DateTimeField(auto_now_add=True, verbose_name=_('Date login'))

    class Meta:
        db_table = 'users_loginlog'
        ordering = ['-datetime']
        verbose_name = _('Login log')
