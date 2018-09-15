# __author__ = "Amos"
# Email: 379833553@qq.com
# Company: 佛山科瑞森科技有限公司
from apps.core import models


class Board(object):
    def __init__(self,response):
        self.response = response

    def _create_board(self,asset_obj,value):
        manu_obj = models.Manufactory.objects.filter(manufactory=value['board_factory']).first()
        if not manu_obj:
            manu_obj = models.Manufactory(manufactory=value['board_factory'])
            manu_obj.save()
        models.Board.objects.create(
            asset=asset_obj,
            board_factory=manu_obj,
            board_model=value['board_model'],
            board_sn=value['board_sn']
        )


    def accept_process(self):
        result = self.response.get('board')
        for salt_key,value in result.items():
            if value['status']:
                asset_obj = models.Asset.objects.filter(name=salt_key).first()
                if not asset_obj:
                    asset_obj = models.Asset(name=salt_key)
                    asset_obj.save()
                    self._create_board(asset_obj=asset_obj,value=value)
                    message = 'salt自动采集新增资产board信息：%s' % self.response
                else:
                    board_obj = models.Board.objects.filter(asset=asset_obj).first()
                    if board_obj:
                        message = []
                        if board_obj.board_factory.manufactory != value['board_factory']:
                            old_data = board_obj.board_factory.manufactory
                            manu_obj = models.Manufactory(manufactory=value['board_factory'])
                            manu_obj.save()
                            board_obj.board_factory = manu_obj
                            message.append('资产%s字段board_factory更新：原：%s 新：%s' %(salt_key,old_data,value['board_factory']))
                        if board_obj.board_model != value['board_model']:
                            old_data = board_obj.board_model
                            board_obj.board_model = value['board_model']
                            message.append('资产%s字段board_model更新：原：%s 新：%s' %(salt_key,old_data,value['board_model']))
                        if board_obj.board_sn != value['board_sn']:
                            old_data = board_obj.board_sn
                            board_obj.board_sn = value['board_sn']
                            message.append('资产%s字段board_sn更新：原：%s 新：%s' %(salt_key,old_data,value['board_sn']))
                        if message:
                            board_obj.save()
                            message = ' , '.join(message)
                    else:
                        self._create_board(asset_obj=asset_obj,value=value)
                        message = 'salt自动采集新增资产board信息：%s' % self.response
            else:
                message = value['message']
            if message:
                models.EventLog.objects.create(
                    name='资产自动采集',
                    event_type='定期维护',
                    detail=message
                )
