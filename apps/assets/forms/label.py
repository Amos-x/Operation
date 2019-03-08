# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-07 16:44
#   FileName = label

from django import forms
from django.utils.translation import gettext_lazy as _
from assets.models import Label, Asset


__all__ = ['LabelForm']


class LabelForm(forms.ModelForm):
    assets = forms.ModelMultipleChoiceField(
        required=False, label=_('Assets'), queryset=Asset.objects.all(),
        widget=forms.SelectMultiple(attrs={
            'class': 'select2', 'data-placeholder': _('Select asset')
        })
    )

    class Meta:
        model = Label
        fields = ['name', 'value', 'comment', 'assets']

    def __init__(self, *args, **kwargs):
        if kwargs.get('instance', None):
            initial = kwargs.get('initial', {})
            initial['assets'] = kwargs['instance'].label_assets.all()
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=commit)
        assets = self.cleaned_data.get('assets')
        instance.label_assets.set(assets)
        return instance

