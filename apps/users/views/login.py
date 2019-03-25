# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-19 17:52
#   FileName = login

import os
from django.views.generic import FormView, TemplateView, ListView
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.core.cache import cache
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.mixins import LoginRequiredMixin
from formtools.wizard.views import SessionWizardView
from users.forms import UserLoginForm, UserLoginCaptchaForm
from users.utils import redirect_user_first_login_or_index, get_login_ip, is_block_login, set_tmp_user_to_cache, \
    get_user_or_tmp_user, set_user_login_failed_count_to_cache, send_reset_password_mail
from users.tasks import write_login_log_async
from users.models import User
from common.utils import get_object_or_none
from common.mixins import AdminUserRequiredMixin, DatetimeSearchMixin


__all__ = ['UserLoginView', 'UserLogoutView', 'UserResetPasswordView', 'UserForgotPasswordView',
           'UserForgotPasswordSuccessView', 'UserResetPasswordSuccessView', 'LoginLogListView']


@method_decorator(sensitive_post_parameters(), name='dispatch')
@method_decorator(never_cache, name='dispatch')
@method_decorator(csrf_protect, name='dispatch')
class UserLoginView(FormView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    form_class_captcha = UserLoginCaptchaForm    # 验证码表单
    redirect_field_name = 'next'
    key_prefix_limit = "_LOGIN_LIMIT_{}_{}"    # 缓存key，个人用户登录次数限制的key，后跟username+ip
    key_prefix_block = "_LOGIN_BLOCK_{}"    # 缓存key，是否已限制用户登录，后跟username
    key_prefix_captcha = '_LOGIN_INVALID_{}'    # 缓存key，个人用户是否需要验证码登录，后跟ip

    def get(self, request, *args, **kwargs):
        """ get请求，判断用户是否已验证，并返回登录页或首页"""
        if request.user.is_staff:
            return redirect(redirect_user_first_login_or_index(
                request, self.redirect_field_name
            ))
        request.session.set_test_cookie()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """ post请求，进行登录验证 """
        ip = get_login_ip(request)
        username = self.request.POST.get('username')
        key_limit = self.key_prefix_limit.format(username, ip)
        if is_block_login(key_limit):
            return self.render_to_response(self.get_context_data(block_login=True))
        return super().post(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'demo_mode': os.environ.get("DEMO_MODE"),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """ 表单验证通过，返回成功url """
        if not self.request.session.test_cookie_worked():
            return HttpResponse(_('Please enable cookies and try again.'))

        set_tmp_user_to_cache(self.request, form.get_user())
        return redirect(self.get_success_url())

    def get_success_url(self):
        """ 获取成功跳转的url """
        user = get_user_or_tmp_user(self.request)
        auth_login(self.request,user)
        data = {
            'username': self.request.user.username,
            'status': True
        }
        self.write_login_log(data)
        return redirect_user_first_login_or_index(self.request, self.redirect_field_name)

    def write_login_log(self, data):
        """ 写入登录历史 """
        login_ip = get_login_ip(self.request)
        user_agent = self.request.META.get('HTTP_USER_AGENT', '')
        tmp_data = {
            'ip': login_ip,
            'type': 'w',
            'user_agent': user_agent
        }
        data.update(tmp_data)
        write_login_log_async.delay(**data)

    def form_invalid(self, form):
        """ 表单验证不通过 """
        username = form.cleaned_data.get('username')
        data = {
            'username': username,
            'status': False
        }
        self.write_login_log(data)

        # limit user login failed count
        ip = get_login_ip(self.request)
        key_limit = self.key_prefix_limit.format(username, ip)
        key_block = self.key_prefix_block.format(username)
        set_user_login_failed_count_to_cache(key_limit, key_block)

        # 设置需要使用验证码的缓存key，然后切换表单为验证码表单
        cache.set(self.key_prefix_captcha.format(ip), 1, 3600)
        old_form = form
        form = self.form_class_captcha(data=form.data)
        form._errors = old_form.errors
        return super().form_invalid(form)

    def get_form_class(self):
        """ 获取表单类，查看缓存是否有需要使用验证码的key """
        ip = get_login_ip(self.request)
        if cache.get(self.key_prefix_captcha.format(ip)):
            return self.form_class_captcha
        else:
            return self.form_class


@method_decorator(never_cache, name='dispatch')
class UserLogoutView(TemplateView):
    template_name = 'flash_message_standalone.html'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'title': _("Logout success"),
            'message': _('Logout success, return login page'),
            'interval': 1,
            'redirect_url': reverse_lazy('users:login'),
            'auto_redirect': True,
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserForgotPasswordView(TemplateView):
    template_name = 'users/forgot_password.html'

    def post(self, request):
        email = request.POST.get('email')
        user = get_object_or_none(User, email=email)
        if not user:
            return self.get(request, errors=_('Email address invalid, please input again'))
        else:
            send_reset_password_mail(user)
            return HttpResponseRedirect(reverse_lazy('users:forgot-password-sendmail-success'))


class UserForgotPasswordSuccessView(TemplateView):
    template_name = 'flash_message_standalone.html'

    def get_context_data(self, **kwargs):
        context = {
            'title': _('Send reset password message'),
            'messages': _('Send reset password mail success, login your mail box and follow it'),
            'redirect_url': reverse_lazy('users:login'),
            'auto_redirect': True
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserResetPasswordView(TemplateView):
    template_name = 'users/reset_password.html'

    def get(self, request, *args, **kwargs):
        token = request.GET.get('token')
        user = User.validate_reset_token(token)
        # TODO： 检查密码安全策略
        if not user:
            kwargs.update({'errors': _('Token invalid or expired')})
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        password_confirm = request.POST.get('password-confirm')
        token = request.GET.get('token')

        if password != password_confirm:
            return self.get(request, errors=_("Password not same"))

        user = User.validate_reset_token(token)
        if not user:
            return self.get(request, errors=_('Token invalid or expired'))

        # TODO: 验证密码策略
        user.set_password(password)
        user.save()
        return HttpResponseRedirect(reverse_lazy('users:reset-password-success'))


class UserResetPasswordSuccessView(TemplateView):
    template_name = 'flash_message_standalone.html'

    def get_context_data(self, **kwargs):
        context = {
            'titile': _('Reset password success'),
            'messages': _('Reset password success, return to login page'),
            'redirect_url': reverse_lazy('users:login'),
            'auto_redirect': True
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class LoginLogListView(AdminUserRequiredMixin, DatetimeSearchMixin, ListView):
    pass

