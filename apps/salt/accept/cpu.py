# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司
from repository import models


class Cpu(object):
    def __init__(self,response):
        self.response = response

    def _create_cpu(self,asset_obj,value):
        models.CPU.objects.create(
            asset = asset_obj,
            cpu_arch = value['cpu_arch'],
            cpu_model = value['cpu_model'],
            cpu_flags = value['cpu_flags'],
            cpu_core_count = value['cpu_core_count'],
            cpu_physical_num = value['cpu_physical_num']
        )


    def accept_process(self):
        result = self.response.get('cpu')
        for salt_key, value in result.items():
            if value['status']:
                asset_obj = models.Asset.objects.filter(name=salt_key).first()
                if not asset_obj:
                    asset_obj = models.Asset(name=value['name'])
                    asset_obj.save()
                    self._create_cpu(asset_obj=asset_obj, value=value)
                    message = 'salt自动采集新增资产cpu信息：%s' % self.response
                else:
                    cpu_obj = models.CPU.objects.filter(asset=asset_obj).first()
                    if cpu_obj:
                        message = []
                        if cpu_obj.cpu_arch != value['cpu_arch']:
                            old_data = cpu_obj.cpu_arch
                            cpu_obj.cpu_arch = value['cpu_arch']
                            message.append('资产%s字段cpu_arch更新：原：%s 新：%s' % (salt_key, old_data, value['cpu_arch']))
                        if cpu_obj.cpu_model != value['cpu_model']:
                            old_data = cpu_obj.cpu_model
                            cpu_obj.cpu_model = value['cpu_model']
                            message.append('资产%s字段cpu_model更新：原：%s 新：%s' % (salt_key, old_data, value['cpu_model']))
                        if cpu_obj.cpu_flags != str(value['cpu_flags']):
                            old_data = cpu_obj.cpu_flags
                            cpu_obj.cpu_flags = value['cpu_flags']
                            message.append('资产%s字段cpu_flags更新：原：%s 新：%s' % (salt_key, old_data, value['cpu_flags']))
                        if cpu_obj.cpu_core_count != value['cpu_core_count']:
                            old_data = cpu_obj.cpu_core_count
                            cpu_obj.cpu_core_count = value['cpu_core_count']
                            message.append('资产%s字段cpu_core_count更新：原：%s 新：%s' % (salt_key, old_data, value['cpu_core_count']))
                        if cpu_obj.cpu_physical_num != int(value['cpu_physical_num']):
                            old_data = cpu_obj.cpu_physical_num
                            cpu_obj.cpu_physical_num = value['cpu_physical_num']
                            message.append('资产%s字段cpu_physical_num更新：原：%s 新：%s' % (salt_key, old_data, value['cpu_physical_num']))
                        if message:
                            cpu_obj.save()
                            message = ' , '.join(message)
                    else:
                        self._create_cpu(asset_obj=asset_obj, value=value)
                        message = 'salt自动采集新增资产cpu信息：%s' % self.response
            else:
                message = value['message']
            if message:
                models.EventLog.objects.create(
                    name='资产自动采集',
                    event_type='定期维护',
                    detail=message
                )