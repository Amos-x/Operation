# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 14:17
#   FileName = user

import uuid
import sshpubkeys
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.utils import timezone
from users.utils import date_expired_default
from common.utils import get_signer


__all__ = ['User']
signer = get_signer()


class User(AbstractUser):
    ROLE_ADMIN = 'Admin'
    ROLE_USER = 'User'
    ROLE_APP = 'App'

    ROLE_CHOICES = (
        (ROLE_ADMIN, _('Administrator')),
        (ROLE_USER, _('User')),
        (ROLE_APP, _('Application')),
    )

    OTP_LEVEL_CHOICES = (
        (0, _("Disable")),
        (1, _("Enable")),
        (2, _('Force enable'))
    )

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, verbose_name=_('Id'))
    name = models.CharField(max_length=64, verbose_name=_('Name'))
    email = models.EmailField(max_length=128, unique=True, verbose_name=_('Email'))
    groups = models.ManyToManyField('users.UserGroup', related_name='users', blank=True, null=True, verbose_name=_('User Group'))
    # 角色
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default='User', blank=True, null=True, verbose_name=_('Role'))
    # 头像
    avatar = models.ImageField(upload_to="avatar", null=True, verbose_name=_('Avatar'))
    wechat = models.CharField(max_length=128, blank=True, null=True, verbose_name=_('Wechat'))
    phone = models.CharField(max_length=128, null=True, blank=True, verbose_name=_('Phone'))
    # otp_level = models.SmallIntegerField(default=0, choices=OTP_LEVEL_CHOICES, verbose_name=_('MFA'))
    # 公钥私钥
    _private_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name=_("Private key"))
    _public_key = models.CharField(max_length=5000, blank=True, null=True, verbose_name=_('Public key'))

    comment = models.TextField(max_length=200, blank=True, null=True, verbose_name=_('Comment'))
    is_first_login = models.BooleanField(default=True)
    # 过期时间
    date_expired = models.DateTimeField(
        default=date_expired_default, blank=True, null=True, db_index=True, verbose_name=_('Date expired')
    )
    created_by = models.CharField(max_length=64, default='', verbose_name=_('Created by'))

    def __str__(self):
        return '{}({})'.format(self.name, self.username)

    class Meta:
        db_table = 'users_user'
        ordering = ['username']
        verbose_name = _("User")

    @property
    def password_raw(self):
        raise AttributeError('Password raw is not a readable attribute')

    #: Use this attr to set user object password, example
    #: user = User(username='example', password_raw='password', ...)
    #: It's equal:
    #: user = User(username='example', ...)
    #: user.set_password('password')
    @password_raw.setter
    def password_raw(self, password_raw_):
        self.set_password(password_raw_)

    @property
    def private_key(self):
        return signer.unsign(self._private_key)

    @private_key.setter
    def private_key(self, private_key_raw):
        self._private_key = signer.sign(private_key_raw)

    @property
    def public_key(self):
        return signer.unsign(self._public_key)

    @public_key.setter
    def public_key(self, public_key_raw):
        self._public_key = signer.sign(public_key_raw)

    @property
    def public_key_obj(self):
        """ """
        if self.public_key:
            try:
                return sshpubkeys.SSHKey(self.public_key)
            except TabError:
                pass
            return None

    @property
    def is_superuser(self):
        """ 判断是否为管理员 """
        if self.role == 'Admin':
            return True
        else:
            return False

    @is_superuser.setter
    def is_superuser(self, value):
        if value is True:
            self.role = 'Admin'
        else:
            self.role = 'User'

    @property
    def avatar_url(self):
        """ 获取用户头像url """
        if self.avatar:
            return self.avatar.url
        elif self.is_superuser:
            return settings.STATIC_URL + "img/avatar/admin.png"
        else:
            return settings.STATIC_URL + "img/avatar/user.png"

    @property
    def is_expired(self):
        """ 判断用户是否过期 """
        if self.date_expired and self.date_expired < timezone.now():
            return True
        else:
            return False

    @property
    def is_valid(self):
        """ 判断用户是否可用 """
        if self.is_active and not self.is_expired:
            return True
        else:
            return False

    def generate_reset_token(self):
        """ 生成重置token，带过期时间3600秒，即 1 hour """
        return signer.sign_t(
            {'reset': str(self.id), 'email': self.email}, expires_in=3600
        )

    @classmethod
    def validate_reset_token(cls, token):
        """ 验证token """
        try:
            data = signer.unsign_t(token)
            user_id = data.get('reset', None)
            user_email = data.get('email', '')
            user = cls.objects.get(id=user_id, email=user_email)
        except:
            user = None
        return user

    @property
    def is_staff(self):
        """ 判断用户是否已登录且可用 """
        if self.is_authenticated and self.is_valid:
            return True
        else:
            return False

    @is_staff.setter
    def is_staff(self, value):
        """ 无法直接设置is_staff参数"""
        pass