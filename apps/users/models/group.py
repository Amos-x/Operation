# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 14:50
#   FileName = group

import uuid
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ['UserGroup']


class UserGroup(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=64, unique=True, verbose_name=_('Group'))
    comment = models.TextField(blank=True, null=True, verbose_name=_("Comment"))
    date_created = models.DateTimeField(auto_now_add=True, null=True, verbose_name=_("Date created"))
    create_by = models.CharField(max_length=128, null=True, blank=True, verbose_name=_("Create by"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'users_usergroup'
        ordering = ['name']
        verbose_name = _('User Group')

    @classmethod
    def initial(cls):
        """ 初始化默认用户组 """
        default_group = cls.objects.filter(name='Default')
        if not default_group:
            group = cls(name='Default', create_by='System', comment='Default user group')
            group.save()
        else:
            group = default_group[0]
        return group
