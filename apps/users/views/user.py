# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 17:59
#   FileName = user

from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from common.mixins import AdminUserRequiredMixin
from common.utils import get_logger
from common.constant import create_success_msg, update_success_msg
from users.models import User, UserGroup
from users.forms import UserCreateUpdateForm
from users.signals import post_user_create
# from users.utils import get_password_check_rules


__all__ = ['UserListView', 'UserDetailView', 'UserCreateView', 'UserUpdateView']
logger = get_logger(__name__)


class UserListView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_list.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User list'),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserDetailView(AdminUserRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user_object'

    def get_context_data(self, **kwargs):
        groups = UserGroup.objects.exclude(id__in=self.object.groups.all())
        context = {
            'app': _('Users'),
            'action': _("User detail"),
            'groups': groups,
            # 'unblock': is_need_unblock(key_block)
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('user:user-list')

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('Create user')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.created_by = self.request.user.username or 'System'
        user.save()
        # 发送创建用户信号
        post_user_create.send(self.__class__, user=user)
        return super().form_valid(form)


class UserUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'users/user_update.html'
    success_url = reverse_lazy('users:user-list')

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['name'])

    def get_context_data(self, **kwargs):
        # check_rules, min_length = get_password_check_rules()
        context = {
            'app': _('Users'),
            'action': _('Update user'),
            # TODO: 密码验证这里是通过前端js进行限制。
            # 'password_check_rules': check_rules,
            # 'min_length': min_length
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        password = form.cleaned_data.get('password')
        if not password:
            return super().form_valid(form)

        # TODO: 密码规则验证
        # is_ok = check_password_rules(password)
        # if not is_ok:
        #     form.add_error(
        #         "password", _("* Your password does not meet the requirements")
        #     )
        #     return self.form_invalid(form)
        return super().form_valid(form)


class UserDeleteView(AdminUserRequiredMixin, DeleteView):
    model = User
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('users:user-list')
