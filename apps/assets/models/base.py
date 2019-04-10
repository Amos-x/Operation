# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-27 18:01
#   FileName = base

import uuid
import sshpubkeys
from django.db import models
from django.utils.translation import ugettext_lazy as _
from assets.validators import private_key_validator
from assets.utils import ssh_key_string_to_obj, ssh_key_gen
from common.validators import alphanumeric
from common.utils import get_signer


__all__ = ['AssetUser']
signer = get_signer()


class AssetUser(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_('Name'))
    username = models.CharField(max_length=32, blank=True, verbose_name=_('Username'), validators=[alphanumeric])
    _password = models.CharField(max_length=256, blank=True, null=True, verbose_name=_('Password'))
    _private_key = models.TextField(max_length=4096, blank=True, null=True, verbose_name=_('SSH private key'), validators=[private_key_validator])
    _public_key = models.TextField(max_length=4096, blank=True, verbose_name=_('SSH public key'))
    comment = models.TextField(blank=True, verbose_name=_('Comment'))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_('Date created'))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_('Date updated'))
    created_by = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Created by'))

    class Meta:
        abstract = True

    @property
    def password(self):
        if self._password:
            return signer.unsign(self._password)
        else:
            return None

    @password.setter
    def password(self, password_raw):
        raise AttributeError("Using set_auth do this")

    @property
    def private_key(self):
        if self._private_key:
            return signer.unsign(self._private_key)
        else:
            return None

    @private_key.setter
    def private_key(self, private_key_raw):
        raise AttributeError("Using set_auth do this")

    @property
    def public_key(self):
        if self._public_key:
            return signer.unsign(self._public_key)
        else:
            return None

    @public_key.setter
    def public_key(self, public_key_raw):
        raise AttributeError("Using set_auth do this")

    @property
    def private_key_obj(self):
        if self.private_key:
            return ssh_key_string_to_obj(self.private_key, password=self.password)
        else:
            return None

    # @property
    # def private_key_file(self):
    #     if not self.private_key_obj:
    #         return None
    #     project_dir = settings.PROJECT_DIR
    #     tmp_dir = os.path.join(project_dir, 'tmp')
    #     key_str = signer.unsign(self._private_key)
    #     key_name = '.' + md5(key_str.encode('utf-8')).hexdigest()
    #     key_path = os.path.join(tmp_dir, key_name)
    #     if not os.path.exists(key_path):
    #         self.private_key_obj.write_private_key_file(key_path)
    #         os.chmod(key_path, 0o400)
    #     return key_path

    @property
    def public_key_obj(self):
        if self.public_key:
            try:
                return sshpubkeys.SSHKey(self.public_key)
            except TabError:
                pass
        return None

    def set_auth(self, password=None, private_key=None, public_key=None):
        """ 设置验证方式，统一使用此方法进行设置 """
        update_fields = []
        if password:
            self._password = signer.sign(password)
            update_fields.append('_password')
        if private_key:
            self._private_key = signer.sign(private_key)
            update_fields.append('_private_key')
        if public_key:
            self._public_key = signer.sign(public_key)
            update_fields.append('_public_key')

        if update_fields:
            self.save(update_fields=update_fields)

    def clear_auth(self):
        """ 清空重置所有认证方式 """
        self._password = ''
        self._private_key = ''
        self._public_key = ''
        self.save()

    def auto_gen_auth(self):
        """ 自动生成验证信息，包括密码，公钥，私钥 """
        password = str(uuid.uuid4())
        private_key, public_key = ssh_key_gen(username=self.username)
        self.set_auth(password=password,
                      private_key=private_key,
                      public_key=public_key)

    # def _to_secret_json(self):
    #     """ 使用管理用户，推送系统用户时使用 """
    #     return {
    #         'name': self.name,
    #         'username': self.username,
    #         'password': self.password,
    #         'public_key': self.public_key,
    #         'private_key': self.private_key_file,
    #     }
