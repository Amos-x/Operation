# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-21 11:18
#   FileName = login

from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from captcha.fields import CaptchaField


__all__ = ['UserLoginForm', 'UserLoginCaptchaForm']


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label=_('Username'), max_length=150)
    password = forms.CharField(
        label=_("Password"), strip=False, max_length=128,
        widget=forms.PasswordInput,
    )

    def confirm_login_allowed(self, user):
        if not user.is_staff:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',)


class UserLoginCaptchaForm(UserLoginForm):
    captcha = CaptchaField()





