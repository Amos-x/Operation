# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司
from repository import models


class Memory(object):
    def __init__(self,response):
        self.response = response

    def _create_ram(self,asset_obj,value):
        models.RAM.objects.create(
            asset = asset_obj,
            slot= value['slot'],
            capacity = value['capacity'],
            model = value['model']
        )


    def accept_process(self):
        result = self.response.get('memory')
        for salt_key, value in result.items():
            if value['status']:
                asset_obj = models.Asset.objects.filter(name=salt_key).first()
                del value['status']
                if not asset_obj:
                    asset_obj = models.Asset(name=salt_key)
                    asset_obj.save()
                    for slot,data in value.items():
                        self._create_ram(asset_obj=asset_obj, value=data)
                    message = 'salt自动采集新增资产board信息：%s' % self.response
                else:
                    message = []
                    for slot, data in value.items():
                        ram_obj = models.RAM.objects.filter(asset=asset_obj,slot=slot).first()
                        if ram_obj:
                            a =[]
                            if ram_obj.capacity != float(data['capacity']):
                                a.append('1')
                                old_data = ram_obj.capacity
                                ram_obj.capacity = data['capacity']
                                message.append(' 资产%s字段capacity更新：原：%s 新：%s ' % (salt_key, old_data, data['capacity']))
                            if ram_obj.model != data['model']:
                                a.append('2')
                                old_data = ram_obj.model
                                ram_obj.model = data['model']
                                message.append(' 资产%s字段model更新：原：%s 新：%s ' % (salt_key, old_data, data['model']))
                            if a:
                                ram_obj.save()
                        else:
                            self._create_ram(asset_obj=asset_obj, value=data)
                            message.append(' salt自动采集新增资产RAM信息,插槽:%s 内容:%s ' %(slot,data))
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


