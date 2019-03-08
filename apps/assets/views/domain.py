# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-05 10:45
#   FileName = domain

from django.views.generic import TemplateView, CreateView, UpdateView, DetailView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy, reverse
from django.contrib.messages.views import SuccessMessageMixin
from common.utils import get_object_or_none
from common.mixins import AdminUserRequiredMixin
from common.constant import create_success_msg, update_success_msg
from assets.models import Domain, Gateway
from assets.forms import DomainForm, GatewayForm

__all__ = ['DomainListView', 'DomainCreateView', 'DomainDetailView', 'DomainUpdateView',
           'DomainDeleteView', 'DomainGatewayListView', 'DomainGatewayCreateView',
           'DomainGatewayUpdateView', 'DomainGatewayDeleteView']


class DomainListView(AdminUserRequiredMixin, TemplateView):
    """ 域名列表 """
    template_name = 'assets/domain_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': _('Assets'),
            'action': _('Domain list'),
        }
        context.update(data)
        return context


class DomainDetailView(AdminUserRequiredMixin, DetailView):
    """ 单个域名详情 """
    model = Domain
    template_name = 'assets/domain_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': _('Assets'),
            'action': _('Domain detail'),
        }
        context.update(data)
        return context


class DomainCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    """ 创建域名 """
    model = Domain
    template_name = 'assets/domain_create_update.html'
    form_class = DomainForm
    success_url = reverse_lazy('assets:domain-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': 'Assets',
            'action': 'Create domain',
        }
        context.update(data)
        return context


class DomainUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    """ 更新域名 """
    model = Domain
    template_name = 'assets/domain_create_update.html'
    form_class = DomainForm
    success_url = reverse_lazy('assets:domain-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': 'Assets',
            'action': 'Update domain',
        }
        context.update(data)
        return context

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['name'])


class DomainDeleteView(AdminUserRequiredMixin, DeleteView):
    """ 删除域名 """
    model = Domain
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:domain-list')


class DomainGatewayListView(AdminUserRequiredMixin, SingleObjectMixin, TemplateView):
    model = Domain
    object = None
    template_name = 'assets/domain_gateway_list.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': _('Assets'),
            'action': _('Domain gateway list'),
            'object': self.get_object()
        }
        context.update(data)
        return context


class DomainGatewayCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = Gateway
    template_name = 'assets/gateway_create_update.html'
    form_class = GatewayForm

    def get_success_url(self):
        domain = self.object.domain
        return reverse('assets:domain-gateway-list', kwargs={'pk': domain.id})

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data['name'])

    def get_form(self, form_class=None):
        """ 重写表单 Domain 字段的值由Domain id来确定，而不是name """
        form = super().get_form(form_class=form_class)
        domain_id = self.kwargs.get('pk')
        domain = get_object_or_none(Domain, id=domain_id)
        if domain:
            form['domain'].initial = domain
        return form

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Create gateway'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DomainGatewayUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Gateway
    template_name = 'assets/gateway_create_update.html'
    form_class = GatewayForm

    def get_success_url(self):
        domain = self.object.domain
        return reverse('assets:domain-gateway-list',kwargs={'pk': domain.id})

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Assets'),
            'action': _('Update gateway'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class DomainGatewayDeleteView(AdminUserRequiredMixin, DeleteView):
    model = Gateway
    template_name = 'delete_confirm.html'

    def get_success_url(self):
        domain = self.object.domain
        return reverse('assets:domain-gateway-list', kwargs={'pk': domain.id})
