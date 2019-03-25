# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-22 17:08
#   FileName = grou

from django import forms
from django.utils.translation import ugettext_lazy as _
from users.models import User, UserGroup


__all__ = ['UserGroupForm']


class UserGroupForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.exclude(role=User.ROLE_APP), label=_("User"),
        widget=forms.SelectMultiple(attrs={'class': 'select2', 'data-placeholder': _('Select users')}),
        required=False
    )

    def __init__(self, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'users': instance.users.all(),
            })
            kwargs['initial'] = initial
        super().__init__(**kwargs)

    def save(self, commit=True):
        group = super().save(commit=commit)
        users = self.cleaned_data['users']
        group.users.set(users)
        return group

    class Meta:
        model = UserGroup
        fields = ['name', 'users', 'comment']
        help_texts = {
            'name': '* required'
        }
