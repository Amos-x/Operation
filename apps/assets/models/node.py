# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019/2/25 3:39 PM
#   FileName = nodes

import uuid
from django.db import models, transaction
from django.utils.translation import ugettext_lazy as _
from django.db.models import Q


__all__ = ['Node']


class Node(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    key = models.CharField(unique=True, max_length=64, verbose_name=_('Key'))  # 内容如：1:1:1:1
    value = models.CharField(max_length=128, verbose_name=_('Value'))
    child_mark = models.IntegerField(default=0)  # node下
    date_create = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))

    is_node = True
    # _assets_amount = None
    # _full_value_cache_key = '_NODE_VALUE_{}'
    # _assets_amount_cache_key = '_NODE_ASSETS_AMOUNT_{}'

    class Meta:
        db_table = 'assets_node'
        verbose_name = _('Node')

    def __str__(self):
        return self.full_value

    def __eq__(self, other):
        if not other:
            return False
        return self.key == other.key

    def __gt__(self, other):
        """
        判断节点的大小，越短，则节点越大，所以重写__gt__方法，最后 return self_key.__lt__(other_key)
        跟正常的列表比大小正好相反
        """
        if self.is_root():
            return True
        self_key = [int(key) for key in self.key.split(':')]
        other_key = [int(key) for key in other.key.split(':')]
        return self_key.__lt__(other_key)

    def __lt__(self, other):
        return not self.__gt__(other)

    def is_root(self):
        """
        isdigit 检查字符串是否全由数字组成，是则返回True，反之则否
        判断 node 是否是根节点
        """
        if self.key.isdigit():
            return True
        else:
            return False

    @property
    def name(self):
        """ 返回 node 名 等于 value"""
        return self.value

    def get_all_assets(self):
        """ 返回 node 下所有 asset"""
        from .asset import Asset
        if self.is_root():
            assets = Asset.objects.all()
        else:
            pattern = r'^{0}$|^{0}:'.format(self.key)
            assets = Asset.objects.filter(nodes__key__regex=pattern)
        return assets

    def get_all_vaild_assets(self):
        return self.get_all_assets().valid()

    def get_assets(self):
        from .asset import Asset
        if self.is_root():
            assets = Asset.objects.filter(Q(node__id=self.id) | Q(nodes__isnull=True))
        else:
            assets = self.node_assets.all()
        return assets

    def get_valid_assets(self):
        return self.get_assets().valid()

    # @property
    # def assets_amount(self):
    #     """ 返回 node 下 asset 的数量"""
    #     if self._assets_amount is not None:
    #         return self._assets_amount
    #     cache_key = self._assets_amount_cache_key.format(self.key)
    #     cached = cache.get(cache_key)
    #     if cached is not None:
    #         return cached
    #     assets_amount = self.get_all_assets().count()
    #     cache.set(cache_key,assets_amount,3600)
    #
    # @assets_amount.setter
    # def assets_amount(self, value):
    #     """ 设置 node 下 asset 的数量"""
    #     self._assets_amount = value

    @property
    def level(self):
        """ 返回 node 等级"""
        return len(self.key.split(":"))

    @classmethod
    def root(cls):
        """ 返回根节点"""
        obj,created = cls.objects.get_or_create(key='1', defaults={'key': '1', 'value': 'Default'})
        print(obj)
        return obj

    @property
    def full_value(self):
        """ 返回全名，从根节点到本身的 全称"""
        if self.is_root():
            return self.value
        ancestor = [a.value for a in self.get_ancestor(with_self=True)]
        return ' / '.join(ancestor)

    def get_ancestor(self,with_self=False):
        """ 返回 所有祖先节点 """
        if self.is_root():
            ancestor = self.__class__.objects.filter(key='1')
            return ancestor

        _key = self.key.split(':')
        if not with_self:
            _key.pop()
        ancestor_keys = []
        for i in range(len(_key)):
            ancestor_keys.append(':'.join(_key))
            _key.pop()
        ancestor = self.__class__.objects.filter(key__in=ancestor_keys).order_by('key')
        return ancestor

    def get_next_child_key(self):
        """ 返回下一个子节点的 key """
        mark = self.child_mark
        self.child_mark += 1
        self.save()
        return "{}:{}".format(self.key, mark)

    def create_child(self, value):
        """ 创建子节点， 返回子节点实例"""
        with transaction.atomic():
            child_key = self.get_next_child_key()
            child = self.__class__.objects.create(key=child_key, value=value)
            return child

    def get_children(self, with_self=False):
        """ 返回节点下的所有子节点，仅子节点，不包括孙节点等后面节点 """
        pattern = r'^{0}$|^{0}:[0-9]+$' if with_self else r'^{0}:[0-9]+$'
        return self.__class__.objects.filter(key__regex=pattern.format(self.key))

    def get_all_children(self, with_self=False):
        """ 返回节点下的所有低于此节点的子孙节点 """
        pattern = r'^{0]$|^{0}:' if with_self else r'^{0}:'
        return self.__class__.objects.filter(key__regex=pattern.format(self.key))

    def get_sibling(self, with_self=False):
        """ 返回兄弟节点 """
        key = ':'.join(self.key.split(":")[:-1])
        pattern = r'^{}:[0-9]+$'.format(key)
        sibling = self.__class__.objects.filter(key__regex=pattern)
        if not with_self:
            sibling = sibling.exclude(key=self.key)
        return sibling

    def get_family(self):
        """ 返回整个相关的节点，所有祖先节点和所有子孙节点 """
        ancestor = self.get_ancestor()
        children = self.get_all_children()
        return [*tuple(ancestor), self, *tuple(children)]

    @property
    def parent(self):
        """ 返回父节点 """
        if self.is_root():
            return self.__class__.root()
        parttern_key = ':'.join(self.key.split(':')[:-1])
        try:
            parent = self.__class__.objects.get(key=parttern_key)
            return parent
        except Node.DoesNotExist:
            return self.__class__.root()

    @parent.setter
    def parent(self, parent):
        """ 设置父节点，用于节点迁移 """
        if self.is_node:
            children = self.get_all_children()
            old_key = self.key
            with transaction.atomic():
                self.key = parent.get_next_child_key()
                for child in children:
                    child.key = child.key.replace(old_key, self.key, 1)
                    child.save()
                self.save()
        else:
            self.key = parent.key + ':fake'

    @parent.setter
    def parent(self, parent):
        if self.is_node:
            children = self.get_all_children()
            old_key = self.key
            with transaction.atomic():
                self.key = parent.get_next_child_key()
                for child in children:
                    child.key = child.key.replace(old_key, self.key, 1)
                    child.save()
                self.save()
        else:
            self.key = parent.key + ':fake'
