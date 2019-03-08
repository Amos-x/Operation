# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-02 14:58
#   FileName = asset

from django import forms
from django.utils.translation import gettext_lazy as _
from assets.models import Asset, AdminUser


__all__ = ['AssetCreateForm', 'AssetUpdateForm', 'AssetBulkUpdateForm']


class AssetCreateForm(forms.ModelForm):
    """ 创建资产表单 """
    class Meta:
        model = Asset
        fields = [
            'hostname', 'ip', 'public_ip', 'port', 'comment',
            'nodes', 'is_active', 'admin_user', 'labels', 'platform',
            'domain', 'protocol',
        ]
        widgets = {
            'nodes': forms.SelectMultiple(attrs={'class': 'select2', 'data-placeholder': _("Nodes")}),
            'admin_user': forms.Select(attrs={'class': 'select2', 'data-placeholder': _('Admin user')}),
            'labels': forms.SelectMultiple(attrs={'class': 'select2', 'data-placeholder': _('Label')}),
            'port': forms.TextInput(),
            'domain': forms.Select(attrs={'class': 'select2', 'data-placeholder': _('Domain')}),
        }
        labels = {'nodes': _('Node')}
        help_texts = {
            'hostname': '* required',
            'ip': '* required',
            'port': '* required',
            'admin_user': _(
                'root or other NOPASSWD sudo privilege user existed in asset,'
                'If asset is windows or other set any one, more see admin user left menu'
            ),
            'platform': _('* required Must set exact system platform, Windows, Linux ... '),
            'domain': _("If your have some network not connect with each other, you can set domain")
        }


class AssetUpdateForm(forms.ModelForm):
    """  资产更新表单 """
    class Meta:
        model = Asset
        fields = [
            'hostname', 'ip', 'port', 'nodes', 'is_active', 'platform',
            'public_ip', 'number', 'comment', 'admin_user', 'labels',
            'domain', 'protocol',
        ]
        widgets = {
            'nodes': forms.SelectMultiple(attrs={'class': 'select2', 'data-placeholder': _("Nodes")}),
            'admin_user': forms.Select(attrs={'class': 'select2', 'data-placeholder': _('Admin user')}),
            'labels': forms.SelectMultiple(attrs={'class': 'select2', 'data-placeholder': _('Label')}),
            'port': forms.TextInput(),
            'domain': forms.Select(attrs={'class': 'select2', 'data-placeholder': _('Domain')}),
        }
        labels = {'nodes': _('Node')}
        help_texts = {
            'hostname': '* required',
            'ip': '* required',
            'port': '* required',
            'admin_user': _(
                'root or other NOPASSWD sudo privilege user existed in asset,'
                'If asset is windows or other set any one, more see admin user left menu'
            ),
            'platform': _('* required Must set exact system platform, Windows, Linux ... '),
            'domain': _("If your have some network not connect with each other, you can set domain")
        }


class AssetBulkUpdateForm(forms.ModelForm):
    """ 资产批量更新表单 """
    assets = forms.ModelMultipleChoiceField(
        required=True, help_text='* required', label=_('Select assets'),
        queryset=Asset.objects.all(), widget=forms.SelectMultiple(
            attrs={
                'class': 'select2',
                'data-placeholder': _('Select assets')
            }
        )
    )
    port = forms.IntegerField(
        label=_('Port'), required=False, min_value=1, max_value=65536,
    )
    admin_user = forms.ModelChoiceField(
        required=True, queryset=AdminUser.objects.all(), label=_('Admin user'),
        widget=forms.Select(
            attrs={
                'class': 'select2',
                'data-placeholder': _('Admin user')
            }
        )
    )

    class Meta:
        model = Asset
        fields = [
            'assets', 'port', 'admin_user', 'labels', 'nodes', 'platform'
        ]
        widgets = {
            'labels': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Label')
            }),
            'nodes': forms.SelectMultiple(attrs={
                'class': 'select2', 'data-placeholder': _('Node')
            })
        }

    def save(self, commit=True):
        """
        重写save函数
        因为批量更新资产的数据不统一，字段只能为空，所以提交时，不更新空值
         """
        changed_fields = []
        for field in self._meta.fields:
            if self.data.get(field) not in [None, '']:
                changed_fields.append(field)

        cleaned_data = {k: v for k,v in self.cleaned_data.items() if k in changed_fields}
        assets = cleaned_data.pop('assets')
        labels = cleaned_data.pop('labels', [])
        nodes = cleaned_data.pop('nodes')
        assets = Asset.objects.filter(id__in=[asset.id for asset in assets])
        assets.update(**cleaned_data)

        if labels:
            for label in labels:
                label.label_assets.add(*tuple(assets))
        if nodes:
            for node in nodes:
                node.node_assets.add(*tuple(assets))
        return assets
