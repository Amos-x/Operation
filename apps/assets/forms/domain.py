# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-05 14:19
#   FileName = domain


from django import forms
from django.utils.translation import gettext_lazy as _
from assets.models import Domain, Asset, Gateway
from .user import PasswordAndKeyAuthForm


__all__ = ['DomainForm', 'GatewayForm']


class DomainForm(forms.ModelForm):

    assets = forms.ModelMultipleChoiceField(
        queryset=Asset.objects.all(), label=_("Asset"), required=False,
        widget=forms.SelectMultiple(attrs={
            'class': 'select2', 'data-placeholder': _('Select assets')
                })
    )

    class Meta:
        model = Domain
        fields = ['name', 'comment', 'assets']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            initial = kwargs.get('initial', {})
            initial['assets'] = kwargs['instance'].domain_assets.all()
        super().__init__(*args,**kwargs)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        assets = self.cleaned_data['assets']
        instance.domain_assets.set(assets)
        return instance


class GatewayForm(PasswordAndKeyAuthForm):
    class Meta:
        model = Gateway
        fields = [
            'name', 'ip', 'port', 'username', 'protocol', 'domain', 'password',
            'private_key_file', 'is_active', 'comment'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Name')}),
            'username': forms.TextInput(attrs={'placeholder': _('Username')})
        }
        help_texts = {
            'name': '* required',
            'username': '* required'
        }

    def save(self, commit=True):
        """ 因为定义了自定义字段，所以要重写save函数 """
        instance = super().save()
        password = self.cleaned_data.get('password')
        private_key, public_key = super().gen_keys()
        instance.set_auth(password=password, private_key=private_key)
        return instance
