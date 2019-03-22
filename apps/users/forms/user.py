# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 20:21
#   FileName = user

from django import forms
from users.models import User


__all__ = ['UserCreateUpdateForm']


class UserCreateUpdateForm(forms.ModelForm):
    role_choices = ((k, v) for k, v in User.ROLE_CHOICES if k != User.ROLE_APP)
    password = forms.CharField(
        label=_('Password'), widget=forms.PasswordInput, max_length=128, strip=False, required=False
    )
    role = forms.ChoiceField(
        choices=role_choices, required=True, initial=User.ROLE_USER, label=_('Role')
    )
    public_key = forms.CharField(
        label=_('ssh public key'), max_length=5000, required=False,
        widget=forms.Textarea(attrs={'placeholder': _('ssh-rsa AAAA...')}),
        help_text=_('Paste user id_rsa.pub here')
    )

    class Meta:
        model = User
        fields = [
            'username', 'name', 'email', 'groups', 'role', 'wechat',
            'phone', 'date_expired', 'comment'
        ]
        widgets = {
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'select2',
                    'data-placeholder': _('Join user group')
                }
            )
        }
        help_texts = {
            'username': _('* required'),
            'name': _('* required'),
            'email': _('* required'),
        }

    def save(self, commit=True):
        password_raw = self.cleaned_data.get('password')
        public_key = self.cleaned_data.get('password')
        user = super().save(commit=commit)
        if password_raw:
            user.set_password(password_raw)
            user.save()
        if public_key:
            user.public_key = public_key
            user.save()
        return user
