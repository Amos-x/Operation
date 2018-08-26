# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司

from repository import models


class Basic(object):
    def __init__(self,response):
        self.response = response

    def _create_server(self,asset_obj,value):
        models.Server.objects.create(
            asset=asset_obj,
            os_type=value['os_type'],
            os_release=value['os_release'],
            kernel_release=value['kernel_release']
        )

    def accept_process(self):
        result = self.response.get('basic')
        for salt_key,value in result.items():
            if value['status']:
                asset_obj = models.Asset.objects.filter(name=salt_key).first()
                if not asset_obj:
                    asset_obj = models.Asset(name=value['name'],sn=value['sn'])
                    asset_obj.save()
                    self._create_server(asset_obj=asset_obj,value=value)
                    message = 'salt自动采集新增资产基本信息：%s' %self.response
                else:
                    server_obj = models.Server.objects.filter(asset=asset_obj).first()
                    if server_obj:
                        message = []
                        if asset_obj.sn != value['sn']:
                            old_data = asset_obj.sn
                            asset_obj.sn = value['sn']
                            message.append(' 资产%s字段SN更新：原：%s 新：%s ' %(value['name'],old_data,value['sn']))
                        if server_obj.os_type != value['os_type']:
                            old_data = server_obj.os_type
                            server_obj.os_type = value['os_type']
                            message.append(' 资产%s字段os_type更新：原：%s 新：%s ' %(value['name'],old_data,value['os_type']))
                        if server_obj.os_release != value['os_release']:
                            old_data = server_obj.os_release
                            server_obj.os_release = value['os_release']
                            message.append(' 资产%s字段os_release更新：原：%s 新：%s ' %(value['name'],old_data,value['os_release']))
                        if server_obj.kernel_release != value['kernel_release']:
                            old_data = server_obj.kernel_release
                            server_obj.kernel_release = value['kernel_release']
                            message.append(' 资产%s字段kernel_release更新：原：%s 新：%s ' %(value['name'],old_data,value['kernel_release']))
                        if message:
                            asset_obj.save()
                            message = ','.join(message)
                    else:
                        self._create_server(asset_obj=asset_obj, value=value)
                        message = 'salt自动采集新增资产基本信息：%s' % self.response
            else:
                message = value['message']
            if message:
                models.EventLog.objects.create(
                    name='资产自动采集',
                    event_type='定期维护',
                    detail=message
                )
