# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司

from django.contrib.auth import get_user_model
from django.db import models


class Asset(models.Model):
    """
    资产总表
    """
    asset_typpe_choices = (
        ('server','服务器'),
        ('networkdevice','网络设备'),
        ('storagedevice','储存设备'),
        ('securitydevice','安全设备'),
        ('software','软件资产'),
        ('others','其他类'),
    )
    asset_type = models.CharField(choices=asset_typpe_choices,max_length=64,default='server')
    name = models.CharField('名称',max_length=100,unique=True)  # 如果是服务器或虚拟机，则名称为hostname。其余设备可以自定义名称
    sn = models.CharField('资产SN号',max_length=128,null=True,blank=True)
    contract = models.ForeignKey('Contract',verbose_name='合同',null=True,blank=True,on_delete=models.DO_NOTHING)
    trade_date = models.DateField('购买时间',null=True,blank=True)
    price = models.FloatField('价格',null=True,blank=True)
    expire_date = models.FloatField('过保修期',null=True,blank=True)
    bussiness_unit = models.ForeignKey('BusinessUnit',verbose_name='所属业务线',null=True,blank=True,on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField('Tag',blank=True,null=True)
    admin = models.ForeignKey(get_user_model(),verbose_name='资产管理员',null=True,blank=True,on_delete=models.DO_NOTHING)
    idc = models.ForeignKey('IDC',verbose_name='IDC机房',null=True,blank=True,on_delete=models.DO_NOTHING)
    status_choices = (
        ('online','在线'),
        ('offline','已下线'),
        ('unknown','未知'),
        ('breakdown','故障'),
        ('backup','备用'),
    )
    status = models.CharField(max_length=20,choices=status_choices,default='online')
    memo = models.TextField('备注',null=True,blank=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,auto_now=True)
    class Meta:
        verbose_name = '资产总表'
        verbose_name_plural = '资产总表'
        unique_together = ('name','sn')

    def __str__(self):
        return '%s %s' %(self.name,self.sn)


class Server(models.Model):
    """
    服务器设备
    """
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    sub_asset_type_choices = (
        ('Rack','机架式服务器'),
        ('Tower','塔式服务器'),
        ('Blade','刀片式服务器'),
        ('PC','PC型小服务器'),
        ('Vps', '虚拟服务器'),
    )
    sub_asset_type = models.CharField(max_length=20,choices=sub_asset_type_choices,verbose_name='服务器类型',default='Rack')
    hosted_on = models.ForeignKey('self',related_name='hosted_on_server',on_delete=models.DO_NOTHING,blank=True,null=True)
    server_factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING,null=True,blank=True)
    model = models.CharField('型号',max_length=128,null=True,blank=True)
    os_type = models.CharField('操作系统类型',max_length=64,blank=True,null=True)
    os_release = models.CharField('操作系统版本',max_length=64,blank=True,null=True)
    kernel_release = models.CharField('内核版本',max_length=64,blank=True,null=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True)
    class Meta:
        verbose_name = '服务器'
        verbose_name_plural = '服务器'

    def __str__(self):
        return '%s %s' %(self.asset.name,self.asset.sn)


class Board(models.Model):
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    board_factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING,blank=True,null=True)
    board_model = models.CharField(max_length=64,blank=True,null=True)
    board_sn = models.CharField(max_length=128,blank=True,null=True)
    class Meta:
        verbose_name = '主板'
        verbose_name_plural = '主板'

    def __str__(self):
        return '%s %s' %(self.asset.name,self.asset.sn)


class SecurityDevice(models.Model):
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    sub_asset_type_choices = (
        ('防火墙','防火墙'),
        ('入侵检测设备','入侵检测设备'),
        ('互联网网关','互联网网关'),
        ('其它安全设备','其它安全设备')
    )
    sub_asset_type = models.CharField(choices=sub_asset_type_choices,max_length=20,)
    factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING)
    model = models.CharField('型号',max_length=128,null=True,blank=True)
    manage_ip = models.GenericIPAddressField('内网管理IP',null=True,blank=True)

    def __str__(self):
        return '%s %s %s' %(self.sub_asset_type,self.asset.name,self.asset.sn)


class NetworkDevice(models.Model):
    """
    网络设备
    """
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    sub_asset_type_choices = (
        ('router','路由器'),
        ('switch','交换机'),
        ('NLB','负载均衡'),
        ('VPN','VPN设备'),
        ('wireless-AP','无线AP'),
    )
    sub_asset_type = models.CharField(max_length=20,choices=sub_asset_type_choices,verbose_name='网络设备类型',default='router')
    vlan_ip = models.GenericIPAddressField('VlanIP',null=True,blank=True)
    manage_ip = models.GenericIPAddressField('内网IP',blank=True,null=True)
    factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING,null=True,blank=True)
    model = models.CharField('型号',max_length=128,null=True,blank=True)
    device_detail = models.TextField('设备详细参数',null=True,blank=True)
    class Meta:
        verbose_name = '网络设备'
        verbose_name_plural = '网络设备'

    def __str__(self):
        return '%s %s %s' %(self.sub_asset_type,self.asset.name,self.asset.sn)


