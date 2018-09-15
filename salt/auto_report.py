# __author__ = "Amos"
# Email: 379833553@qq.com

from salt import settings
from concurrent.futures import ThreadPoolExecutor
import importlib


class AutoReportManager(object):

    def __init__(self,token,tgt):
        self.token = token
        self.tgt = tgt
        self.plugins_dict = settings.PLUGINS_DICT
        self.api = settings.INSERT_ASSET_API
        self.accept_dict = settings.ACCEPT_DICT

    def exec_plugins(self):
        """
        循环插件文件夹，依次执行插件，采集资产信息
        """
        pool = ThreadPoolExecutor(10)
        for k,v in self.plugins_dict.items():
            pool.submit(self.task,k,v)

    def task(self,k,v):
        response = {}
        module_path, class_name = v.rsplit('.', 1)
        m = importlib.import_module(module_path)
        cls = getattr(m, class_name)
        response[k] = cls(self.token, self.tgt).process()
        self.update_asset_info(response)

    def update_asset_info(self,response):
        """
        将获取的数据插入数据库
        """
        key = list(response.keys())[0]
        module_path,class_name = self.accept_dict.get(key).rsplit('.',1)
        m = importlib.import_module(module_path)
        cls = getattr(m,class_name)
        cls(response).accept_process()


if __name__ == '__main__':
    token = 'a7a8b2b7acca5d2bc7536dc305bec08237d7db74'
    AutoReportManager(token,['test']).exec_plugins()