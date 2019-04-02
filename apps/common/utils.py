# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-28 14:29
#   FileName = utils

import codecs
import re
import csv
import logging
from itsdangerous import TimedJSONWebSignatureSerializer, JSONWebSignatureSerializer, \
    BadSignature, SignatureExpired
from django.conf import settings
from django.urls import reverse as dj_reverse
from django.utils.functional import lazy
from django.http import HttpResponse


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
        return str(s.dumps(value), encoding='utf-8')

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


def reverse(viewname, urlconf=None, args=None, kwargs=None, current_app=None, external=False):
    url = dj_reverse(viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if external:
        url = settings.SITE_URL.strip('/') + url
    return url


reverse_lazy = lazy(reverse, str)


def data_to_csv_http_response(filename, data):
    """ 将list数据，转成csv文件的HttpResponse对象，进行文件导出返回 """
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
    response.write(codecs.BOM_UTF8)
    writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL)
    if isinstance(data, list):
        for line in data:
            writer.writerow(line)
        return response


def is_uuid(seq):
    """ 判断是否是uuid, 接受传入字符串或字符串列表，元组 """
    if isinstance(seq, str):
        uuid_pattern = re.compile(r'[0-9a-zA-Z\-]{36}')
        if uuid_pattern.match(seq):
            return True
        else:
            return False
    else:
        for s in seq:
            if not is_uuid(s):
                return False
        return True