class Software(models.Model):
    """
    系统/软件,只保存购买的软件或系统
    例如: oracle授权，adobe授权，VPN授权，VMware虚拟系统等
    """
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    sub_asset_type_choices = (
        ('System','系统'),
        ('Software','软件'),
    )
    sub_asset_type = models.CharField(max_length=20,choices=sub_asset_type_choices,verbose_name='软件资产类型',default='Software')
    factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING,null=True,blank=True)
    version = models.CharField('系统/软件版本', max_length=100)
    license_num = models.IntegerField(verbose_name='授权数')

    class Meta:
        verbose_name = '系统/软件'
        verbose_name_plural = '系统/软件'

    def __str__(self):
        return '%s %s' %(self.asset.name,self.version)


class CPU(models.Model):
    """
    CPU组件
    """
    asset = models.OneToOneField('Asset',on_delete=models.CASCADE)
    cpu_factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING,null=True,blank=True)
    cpu_arch = models.CharField('CPU架构',max_length=50,blank=True,null=True)
    cpu_model = models.CharField('CPU型号',max_length=100,blank=True)
    cpu_physical_num = models.SmallIntegerField('物理CPU个数',blank=True,null=True)
    cpu_core_count = models.SmallIntegerField('CPU核数')
    cpu_flags = models.TextField('CPU支持的功能')
    memo = models.TextField('备注',null=True,blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        verbose_name = 'CPU部件'
        verbose_name_plural = 'CPU部件'

    def __str__(self):
        return '%s %s' %(self.asset.name,self.cpu_model)


class RAM(models.Model):
    """
    内存组件
    """
    asset = models.ForeignKey('Asset',on_delete=models.DO_NOTHING)
    sn = models.CharField('SN号',max_length=128,blank=True,null=True)
    ram_factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING,null=True,blank=True)
    model = models.CharField('内存型号',max_length=128,null=True,blank=True)
    slot = models.CharField('插槽',max_length=64)
    speed = models.CharField('速度',max_length=30,null=True,blank=True)
    capacity = models.IntegerField('内存大小（MB）')
    memo = models.TextField('备注',blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,blank=True)
    update_date = models.DateTimeField(blank=True,null=True,auto_now=True)

    class Meta:
        verbose_name = 'RAM'
        verbose_name_plural = 'RAM'
        unique_together = ('asset','slot')

    def __str__(self):
        return '%s %s %s' %(self.asset.name,self.slot,self.capacity)


class Disk(models.Model):
    """
    磁盘组件
    """
    asset = models.ForeignKey('Asset',on_delete=models.DO_NOTHING)
    sn = models.CharField('SN号',max_length=128,blank=True,null=True)
    slot = models.CharField('插槽',max_length=64,blank=True,null=True)
    factory = models.CharField('制造商',max_length=64,blank=True,null=True)
    model = models.CharField('磁盘型号',max_length=128,blank=True,null=True)
    capacity = models.FloatField('磁盘容量GB')
    disk_iface_choices = (
        ('SATA','SATA'),
        ('SAS','SAS'),
        ('SCSI','SCSI'),
        ('SSD','SSD'),
    )
    iface_type = models.CharField('接口类型',choices=disk_iface_choices,max_length=20,default='SAS')
    memo = models.TextField('备注',blank=True,null=True)
    create_date = models.DateTimeField(auto_now_add=True,blank=True)
    update_date = models.DateTimeField(blank=True,null=True)

    class Meta:
        verbose_name = '硬盘'
        verbose_name_plural = '硬盘'
        unique_together = ('asset','slot')

    def __str__(self):
        return '%s %s %s' %(self.asset.name,self.slot,self.capacity)


class NIC(models.Model):
    """
    网卡组件
    """
    asset = models.ForeignKey('Asset',on_delete=models.DO_NOTHING)
    name = models.CharField('网卡名',max_length=20,blank=True,null=True)
    model = models.CharField('网卡型号',max_length=128,blank=True,null=True)
    mac_addr = models.CharField('MAC地址',max_length=64,unique=True)
    ip_addr = models.GenericIPAddressField('IP',blank=True,null=True)
    netmask = models.CharField(max_length=64,blank=True,null=True)
    broadcast = models.CharField(max_length=64,blank=True,null=True)
    memo = models.TextField('备注',blank=True,null=True)
    create_date = models.DateTimeField(blank=True,auto_now_add=True)
    update_date = models.DateTimeField(blank=True,null=True,auto_now=True)
    # auto_create_files = ['name','sn','model','macaddress','netmask','bonding']

    class Meta:
        verbose_name = '网卡'
        verbose_name_plural = '网卡'
        unique_together = ('asset','mac_addr')

    def __str__(self):
        return '%s %s' %(self.asset.name,self.mac_addr)


