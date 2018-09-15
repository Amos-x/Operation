import json
import logging
import time
import requests
from django.core.cache import cache
from . import settings

logger = logging.getLogger('django')


class SaltApiClient(object):
    def __init__(self):
        """
        初始化，获取salt-api的token，用这个来操作saltstack
        """
        self._url = settings.SALT_API_URL


    def get_salt_token(self):
        _username = settings.SALT_USER
        _passwd = settings.SALT_PASSWD
        headers = {'Content-Type': 'application/json'}
        data = {
            'eauth': 'pam',
            'username': _username,
            'password': _passwd,
        }
        login_url = '%s%s' % (self._url, '/login')
        try:
            response = requests.post(login_url, data=json.dumps(data), headers=headers, verify=False)
            token = response.json()['return'][0]['token']
            expire = response.json()['return'][0]['expire']
            expire_time = int(int(expire) - time.time()) - 3600
            cache.set('salt-token',token,expire_time)
            logger.info('获取salt-api认证token成功。')
            return token
        except:
            token = None
            logger.error('获取salt-api认证token错误。')
            raise Exception('获取salt-api认证token错误。please checkout')

    def token(self):
        """
        使用此方法来返回 token
        """
        token = cache.get('salt-token')
        if not token:
            token = self.get_salt_token()
        return token
