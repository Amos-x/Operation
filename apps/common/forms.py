# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-08 19:40
#   FileName = forms

import json
from django import forms
from django.conf import settings
from django.db import transaction
from django.utils.translation import ugettext_lazy as _
from common.models import Setting


__all__ = ['BasicSettingForm', 'EmailSettingForm', 'SecuritySettingForm']


def to_model_vlue(value):
    try:
        return json.dumps(value)
    except json.JSONDecodeError:
        return None


def to_form_value(value):
    try:
        data = json.loads(value)
        if isinstance(data,dict):
            data = value
        return data
    except json.JSONDecodeError:
        return ""


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        db_settings = Setting.objects.all()
        for name, field in self.fields.items():
            db_value = getattr(db_settings, name).value
            django_value = getattr(settings, name) if hasattr(settings, name) else None
            if db_value is False or db_value:
                field.initial = to_form_value(db_value)
            elif django_value is False or django_value:
                field.initial = to_form_value(to_model_vlue(django_value))

    def save(self):
        """ 重写save函数 设定一些修改规则 """
        if not self.is_bound:
            raise ValueError("Form is not bound")

        db_settings = Setting.objects.all()
        if self.is_valid():
            with transaction.atomic():
                for name, value in self.cleaned_data.items():
                    field = self.fields[name]
                    if isinstance(field.widget, forms.PasswordInput) and not value:
                        # 密码类字段为空时不做更新
                        continue
                    if value == to_form_value(getattr(db_settings, name).value):
                        # 如果配置跟文件配置相同，则不做数据库保存
                        continue

                    default = {
                        'name': name,
                        'value': to_model_vlue(value)
                    }
                    Setting.objects.update_or_create(defaults=default, name=name)
        else:
            raise ValueError(self.errors)


class BasicSettingForm(BaseForm):
    """ basic setting 设置项 """
    SITE_URL = forms.URLField(
        label=_('Current SITE URL'),
        help_text="eg: http://jumpserver.abc.com:8080"
    )
    USER_GUIDE_URL = forms.URLField(
        label=_("User Guide URL"), required=False,
        help_text=_('User first login update profile done redirect to it')
    )
    EMAIL_SUBJECT_PREFIX = forms.CharField(
        max_length=128, label=_('Email Subject Prefix'),
        initial="[Operation]"
    )


class EmailSettingForm(BaseForm):
    """ email setting 设置项 """
    EMAIL_HOST = forms.CharField(
        max_length=255, label=_('SMTP host'), initial='smtp.operation.org'
    )
    EMAIL_PORT = forms.IntegerField(min_value=1, max_value=65536, label=_('SMTP port'), initial=25)
    EMAIL_HOST_USER = forms.CharField(max_length=128, label=_('SMTP user'), initial='noreply@operation.org')
    EMAIL_HOST_PASSWORD = forms.CharField(
        max_length=255, label=_('SMTP user password'), widget=forms.PasswordInput, required=False,
        help_text=_("Some provider use token except password")
    )
    EMAIL_USE_SSL = forms.BooleanField(
        label=_('Use SSL'), initial=False, required=False,
        help_text=_('If SMTP port is 465, may be select')
    )
    EMAIL_USE_TLS = forms.BooleanField(
        label=_('Use TLS'), initial=False, required=False,
        help_text=_('If SMTP port is 587, may be select')
    )


class SecuritySettingForm(BaseForm):
    """ 安全设置项 """
    # MFA global setting
    SECURITY_MFA_AUTH = forms.BooleanField(
        label=_('MFA Secondary certification'), initial=False, required=False,
        help_text=_(
            'After opening, the user login must use MFA secondary '
            'authentication (valid for all users, including administrators)'
        )
    )

    # 登录失败多少次会被锁
    SECURITY_LOGIN_LIMIT_COUNT = forms.IntegerField(
        initial=3, min_value=3,
        label=_('Limit the number of login failures')
    )

    # 账号登录失败超过限制，被锁时间
    SECURITY_LOGIN_LIMIT_TIME = forms.IntegerField(
        initial=30, min_value=5,
        label=_('No login interval'),
        help_text=_(
            "Tip :(unit/minute) if the user has failed to log in for a limited "
            "number of times, no login is allowed during this time interval."
        )
    )

    # 密码最小长度
    SECURITY_PASSWORD_MIN_LENGTH = forms.IntegerField(
        initial=6, min_value=6,
        label=_('Password minimum length')
    )

    # 密码必须包含大写字母
    SECURITY_PASSWORD_UPPER_CASE = forms.BooleanField(
        initial=False, required=False,
        label=_('Must contain capital letters'),
        help_text=_(
            'After opening, the user password changes '
            'and resets must contain uppercase letters'
        )
    )

    # 密码必须包含小写字母
    SECURITY_PASSWORD_LOWER_CASE = forms.BooleanField(
        initial=False, required=False,
        label=_('Must containn lowercase letters'),
        help_text=_(
            'After opening, the user password changes '
            'and resets must contain lowercase letters'
        )
    )

    # 密码必须包含数字
    SECURITY_PASSWORD_NUMBER = forms.BooleanField(
        initial=False, required=False,
        label=_('Must contain numeric characters'),
        help_text=_(
            'After opening, the user password changes '
            'and resets must contain numeric characters'
        )
    )

    # 密码必须包含特殊字符
    SECURITY_PASSWORD_SPECIAL_CHAR = forms.BooleanField(
        initial=False, required=False,
        label=_('Must contain special characters'),
        help_text=_(
            'After opening, the user password changes '
            'and resets must contain special characters'
        )
    )
