# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-05 15:10
#   FileName = user

from django import forms
from django.utils.translation import gettext_lazy as _
from common.utils import get_logger
from django.utils.translation import gettext_lazy as _
from assets.utils import validate_ssh_private_key, ssh_pubkey_gen
from assets.models import AdminUser, SystemUser


__all__ = ['PasswordAndKeyAuthForm', 'AdminUserForm', 'SystemUserForm']
logger = get_logger(__file__)


class FileForm(forms.Form):
    """ 文件表单 """
    file = forms.FileField()


class PasswordAndKeyAuthForm(forms.ModelForm):
    """ 密码或密钥验证表单，是其他用户表单等的基础表单 """
    # Form field name can not start with `_`, so redefine it,
    password = forms.CharField(
        widget=forms.PasswordInput, max_length=128,
        strip=True, required=False, label=_('Password'),
        help_text=_('Password or private key passphrase')
    )
    # Need use upload private key file except paste private key content
    private_key_file = forms.FileField(required=False, label=_('Private key'))

    def clean_private_key_file(self):
        """ 验证上传的私钥文件，返回字符串形式的私钥 """
        private_key_file = self.cleaned_data.get('private_key_file')
        password = self.cleaned_data.get('password')

        if private_key_file:
            key_string = private_key_file.read()
            private_key_file.seek(0)
            if not validate_ssh_private_key(key_string, password):
                raise forms.ValidationError(_('Invalid private key'))
            return private_key_file

    def validate_password_key(self):
        """ 验证私钥 和 密码 必填其一"""
        password = self.cleaned_data.get('password')
        private_key_file = self.cleaned_data.get('private_key_file')

        if not password and not private_key_file:
            raise forms.ValidationError(_('Password and private key file must be input one'))

    def gen_keys(self):
        """ 根据上传的私钥文件，生产公钥，返回密钥对 """
        password = self.cleaned_data.get('password') or None
        private_key_file = self.cleaned_data.get('private_key_file')

        if private_key_file:
            private_key = private_key_file.read().strip().decode('utf-8')
            public_key = ssh_pubkey_gen(private_key=private_key, password=password)
            return private_key, public_key


class AdminUserForm(PasswordAndKeyAuthForm):
    class Meta:
        model = AdminUser
        fields = ['name', 'username', 'password', 'private_key_file', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'username': forms.TextInput(attrs={'placeholder': _('Username')})
        }
        help_texts = {
            'name': '* required',
            'username': '* required'
        }

    def save(self, commit=True):
        admin_user = super().save(commit=commit)
        password = self.cleaned_data.get('password', '') or None
        private_key, public_key = super().gen_keys()
        admin_user.set_auth(password=password, public_key=public_key, private_key=private_key)
        return admin_user

    def clean(self):
        """ 清理数据时，检查密码和密钥必填其一"""
        super().clean()
        if not self.instance:
            super().validate_password_key()


class SystemUserForm(PasswordAndKeyAuthForm):
    # 定义是否自动生成密钥
    auto_generate_key = forms.BooleanField(initial=True, required=False)

    class Meta:
        model = SystemUser
        fields = ['name', 'username', 'priority', 'protocol', 'password', 'private_key_file',
                  'auto_push', 'login_mode', 'comment', 'shell', 'sudo', 'auto_generate_key']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'username': forms.TextInput(attrs={'placeholder': _('Username')})
        }
        help_texts = {
            'name': '* required',
            'username': '* required',
            'auto_push': _('Auto push system user to asset'),
            'priority': _('High level will be using login asset as default, '
                          'if user was granted more than 2 system user'),
            'login_mode': _('If you choose manual login mode, you do not '
                            'need to fill in the username and password.')
        }

    def save(self, commit=True):
        system_user = super().save(commit=commit)
        login_mode = self.cleaned_data.get('login_mode', '') or None
        protocol = self.cleaned_data.get('protocol', '') or None
        auto_generate_key = self.cleaned_data.get('auto_generate_key', False)

        if login_mode == SystemUser.MANUAL_LOGIN or protocol == SystemUser.TELNET_PROTOCOL:
            system_user.auto_push = False
            system_user.save()

        if auto_generate_key:
            logger.info('Auto generate key and set system user auth')
            system_user.auto_gen_auth()
        else:
            password = self.cleaned_data.get('password', '') or None
            private_key, public_key = super().gen_keys()
            system_user.set_auth(password=password, private_key=private_key, public_key=public_key)

        return system_user

    def clean(self):
        super().clean()
        auto_generate = self.cleaned_data.get('auto_generate_key')
        if not self.instance and not auto_generate:
            super().validate_password_key()

    def is_valid(self):
        validated = super().is_valid()
        username = self.cleaned_data.get('username')
        login_mode = self.cleaned_data.get('login_mode')
        if login_mode == SystemUser.AUTO_LOGIN and not username:
            self.add_error(
                "username", _('* Automatic login mode,'
                              ' must fill in the username.')
            )
            return False
        return validated
