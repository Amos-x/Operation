# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019/2/24 4:08 PM
#   FileName = assets

import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache
from assets.constant import ASSET_ADMIN_CONN_CACHE_KEY


__all__ = ['Asset']
logger = logging.getLogger(__name__)


def default_node():
    try:
        from .node import Node
        root = Node.root()
        return root
    except:
        return None


class AssetQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def valid(self):
        return self.active()


class AssetManager(models.Manager):
    def get_queryset(self):
        return AssetQuerySet(self.model, using=self._db)


class Asset(models.Model):
    PLATFORM_CHOICES = (
        ('Linux', 'Linux'),
        ('Unix', 'Unix'),
        ('MacOS', 'MacOS'),
        ('BSD', 'BSD'),
        ('Windows', 'Windows'),
        ('Windows2016', 'Windows(2016)'),
        ('Other', 'Other'),
    )

    PROTOCOL_SSH = 'ssh'
    PROTOCOL_RDP = 'rdp'
    PROTOCOL_TELNET = 'telnet'
    PROTOCOL_VNC = 'vnc'
    PROTOCOL_CHOICES = (
        (PROTOCOL_SSH, 'ssh'),
        (PROTOCOL_RDP, 'rdp'),
        (PROTOCOL_TELNET, 'telnet (beta)'),
        (PROTOCOL_VNC, 'vnc'),
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    ip = models.GenericIPAddressField(max_length=32, verbose_name=_('IP'), db_index=True)
    # 主机名，可自定义的名称
    hostname = models.CharField(max_length=128, verbose_name=_('Hostname'))
    protocol = models.CharField(max_length=128, default=PROTOCOL_SSH, choices=PROTOCOL_CHOICES, verbose_name=_('Protocol'))
    port = models.IntegerField(default=22, verbose_name=_('Port'))
    is_active = models.BooleanField(default=True, verbose_name=_('Is active'))

    # 系统平台
    platform = models.CharField(max_length=128, default='Linux', choices=PLATFORM_CHOICES, verbose_name=_('Platform'))

    # 网域
    domain = models.ForeignKey("assets.Domain", null=True, blank=True, related_name='domain_assets', verbose_name=_('Domain'), on_delete=models.SET_NULL)

    # 节点
    nodes = models.ManyToManyField("assets.Node", default=default_node, related_name='node_assets', verbose_name=_('Nodes'))

    # Auth
    admin_user = models.ForeignKey('assets.AdminUser', on_delete=models.PROTECT, null=True, verbose_name=_("Admin user"))

    # 公网ip
    public_ip = models.GenericIPAddressField(max_length=32, blank=True, null=True, verbose_name=_('Public IP'))

    # 资产编号
    number = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('Asset number'))

    # 制造商
    vendor = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Vendor'))

    # 型号
    model = models.CharField(max_length=54, null=True, blank=True, verbose_name=_('Model'))

    # SN序列号
    sn = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Serial number'))

    # cpu 信息
    # cpu 型号
    cpu_model = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('CPU model'))
    # cpu 单核线程数
    cpu_count = models.IntegerField(null=True, verbose_name=_('CPU count'))
    # cpu 物理核心数
    cpu_cores = models.IntegerField(null=True, verbose_name=_('CPU cores'))
    # cpu 逻辑核心数 = cpu物理核心数 * cpu线程数 即cpu_count * cpu_cores
    cpu_vcpus = models.IntegerField(null=True, verbose_name=_('CPU vcpus'))

    # 内存
    memory = models.CharField(max_length=64, null=True, blank=True, verbose_name=_('Memory'))

    # 磁盘总容量
    disk_total = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_('Disk total'))
    # 磁盘完整信息
    disk_info = models.CharField(max_length=1024, null=True, blank=True, verbose_name=_('Disk info'))

    # 系统
    os = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('OS'))
    os_version = models.CharField(max_length=16, null=True, blank=True, verbose_name=_('OS version'))
    # 系统架构，如：X86_64
    os_arch = models.CharField(max_length=16, blank=True, null=True, verbose_name=_('OS arch'))
    # 系统hostname
    hostname_raw = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Hostname raw'))

    # 标签
    labels = models.ManyToManyField('assets.Label', blank=True, related_name='label_assets', verbose_name=_('Labels'))

    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))

    # 备注,说明
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))

    # 指定objects，使得objects的方法能重写
    objects = AssetManager()

    def __str__(self):
        return '{0.hostname}({0.ip})'.format(self)

    class Meta:
        db_table = 'assets_asset'
        verbose_name = _('Asset')

    @property
    def is_valid(self):
        "表单验证"
        warning = ''
        if not self.is_active:
            warning += ' inactive'
        else:
            return True, ''
        return False, warning

    def support_ansible(self):
        "是否支持ansible"
        if self.platform in ("Windows", "Windows2016", "Other"):
            return False
        if self.protocol != 'ssh':
            return False
        return True

    def is_unixlike(self):
        "是否是unix系统"
        if self.platform not in ("Windows", "Windows2016"):
            return True
        else:
            return False

    def get_nodes(self):
        from .node import Node
        nodes = self.nodes.all() or [Node.root()]
        return nodes

    @property
    def hardware_info(self):
        if self.cpu_count:
            return '{} Core {} {}'.format(self.cpu_vcpus or self.cpu_count * self.cpu_cores, self.memoryl, self.disk_total)
        else:
            return ''

    @property
    def is_connective(self):
        """ 判断是否可连接,通过带id的缓存key来判断 """
        if not self.is_unixlike():
            return True
        val = cache.get(ASSET_ADMIN_CONN_CACHE_KEY.format(self.id))
        if val == 1:
            return True
        else:
            return False
