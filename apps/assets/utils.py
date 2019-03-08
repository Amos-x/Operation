# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-27 19:27
#   FileName = utils

import os
import sshpubkeys
import paramiko
from io import StringIO
from six import string_types


def ssh_key_string_to_obj(text, password=None):
    """ 生成密钥对象，用于paramiko登陆时的pkey参数 """
    key = None
    try:
        key = paramiko.RSAKey.from_private_key(StringIO(text), password=password)
    except paramiko.SSHException:
        pass

    try:
        key = paramiko.DSSKey.from_private_key(StringIO(text), password=password)
    except paramiko.SSHException:
        pass
    return key


def validate_ssh_private_key(text, password=None):
    """ 验证ssh私钥 """
    if isinstance(text, bytes):
        try:
            text = text.decode("utf-8")
        except UnicodeDecodeError:
            return False

    key = ssh_key_string_to_obj(text, password=password)
    if key is None:
        return False
    else:
        return True


def validate_ssh_public_key(text):
    """ 验证ssh公钥 """
    ssh = sshpubkeys.SSHKey(text)
    try:
        ssh.parse()
    except (sshpubkeys.InvalidKeyException, UnicodeDecodeError):
        return False
    except NotImplementedError as e:
        return False
    return True


def ssh_pubkey_gen(private_key=None, username='operation', hostname='localhost', password=None):
    """ 根据私钥，生成公钥，并返回 """
    if isinstance(private_key, bytes):
        private_key = private_key.decode("utf-8")
    if isinstance(private_key, string_types):
        private_key = ssh_key_string_to_obj(private_key, password=password)
    if not isinstance(private_key, (paramiko.RSAKey, paramiko.DSSKey)):
        raise IOError('Invalid private key')

    public_key = "%(key_type)s %(key_content)s %(username)s@%(hostname)s" % {
        'key_type': private_key.get_name(),
        'key_content': private_key.get_base64(),
        'username': username,
        'hostname': hostname,
    }
    return public_key


def ssh_key_gen(length=2048, type='rsa', password=None, username='operation', hostname=None):
    """ 自动生成用户ssh私钥和公钥，使用paramiko生成 ，返回 私钥，公钥 """
    if hostname is None:
        hostname = os.uname()[1]

    f = StringIO()
    try:
        if type == 'rsa':
            private_key_obj = paramiko.RSAKey.generate(length)
        elif type == 'dsa':
            private_key_obj = paramiko.DSSKey.generate(length)
        else:
            raise IOError('SSH private key must be `rsa` or `dsa`')
        private_key_obj.write_private_key(f,password=password)
        private_key = f.getvalue()
        public_key = ssh_pubkey_gen(private_key_obj, username=username, hostname=hostname)
        return private_key, public_key
    except IOError:
        raise IOError("These is error when generate ssh key")
