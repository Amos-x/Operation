# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-28 19:32
#   FileName = user

import logging
from .base import AssetUser
from common.utils import get_signer
from assets.constant import SYSTEM_USER_CONN_CACHE_KEY
from django.db import models
from django.core.cache import cache
from django.utils.translation import ugettext_lazy as _


__all__ = ['AdminUser', 'SystemUser']
logger = logging.getLogger(__name__)
signer = get_signer()


class AdminUser(AssetUser):
    """ 管理用户，对资产的管理和系统用户的推送设置等都需要使用管理用户，推荐是root用户 """
    BECOME_METHOD_CHOICES = (
        ('sudo', 'sudo'),
        ('su', 'su'),
    )
    become = models.BooleanField(default=True)
    become_method = models.CharField(choices=BECOME_METHOD_CHOICES, default='sudo', max_length=8)
    become_user = models.CharField(default='root', max_length=64)
    _become_pass = models.CharField(default='', max_length=128)

    class Meta:
        ordering = ['name']
        db_table = 'assets_adminuser'
        verbose_name = _('Admin user')

    def __str__(self):
        return self.name

    @property
    def become_pass(self):
        if self._become_pass:
            return signer.unsign(self._become_pass)
        else:
            return None

    @become_pass.setter
    def become_pass(self, password_raw):
        self._become_pass = signer.sign(password_raw)

    def get_related_assets(self):
        """ 获取此管理用户下的所有资产 """
        return self.asset_set.all()

    @property
    def assets_amount(self):
        """ 返回此管理用户下所有资产的数量 """
        return self.get_related_assets().count()


class SystemUser(AssetUser):
    SSH_PROTOCOL = 'ssh'
    RDP_PROTOCOL = 'rdp'
    TELNET_PROTOCOL = 'telnet'
    PROTOCOL_CHOICES = (
        (SSH_PROTOCOL, 'ssh'),
        (RDP_PROTOCOL, 'rdp'),
        (TELNET_PROTOCOL, 'telnet (beta)'),
    )
    AUTO_LOGIN = 'auto'
    MANUAL_LOGIN = 'manual'
    LOGIN_MODE_CHOICES = (
        (AUTO_LOGIN, _('Automatic login')),
        (MANUAL_LOGIN, _('Manually login'))
    )

    nodes = models.ManyToManyField('assets.Node', blank=True, verbose_name=_('Nodes'))
    assets = models.ManyToManyField('assets.Asset', blank=True, verbose_name=_('Assets'))
    priority = models.IntegerField(default=10, verbose_name=_('Priority'))  # 优先度
    protocol = models.CharField(max_length=16, choices=PROTOCOL_CHOICES, default='ssh', verbose_name=_('Protocol'))
    auto_push = models.BooleanField(default=True, verbose_name=_("Auto push"))
    sudo = models.TextField(default='/bin/whoami', verbose_name=_('Sudo'))
    shell = models.CharField(max_length=64, default='/bin/bash', verbose_name=_('Shell'))
    login_Mode = models.CharField(choices=LOGIN_MODE_CHOICES, default=AUTO_LOGIN, max_length=16, verbose_name=_('Login mode'))

    def __str__(self):
        return '{0}({1})'.format(self.name, self.username)

    class Meta:
        db_table = 'assets_systemuser'
        ordering = ['name']
        verbose_name = _("System user")

    def get_assets(self):
        """ 返回系统用户的所有资产 """
        return set(self.assets.all())

    @property
    def assets_connective(self):
        """ 从缓存中获取系统用户所有相关的资产的连接信息 """
        _result = cache.get(SYSTEM_USER_CONN_CACHE_KEY.format(self.name), {})
        return _result

    @property
    def reachable_assets(self):
        """ 获取连接中可连接的资产 """
        return self.assets_connective.get('contacted', [])

    @property
    def unreachable_assets(self):
        """ 获取连接中不可连接的资产的列表"""
        return list(self.assets_connective.get('dark', {}.keys()))

    def is_need_push(self):
        """ 判断是否需要主动推送此系统用户，返回True or False"""
        if self.auto_push and self.protocol == self.__class__.SSH_PROTOCOL:
            return True
        else:
            return False

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'protocol': self.protocol,
            'priority': self.priority,
            'auto_push': self.auto_push,
        }
