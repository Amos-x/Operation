# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com

from django.views.generic import UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import ugettext_lazy as _
from common.mixins import AdminUserRequiredMixin
from common.models import Setting
from common.forms import BasicSettingForm, EmailSettingForm, SecuritySettingForm

# Create your views here.


class BasicSettingView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Setting
    form_class = BasicSettingForm
    template_name = 'common/basic_setting.html'
    success_url = reverse_lazy('common:basic-setting')
    success_message = _('Update setting successfully, please restart program')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Common'),
            'action': _('Basic setting')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class EmailSettingView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Setting
    form_class = EmailSettingForm
    template_name = 'common/email_setting.html'
    success_url = reverse_lazy('common:email-setting')
    success_message = _('Update setting successfully, please restart program')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Common'),
            'action': _('Email setting')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SecuritySettingView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Setting
    form_class = SecuritySettingForm
    template_name = 'common/security_setting.html'
    success_url = reverse_lazy('common:security-setting')
    success_message = _('Update setting successfully, please restart program')

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Common'),
            'action': _('Security setting')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
