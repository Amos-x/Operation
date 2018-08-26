# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司
from repository import models


class Disk(object):
    def __init__(self,response):
        self.response = response

    def _create_disk(self,asset_obj,value):
        models.Disk.objects.create(
            asset=asset_obj,
            iface_type = value['iface_type'],
            capacity = value['capacity']
        )

    def accept_process(self):
        result = self.response.get('disk')
        for salt_key, value in result.items():
            if value['status']:
                asset_obj = models.Asset.objects.filter(name=salt_key).first()
                if not asset_obj:
                    asset_obj = models.Asset(name=salt_key)
                    asset_obj.save()
                    self._create_disk(asset_obj=asset_obj, value=value)
                    message = 'salt自动采集新增资产RAM信息：%s' % self.response
                else:
                    disk_obj = models.Disk.objects.filter(asset=asset_obj).first()
                    if disk_obj:
                        message = []
                        if disk_obj.iface_type != value['iface_type']:
                            old_data = disk_obj.iface_type
                            disk_obj.iface_type = value['iface_type']
                            message.append('资产%s字段iface_type更新：原：%s 新：%s' % (salt_key, old_data, value['iface_type']))
                        if disk_obj.capacity != float(value['capacity']):
                            old_data = disk_obj.capacity
                            disk_obj.capacity = value['capacity']
                            message.append('资产%s字段capacity更新：原：%s 新：%s' % (salt_key, old_data, value['capacity']))
                        if message:
                            disk_obj.save()
                            message = ' , '.join(message)
                    else:
                        self._create_disk(asset_obj=asset_obj, value=value)
                        message = 'salt自动采集新增资产RAM信息：%s' % self.response
            else:
                message = value['message']
            if message:
                models.EventLog.objects.create(
                    name='资产自动采集',
                    event_type='定期维护',
                    detail=message
                )
