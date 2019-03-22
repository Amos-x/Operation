# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-22 17:04
#   FileName = group

from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from common.mixins import AdminUserRequiredMixin
from common.constant import create_success_msg, update_success_msg
from users.forms import UserGroupForm
from users.models import UserGroup, User


__all__ = ['UserGroupListView', 'UserGroupCreateView', 'UserGroupUpdateView', 'UserGroupDetailView',
           'UserGroupDeleteView', 'UserGroupGrantedAssetView']


class UserGroupListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_group_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User group list')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = UserGroup
    template_name = 'users/user_group_create_update.html'
    form_class = UserGroupForm
    success_url = reverse_lazy('users:user-group-list')

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Create user group')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = UserGroup
    template_name = 'users/user_group_create_update.html'
    form_class = UserGroupForm
    success_url = reverse_lazy('users:user-group-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _("Update user group")
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupDetailView(AdminUserRequiredMixin, DetailView):
    model = UserGroup
    template_name = 'users/user_group_detail.html'
    context_object_name = 'user_group'

    def get_context_data(self, **kwargs):
        users = User.objects.exclude(id__in=self.object.users.all()).exclude(role=User.ROLE_APP)
        context = {
            'app': _('Users'),
            'action': _('User group detail'),
            'users': users
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGroupDeleteView(AdminUserRequiredMixin, DeleteView):
    model = UserGroup
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('users:user-group-list')


class UserGroupGrantedAssetView(AdminUserRequiredMixin, DetailView):
    model = UserGroup
    template_name = 'users/user_group_granted_asset.html'
    context_object_name = 'user_group'
    object = None

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _("User group granted asset"),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
