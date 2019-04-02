# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 20:21
#   FileName = user

from django import forms
from django.utils.translation import ugettext_lazy as _
from assets.utils import validate_ssh_public_key
from users.models import User


__all__ = ['UserCreateUpdateForm', 'FileForm', 'UserBulkUpdateForm', 'UserProfileForm', 'UserPasswordForm',
           'UserPublicKeyForm']


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


class FileForm(forms.Form):
    file = forms.FileField()


class UserBulkUpdateForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        required=True, help_text=_("* required"), label=_('Select users'),
        queryset=User.objects.all(), widget=forms.SelectMultiple(
            attrs={
                'class': 'select2',
                'data-placeholder': _('Select users')
            }
        )
    )

    class Meta:
        model = User
        fields = ['users', 'role', 'groups', 'date_expired']
        widgets = {
            'groups': forms.SelectMultiple(
                attrs={
                    'class': 'select2',
                    'data-placeholder': _('Select users')
                }
            )
        }

    def save(self, commit=True):
        """ 重写save函数，进行批量更新 """
        changed_fields = []
        for field in self._meta.fields:
            if self.data.get(field) is not None:
                changed_fields.append(field)

        cleaned_data = {k: v for k, v in self.cleaned_data.items() if k in changed_fields}
        users = cleaned_data.pop('users', '')
        groups = cleaned_data.pop('groups', [])
        users = User.objects.filter(id__in=[user.id for user in users])
        users.update(**cleaned_data)
        if groups:
            for user in users:
                user.groups.set(groups)
        return users


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username', 'name', 'email',
            'wechat', 'phone',
        ]
        help_texts = {
            'username': '* required',
            'name': '* required',
            'email': '* required',
        }


class UserPasswordForm(forms.Form):
    old_password = forms.CharField(
        max_length=128, label=_("Old password"), required=True,
        widget=forms.PasswordInput
    )
    new_password = forms.CharField(
        max_length=128, label=_('New password'), required=True,
        min_length=6, widget=forms.PasswordInput
    )
    confirm_password = forms.CharField(
        min_length=6, max_length=128, label=_('Confirm password'),
        required=True, widget=forms.PasswordInput
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        old_password = self.cleaned_data['old_password']
        if not self.instance.check_password(old_password):
            raise forms.ValidationError(_('Old password error'))
        return old_password

    def clean_confirm_password(self):
        new_password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_password']

        if new_password != confirm_password:
            raise forms.ValidationError(_('Password does not match'))
        return confirm_password

    def save(self):
        password = self.cleaned_data['new_password']
        self.instance.set_password(password)
        self.instance.save()
        return self.instance


class UserPublicKeyForm(forms.Form):
    public_key = forms.CharField(
        max_length=5000, label=_('ssh public key'), required=False,
        help_text=_("Paste your id_rsa.pub here"),
        widget=forms.Textarea(attrs={
            'placeholder': _('ssh-rsa AAAAA...')
        })
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)

    def clean_public_key(self):
        public_key = self.cleaned_data['public_key']
        if self.instance.public_key and public_key == self.instance.public_key:
            msg = _('Public key should not be same as your old one')
            raise forms.ValidationError(msg)
        if public_key and not validate_ssh_public_key(public_key):
            raise forms.ValidationError(_("Not a valid ssh public key"))
        return public_key

    def save(self):
        public_key = self.cleaned_data['public_key']
        if public_key:
            self.instance.public_key = public_key
            self.instance.save()
        return self.instance
