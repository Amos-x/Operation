# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 17:59
#   FileName = user

import uuid
import json
import csv
import codecs
import chardet
from io import StringIO
from django.contrib import messages
from django.views.generic import TemplateView, DetailView, UpdateView, CreateView, DeleteView, View, FormView
from django.utils.translation import ugettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.shortcuts import redirect
from common.mixins import AdminUserRequiredMixin, JSONResponseMixin
from common.utils import get_logger, data_to_csv_http_response, get_object_or_none, is_uuid
from common.constant import create_success_msg, update_success_msg
from users.models import User, UserGroup
from users.forms import UserCreateUpdateForm, FileForm, UserBulkUpdateForm
from users.signals import post_user_create
from users.utils import is_need_unblock


__all__ = ['UserListView', 'UserDetailView', 'UserCreateView', 'UserUpdateView', 'UserExportView', 'UserBulkImportView',
           'UserDeleteView', 'UserBulkUpdateView', 'UserGrantedAssetView']
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
    key_prefix_block = "_LOGIN_BLOCK_{}"    # 缓存key，是否已限制用户登录，后跟username

    def get_context_data(self, **kwargs):
        user = self.get_object()
        key_block = self.key_prefix_block.format(user.username)
        groups = UserGroup.objects.exclude(id__in=self.object.groups.all())
        context = {
            'app': _('Users'),
            'action': _("User detail"),
            'groups': groups,
            'unblock': is_need_unblock(key_block)
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserCreateUpdateForm
    template_name = 'users/user_create.html'
    success_url = reverse_lazy('users:user-list')

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


@method_decorator(csrf_exempt, name='dispatch')
class UserExportView(View):
    def get(self, request):
        fields = [User._meta.get_field(name) for name in ['id', 'name', 'username', 'email', 'role', 'wechat', 'phone',
                                                          'is_active', 'comment']]
        spm = request.GET.get('spm', '')
        users_id = cache.get(spm, [])
        filename = 'users-{}.csv'.format(timezone.localtime(timezone.now()).strftime('%Y-%m-$d_%H-%M-%S'))
        data = []
        users = User.objects.filter(id__in=users_id)

        header = [field.verbose_name for field in fields]
        header.append(_('User groups'))
        data.append(header)
        for user in users:
            groups = ','.join([group.name for group in user.groups.all()])
            linedata = [getattr(user, field.name) for field in fields]
            linedata.append(groups)
            data.append(linedata)

        return data_to_csv_http_response(filename=filename, data=data)

    def post(self, request):
        try:
            users_id = json.loads(request.body).get('users_id', [])
        except ValueError:
            return HttpResponse('Json object not valid', status=400)
        spm = uuid.uuid4().hex
        cache.set(spm, users_id, 300)
        url = reverse_lazy('users:user-export') + '?spm={}'.format(spm)
        return JsonResponse({'redirect': url})


class UserBulkImportView(AdminUserRequiredMixin, JSONResponseMixin, FormView):
    form_class = FileForm

    def form_invalid(self, form):
        """ 自定义表单验证不通过的返回 """
        try:
            error_message = form.errors.values()[-1][-1]
        except Exception as e:
            error_message = _('Invalid file')
        data = {
            'success': False,
            'msg': error_message
        }
        return self.render_json_response(data)

    def form_valid(self, form):
        """ 验证表单并读取数据进行创建或更新 """
        # TODO： 方法太长，需要优化
        f = form.cleaned_data['file']
        det_result = chardet.detect(f.read())
        f.seek(0)  # reset file seek index
        data = f.read().decode(det_result['encoding']).strip(codecs.BOM_UTF8.decode())
        csv_file = StringIO(data)
        reader = csv.reader(csv_file)
        csv_data = [row for row in reader]
        header_ = csv_data[0]
        fields = [
            User._meta.get_field(name)
            for name in [
                'id', 'name', 'username', 'email', 'role',
                'wechat', 'phone', 'is_active', 'comment',
            ]
        ]
        mapping_reverse = {field.verbose_name: field.name for field in fields}
        mapping_reverse[_('User groups')] = 'groups'
        attr = [mapping_reverse.get(n, None) for n in header_]
        if None in attr:
            data = {'valid': False,
                    'msg': 'Must be same format as '
                           'template or export file'}
            return self.render_json_response(data)

        created, updated, failed = [], [], []
        for row in csv_data[1:]:
            if set(row) == {''}:
                continue
            user_dict = dict(zip(attr, row))
            id_ = user_dict.pop('id')
            for k, v in user_dict.items():
                if k in ['is_active']:
                    if v.lower() == 'false':
                        v = False
                    else:
                        v = bool(v)
                elif k == 'groups':
                    groups_name = v.split(',')
                    v = UserGroup.objects.filter(name__in=groups_name)
                else:
                    continue
                user_dict[k] = v
            user = get_object_or_none(User, id=id_) if id_ and is_uuid(id_) else None
            if not user:
                try:
                    with transaction.atomic():
                        groups = user_dict.pop('groups')
                        user = User.objects.create(**user_dict)
                        user.groups.set(groups)
                        created.append(user_dict['username'])
                        post_user_create.send(self.__class__, user=user)
                except Exception as e:
                    failed.append('%s: %s' % (user_dict['username'], str(e)))
            else:
                for k, v in user_dict.items():
                    if k == 'groups':
                        user.groups.set(v)
                        continue
                    if v:
                        setattr(user, k, v)
                try:
                    user.save()
                    updated.append(user_dict['username'])
                except Exception as e:
                    failed.append('%s: %s' % (user_dict['username'], str(e)))

        data = {
            'created': created,
            'created_info': 'Created {}'.format(len(created)),
            'updated': updated,
            'updated_info': 'Updated {}'.format(len(updated)),
            'failed': failed,
            'failed_info': 'Failed {}'.format(len(failed)),
            'valid': True,
            'msg': 'Created: {}. Updated: {}, Error: {}'.format(
                len(created), len(updated), len(failed))
        }
        return self.render_json_response(data)


class UserBulkUpdateView(AdminUserRequiredMixin, TemplateView):
    template_name = 'users/user_bulk_update.html'
    form_class = UserBulkUpdateForm
    success_url = reverse_lazy('users:user-list')
    success_message = _('Bulk update user success')
    id_list = None
    form = None

    def get(self, request, *args, **kwargs):
        users_id = self.request.GET.get('users_id', '')
        self.id_list = [i for i in users_id.split(',')]
        if kwargs.get('form'):
            self.form = kwargs['form']
        elif users_id:
            self.form = self.form_class(initial={'users': self.id_list})
        else:
            self.form = self.form_class
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, self.success_message)
            return redirect(reverse_lazy('users:user-list'))
        else:
            return self.get(self, request, form=form, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = {
            'app': 'Users',
            'action': 'Bulk update users',
            'form': self.form,
            'users_selected': self.id_list
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class UserGrantedAssetView(AdminUserRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_granted_asset.html'

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Users'),
            'action': _('User granted assets')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)
