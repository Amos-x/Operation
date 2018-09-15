# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司
from apps.core import models


class Nic(object):
    def __init__(self,response):
        self.response = response

    def _create_nic(self,asset_obj,value,name):
        models.NIC.objects.create(
            asset = asset_obj,
            name=name,
            mac_addr = value['mac_addr'],
            ip_addr = value['ip'],
            netmask = value['netmask'],
            broadcast = value['broadcast'],
        )

    def accept_process(self):
        result = self.response.get('nic')
        for salt_key, value in result.items():
            if value['status']:
                asset_obj = models.Asset.objects.filter(name=salt_key).first()
                del value['status']
                if not asset_obj:
                    asset_obj = models.Asset(name=salt_key)
                    asset_obj.save()
                    for nic_name, data in value.items():
                        self._create_nic(asset_obj=asset_obj, value=data,name=nic_name)
                    message = 'salt自动采集新增资产nic信息：%s' % self.response
                else:
                    message = []
                    for nic_name, data in value.items():
                        nic_obj = models.NIC.objects.filter(asset=asset_obj, mac_addr=data['mac_addr']).first()
                        if nic_obj:
                            a = []
                            if nic_obj.name != nic_name:
                                a.append('1')
                                old_data = nic_obj.name
                                nic_obj.name = nic_name
                                message.append(' 资产%s字段name更新：原：%s 新：%s ' % (salt_key, old_data, nic_name))
                            if nic_obj.ip_addr != data['ip']:
                                a.append('2')
                                old_data = nic_obj.ip_addr
                                nic_obj.ip_addr = data['ip']
                                message.append(' 资产%s字段ip_addr更新：原：%s 新：%s ' %(salt_key, old_data, data['ip']))
                            if nic_obj.netmask != data['netmask']:
                                a.append('3')
                                old_data = nic_obj.netmask
                                nic_obj.netmask = data['netmask']
                                message.append(' 资产%s字段netmask更新：原：%s 新：%s ' % (salt_key, old_data, data['netmask']))
                            if nic_obj.broadcast != data['broadcast']:
                                a.append('3')
                                old_data = nic_obj.broadcast
                                nic_obj.broadcast = data['broadcast']
                                message.append(' 资产%s字段broadcast更新：原：%s 新：%s ' % (salt_key, old_data, data['broadcast']))
                            if a:
                                nic_obj.save()
                        else:
                            self._create_nic(asset_obj=asset_obj, value=data,name=nic_name)
                            message.append(' salt自动采集新增资产nic信息,网卡mac:%s 内容:%s ' % (data['mac_addr'], data))
                    if message:
                        message = ','.join(message)
            else:
                message = value['message']
            if message:
                models.EventLog.objects.create(
                    name='资产自动采集',
                    event_type='定期维护',
                    detail=message
                )