class Manufactory(models.Model):
    """
    厂商/制造商/代理商/服务商
    """
    manufactory = models.CharField('厂商名称',max_length=64,unique=True)
    support_person = models.CharField('联系人',max_length=10,blank=True,null=True)
    support_num = models.CharField('支持电话',max_length=30,blank=True,null=True)
    memo = models.TextField('备注',blank=True,null=True)
    class Meta:
        verbose_name = '厂商'
        verbose_name_plural = '厂商'

    def __str__(self):
        return self.manufactory


class BusinessUnit(models.Model):
    """
    业务线
    """
    parent_unit =  models.ForeignKey('self',related_name='parent_level',on_delete=models.DO_NOTHING,blank=True,null=True)
    name = models.CharField('业务线',max_length=64,unique=True)
    memo = models.TextField('备注',blank=True,null=True)
    class Meta:
        verbose_name = '业务线'
        verbose_name_plural = '业务线'

    def __str__(self):
        return self.name


class Contract(models.Model):
    """
    合同
    """
    contract_num = models.CharField('合同编号',max_length=128,unique=True)
    name = models.CharField('合同名称',max_length=64)
    contract_factory = models.ForeignKey('Manufactory',on_delete=models.DO_NOTHING)
    price = models.IntegerField('合同金额',null=True,blank=True)
    detail = models.TextField('合同详情',blank=True,null=True)
    memo = models.TextField('备注', blank=True, null=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)
    class Meta:
        verbose_name = '合同'
        verbose_name_plural = '合同'

    def __str__(self):
        return '%s %s' %(self.name,self.contract_num)


class IDC(models.Model):
    """
    IDC机房
    """
    name = models.CharField('机房名称',max_length=64,unique=True)
    address = models.CharField('机房地址',max_length=128)
    memo = models.TextField('备注',blank=True,null=True)
    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房'

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    资产标签
    """
    name = models.CharField('Tag_Name',max_length=128,unique=True)
    creator = models.ForeignKey(get_user_model(),on_delete=models.DO_NOTHING)
    create_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class EventLog(models.Model):
    """
    事件日志
    """
    name = models.CharField('事件名称',max_length=128)
    event_type_choices = (
        ('硬件变更','硬件变更'),
        ('新增配件','新增配件'),
        ('设备上线','设备上线'),
        ('设备下线','设备下线'),
        ('定期维护','定期维护'),
        ('业务上线/变更','业务上线/变更'),
        ('其他','其他'),
    )
    event_type = models.CharField('事件类型',choices=event_type_choices,max_length=20)
    asset = models.ManyToManyField('Asset',null=True)
    detail = models.TextField('事件详情')
    date = models.DateTimeField('事件时间',auto_now_add=True)
    handler = models.ForeignKey(get_user_model(),verbose_name='事件负责人',on_delete=models.DO_NOTHING,blank=True,null=True)
    memo = models.TextField('备注',blank=True,null=True)
    class Meta:
        verbose_name = '事件记录'
        verbose_name_plural = '事件记录'

    def __str__(self):
        return '%s %s' %(self.name,self.date)


class NewAssetApprovalZone(models.Model):
    """新资产待审批区"""

    name = models.CharField('名称',max_length=100,unique=True)  # 如何是服务器或虚拟机，则是hostname
    sn = models.CharField(u'资产SN号', max_length=128)
    asset_type_choices = (
        ('server', '服务器'),
        ('networkdevice', '网络设备'),
        ('storagedevice', '储存设备'),
        ('securitydevice', '安全设备'),
        ('software', '软件资产'),
        ('others', '其他类'),
    )
    asset_type = models.CharField(choices=asset_type_choices, max_length=64, blank=True, null=True)
    contract = models.ForeignKey('Contract',on_delete=models.DO_NOTHING,null=True)
    bussiness_unit = models.ForeignKey('BusinessUnit',on_delete=models.DO_NOTHING,blank=True)
    tags = models.ManyToManyField('Tag')
    idc = models.ForeignKey('IDC',models.DO_NOTHING,blank=True)
    data = models.TextField(u'资产数据')
    date = models.DateTimeField(u'汇报日期', auto_now_add=True)
    approved = models.BooleanField(u'已批准', default=False)
    approved_by = models.ForeignKey(get_user_model(), verbose_name=u'批准人', blank=True, null=True,on_delete=models.DO_NOTHING)
    approved_date = models.DateTimeField(u'批准日期', blank=True, null=True)

    def __str__(self):
        return '%s %s' %(self.name,self.sn)

    class Meta:
        verbose_name = '新上线待批准资产'
        verbose_name_plural = "新上线待批准资产"