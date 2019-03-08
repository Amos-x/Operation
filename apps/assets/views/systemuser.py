# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-06 16:46
#   FileName = systemuser

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from common.mixins import AdminUserRequiredMixin
from common.constant import create_success_msg, update_success_msg
from assets.models import SystemUser
from assets.forms import SystemUserForm

__all__ = ['SystemUserListView', 'SystemUserCreateView', 'SystemUserDetailView',
           'SystemUserUpdateView', 'SystemUserDeleteView', 'SystemUserAssetView']


class SystemUserListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'assets/system_user_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('System user list')
        }
        kwargs.update(context)
        return context


class SystemUserDetailView(AdminUserRequiredMixin, DetailView):
    template_name = 'assets/system_user_detail.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('System user list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = SystemUser
    template_name = 'assets/system_user_create.html'
    form_class = SystemUserForm
    success_url = reverse_lazy('assets:system-user-list')

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data.get('name'))

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create system user')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = SystemUser
    template_name = 'assets/system_user_update.html'
    form_class = SystemUserForm
    success_url = reverse_lazy('assets:system-user-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data.get('name'))

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update system user'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SystemUserDeleteView(AdminUserRequiredMixin, DeleteView):
    model = SystemUser
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:system-user-list')


class SystemUserAssetView(AdminUserRequiredMixin, DetailView):
    model = SystemUser
    template_name = 'assets/system_user_asset.html'
    context_object_name = 'system_user'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('System user asset'),
        }
        kwargs.update(**context)
        return super().get_context_data(**kwargs)
