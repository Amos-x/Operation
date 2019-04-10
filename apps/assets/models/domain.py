# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-27 17:31
#   FileName = domain

import uuid
import random
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .base import AssetUser


__all__ = ['Domain', 'Gateway']


class Domain(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Name'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'assets_domain'
        verbose_name = _('Domain')

    def has_gateway(self):
        return self.gateway_set.filter(is_active=True).exists()

    @property
    def gateways(self):
        """ 返回所有可用的网关 """
        return self.gateway_set.filter(is_active=True)

    def random_gateway(self):
        """ 返回一个随机网关 """
        return random.choice(self.gateways)


class Gateway(AssetUser):
    SSH_PROTOCOL = 'ssh'
    RDP_PROTOCOL = 'rdp'
    PROTOCOL_CHOICES = (
        (SSH_PROTOCOL, 'ssh'),
        (RDP_PROTOCOL, 'rdp'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ip = models.GenericIPAddressField(max_length=32, verbose_name=_('IP'), db_index=True)
    port = models.IntegerField(default=22, verbose_name=_('Port'))
    protocol = models.CharField(max_length=16, choices=PROTOCOL_CHOICES, default=SSH_PROTOCOL, verbose_name=_('Protocol'))
    domain = models.ForeignKey(Domain, verbose_name=_('Domain'), on_delete=models.CASCADE)
    comment = models.TextField(blank=True, null=True, verbose_name=_('Comment'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

    def __str__(self):
        return self.name
