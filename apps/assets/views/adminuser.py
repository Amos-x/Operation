# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-06 15:07
#   FileName = adminuser

from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, CreateView, UpdateView, DeleteView, DetailView, ListView
from django.views.generic.detail import SingleObjectMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from common.mixins import AdminUserRequiredMixin
from common.constant import create_success_msg, update_success_msg
from assets.models import AdminUser, Node
from assets.forms import AdminUserForm


__all__ = ['AdminUserListView', 'AdminUserDetailView', 'AdminUserCreateView',
           'AdminUserUpdateView', 'AdminUserDeleteView', 'AdminUserAssetView']


class AdminUserListView(AdminUserRequiredMixin, TemplateView):
    # model = AdminUser
    template_name = 'assets/admin_user_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Assets',
            'action': 'Admin user list',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserDetailView(AdminUserRequiredMixin, DetailView):
    model = AdminUser
    template_name = 'assets/admin_user_detail.html'
    context_object_name = 'admin_user'
    object = None

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user detail'),
            'node': Node.objects.all()
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = AdminUser
    form_class = AdminUserForm
    template_name = 'assets/admin_user_create_update.html'
    success_url = reverse_lazy('assets:admin-user-list')

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user create')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AdminUser
    form_class = AdminUserForm
    template_name = 'assets/admin_user_create_update.html'
    success_url = reverse_lazy('assets:admin-user-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user update')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class AdminUserDeleteView(AdminUserRequiredMixin, DeleteView):
    model = AdminUser
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:admin-user-list')


class AdminUserAssetView(AdminUserRequiredMixin, SingleObjectMixin, ListView):
    model = AdminUser
    template_name = 'assets/admin_user_assets.html'
    context_object_name = 'admin_user'
    object = None

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=AdminUser.objects.all())
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        self.queryset = self.object.asset_set.all()
        return self.queryset

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Admin user detail'),
            'total_amount': self.object.assets_amount,
            'unreachable_amount': len([asset for asset in self.queryset if asset.is_connective is False])
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
