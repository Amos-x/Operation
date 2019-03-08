# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-28 14:29
#   FileName = utils

import logging
from itsdangerous import TimedJSONWebSignatureSerializer, JSONWebSignatureSerializer, \
    BadSignature, SignatureExpired
from django.conf import settings


class Singleton(type):
    """ 单例模式元类 """
    def __init__(cls, *args, **kwargs):
        cls.__instance = None
        super().__init__(*args,**kwargs)

    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args,**kwargs)
            return cls.__instance
        else:
            return cls.__instance


class Signer(metaclass=Singleton):
    """ 用于加密，解密，和基于时间戳的方式验证token -- 单实例模式"""
    def __init__(self, secret_key=None):
        self.secret_key = secret_key

    def sign(self, value):
        """ json web 签名 """
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        s = JSONWebSignatureSerializer(self.secret_key)
        return s.dumps(value)

    def unsign(self, value):
        """ json web 解签名 """
        if value is None:
            return value
        s = JSONWebSignatureSerializer(self.secret_key)
        try:
            return s.loads(value)
        except BadSignature:
            return {}

    def sign_t(self, value, expires_in=3600):
        """ json web 带过期时间的 签名"""
        s = TimedJSONWebSignatureSerializer(self.secret_key, expires_in=expires_in)
        return str(s.dumps(value), encoding='utf8')

    def unsign_t(self, value):
        """ json web 带过期时间的 解签名"""
        s = TimedJSONWebSignatureSerializer(self.secret_key)
        try:
            return s.loads(value)
        except (BadSignature, SignatureExpired):
            return {}


def get_signer():
    """ 返回一个签名实例 """
    signer = Signer(settings.SECRET_KEY)
    return signer


def get_logger(name=None):
    """ 返回日志logger """
    return logging.getLogger('operation.{}'.format(name))


def get_object_or_none(model, **kwargs):
    """ 返回单个model对象 或 None。 传入模型对象，和查询的筛选字段 """
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj
