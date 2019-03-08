# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-07 16:40
#   FileName = label

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from common.constant import create_success_msg, update_success_msg
from common.mixins import AdminUserRequiredMixin
from assets.forms import LabelForm


__all__ = ['LabelListView', 'LabelCreateView', 'LabelUpdateView', 'LabelDeleteView']


class LabelListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'assets/label_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Asstes'),
            'action': _('Label list')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class LabelCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = LabelForm
    template_name = 'assets/label_create_update.html'
    success_url = reverse_lazy('assets:label-list')

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data.get('name', ''))

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create label'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class LabelUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = LabelForm
    template_name = 'assets/label_create_update.html'
    success_url = reverse_lazy('assets:label-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data.get('name', ''))

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update label')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class LabelDeleteView(AdminUserRequiredMixin, DeleteView):
    model = LabelForm
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:label-list')

