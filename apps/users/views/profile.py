# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-25 17:25
#   FileName = profile

from django.views.generic import TemplateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.http import HttpResponse
from users.models import User
from users.forms import UserProfileForm, UserPasswordForm, UserPublicKeyForm
from assets.utils import ssh_key_gen


__all__ = ['UserProfileView', 'UserProfileUpdateView', 'UserPasswordUpdateView',
           'UserPublicKeyUpdateView', 'UserPublicKeyGenerateView']


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_profile.html'

    def get_context_data(self, **kwargs):
        # mfa_setting = Setting.objects.filter(name='SECURITY_MFA_AUTH').first()
        context = {
            'app': _('Users'),
            'action': _('Profile'),
            # 'mfa_setting': mfa_setting.cleaned_value if mfa_setting else False,
            'mfa_setting': False,
            'user': self.request.user
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'users/user_profile_update.html'
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        """ 这个updateview所对应的url没有pk，必须重写get_object，指定obj """
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {
            'app': _('User'),
            'action': _('Profile setting'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserPasswordUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_password_update.html'
    form_class = UserPasswordForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Users',
            'action': 'Update user password',
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def get_success_url(self):
        logout(self.request)
        return super().get_success_url()


class UserPublicKeyUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_pubkey_update.html'
    form_class = UserPublicKeyForm
    success_url = reverse_lazy('users:user-profile')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Users',
            'action': 'Public key update '
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserPublicKeyGenerateView(LoginRequiredMixin, View):
    """ 自动生成访问的私钥，公钥，并保存，只提供下载私钥 """
    def get(self, request, *args, **kwargs):
        private_key, public_key = ssh_key_gen(username=request.user.username, hostname='operation')
        request.user.public_key = public_key
        request.user.save()
        response = HttpResponse(private_key, content_type='text/plain')
        filename = "{0}-operation.pem".format(request.user.username)
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)
        return response
