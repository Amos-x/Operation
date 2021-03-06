# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-01 17:20
#   FileName = asset

import logging
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.shortcuts import redirect
from common.mixins import AdminUserRequiredMixin
from common.utils import get_object_or_none
from common.constant import create_success_msg, update_success_msg
from assets.models import Node, Label, SystemUser, Asset
from assets import forms


__all__ = ['AssetListView', 'UserAssetListView', 'AssetCreateView', 'AssetDeleteView', 'AssetDetailView',
           'AssetUpdateView', 'AssetBulkUpdateView', 'AssetExportView', 'BulkImportAssetView']


class AssetListView(AdminUserRequiredMixin, TemplateView):
    """ 管理员资产列表 """
    template_name = 'assets/asset_list.html'

    def get_context_data(self, **kwargs):
        Node.root()
        data = {
            'app': _('Assets'),
            'action': _('Asset list'),
            'labels': Label.objects.all().order_by('name'),
            'nodes': Node.objects.all().order_by('-key'),
        }
        context = super().get_context_data(**kwargs)
        context.update(data)
        return context


class UserAssetListView(LoginRequiredMixin, TemplateView):
    """ 用户资产列表 """
    template_name = 'assets/user_asset_list.html'

    def get_context_data(self, **kwargs):
        data = {
            'action': _('My assets'),
            'system_users': SystemUser.objects.all(),
        }
        context = super().get_context_data(**kwargs)
        context.update(data)
        return data


class AssetCreateView(AdminUserRequiredMixin, SuccessMessageMixin, CreateView):
    """ 管理员创建资产 """
    model = Asset
    form_class = forms.AssetCreateForm
    template_name = 'assets/asset_create.html'
    success_message = reverse_lazy('assets:asset-list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        node_id = self.request.GET.get("node_id")
        if node_id:
            node = get_object_or_none(Node, id=node_id)
        else:
            node = Node.root()
        form['nodes'].initial = node
        return form

    def get_success_message(self, cleaned_data):
        return create_success_msg.format(name=cleaned_data['hostname'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': _('Assets'),
            'action': _('Create asset'),
        }
        context.update(data)
        return context


class AssetDeleteView(AdminUserRequiredMixin, DeleteView):
    """ 管理员删除资产"""
    model = Asset
    template_name = 'delete_confirm.html'
    success_url = reverse_lazy('assets:asset-list')


class AssetUpdateView(AdminUserRequiredMixin, SuccessMessageMixin, UpdateView):
    """ 管理员更新资产信息 """
    model = Asset
    form_class = forms.AssetUpdateForm
    template_name = 'assets/asset_update.html'
    success_url = reverse_lazy('assets:asset-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        data = {
            'app': _('Assets'),
            'action': _('Update asset'),
        }
        context.update(data)
        return context

    def get_success_message(self, cleaned_data):
        return update_success_msg.format(name=cleaned_data['hostname'])


class AssetBulkUpdateView(AdminUserRequiredMixin, ListView):
    """ 管理员批量更新资产 """
    model = Asset
    form_class = forms.AssetBulkUpdateForm
    template_name = 'assets/asset_bulk_update.html'
    success_url = reverse_lazy('assets:asset-list')
    id_list = None
    form = None

    def get(self, request, *args, **kwargs):
        assets_id = self.request.GET.get('assets_id')
        self.id_list = [i for i in assets_id.split(',')]

        if kwargs.get('form'):
            self.form = kwargs.get('form')
        elif assets_id:
            self.form = self.form_class(initial={'assets': self.id_list})
        else:
            self.form = self.form_class()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(self.success_url)
        else:
            self.get(request, form=form, *args, **kwargs)

    def get_context_data(self, **kwargs):
        data = {
            'app': _('Assets'),
            'action': _('Bulk update asset'),
            'form': self.form,
            'assets_selected': self.id_list,
        }
        context = super().get_context_data(**kwargs)
        context.update(data)
        return context


class AssetDetailView(DetailView):
    """ 资产单例详情视图 """
    model = Asset
    template_name = 'assets/asset_detail.html'
    context_object_name = 'asset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        nodes_remain = Node.objects.exclude(node_assets=self.object)
        data = {
            'app': _('Assets'),
            'action': _('Asset detail'),
            'nodes_remain': nodes_remain
        }
        context.update(data)
        return context


# class BulkImportAssetView(AdminUserRequiredMixin, JSONResponseMixin, FormView):
#     """ 资产从csv文件批量导入 """
#     form_class = forms.FileForm
#
#     def form_valid(self, form):
#         node_id = self.request.GET.get("node_id")
#         node = get_object_or_none(Node, id=node_id) if node_id else Node.root()
#         f = form.cleaned_data['file']
#         det_result = chardet.detect(f.read())
#         f.seek(0)  # reset file seek index
#
#         file_data = f.read().decode(det_result['encoding']).strip(codecs.BOM_UTF8.decode())
#         csv_file = StringIO(file_data)
#         reader = csv.reader(csv_file)
#         csv_data = [row for row in reader]
#         fields = [
#             field for field in Asset._meta.fields
#             if field.name not in [
#                 'date_created'
#             ]
#         ]
#         header_ = csv_data[0]
#         mapping_reverse = {field.verbose_name: field.name for field in fields}
#         attr = [mapping_reverse.get(n, None) for n in header_]
#         if None in attr:
#             data = {'valid': False,
#                     'msg': 'Must be same format as '
#                            'template or export file'}
#             return self.render_json_response(data)
#
#         created, updated, failed = [], [], []
#         assets = []
#         for row in csv_data[1:]:
#             if set(row) == {''}:
#                 continue
#
#             asset_dict_raw = dict(zip(attr, row))
#             asset_dict = dict()
#             for k, v in asset_dict_raw.items():
#                 v = v.strip()
#                 if k == 'is_active':
#                     v = False if v in ['False', 0, 'false'] else True
#                 elif k == 'admin_user':
#                     v = get_object_or_none(AdminUser, name=v)
#                 elif k in ['port', 'cpu_count', 'cpu_cores']:
#                     try:
#                         v = int(v)
#                     except ValueError:
#                         v = ''
#                 elif k == 'domain':
#                     v = get_object_or_none(Domain, name=v)
#
#                 if v != '':
#                     asset_dict[k] = v
#
#             asset = None
#             asset_id = asset_dict.pop('id', None)
#             if asset_id:
#                 asset = get_object_or_none(Asset, id=asset_id)
#             if not asset:
#                 try:
#                     if len(Asset.objects.filter(hostname=asset_dict.get('hostname'))):
#                         raise Exception(_('already exists'))
#                     with transaction.atomic():
#                         asset = Asset.objects.create(**asset_dict)
#                         if node:
#                             asset.nodes.set([node])
#                         created.append(asset_dict['hostname'])
#                         assets.append(asset)
#                 except Exception as e:
#                     failed.append('%s: %s' % (asset_dict['hostname'], str(e)))
#             else:
#                 for k, v in asset_dict.items():
#                     if v != '':
#                         setattr(asset, k, v)
#                 try:
#                     asset.save()
#                     updated.append(asset_dict['hostname'])
#                 except Exception as e:
#                     failed.append('%s: %s' % (asset_dict['hostname'], str(e)))
#
#         data = {
#             'created': created,
#             'created_info': 'Created {}'.format(len(created)),
#             'updated': updated,
#             'updated_info': 'Updated {}'.format(len(updated)),
#             'failed': failed,
#             'failed_info': 'Failed {}'.format(len(failed)),
#             'valid': True,
#             'msg': 'Created: {}. Updated: {}, Error: {}'.format(
#                 len(created), len(updated), len(failed))
#         }
#         return self.render_json_response(data)
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class AssetExportView(View):
#     """ 资产批量导出成csv文件 """
#     def get(self, request):
#         spm = request.GET.get('spm', '')
#         assets_id_default = [Asset.objects.first().id] if Asset.objects.first() else []
#         assets_id = cache.get(spm, assets_id_default)
#         fields = [
#             field for field in Asset._meta.fields
#             if field.name not in [
#                 'date_created'
#             ]
#         ]
#         filename = 'assets-{}.csv'.format(
#             timezone.localtime(timezone.now()).strftime('%Y-%m-%d_%H-%M-%S')
#         )
#         response = HttpResponse(content_type='text/csv')
#         response['Content-Disposition'] = 'attachment; filename="%s"' % filename
#         response.write(codecs.BOM_UTF8)
#         assets = Asset.objects.filter(id__in=assets_id)
#         writer = csv.writer(response, dialect='excel', quoting=csv.QUOTE_MINIMAL)
#
#         header = [field.verbose_name for field in fields]
#         writer.writerow(header)
#
#         for asset in assets:
#             data = [getattr(asset, field.name) for field in fields]
#             writer.writerow(data)
#         return response
#
#     def post(self, request, *args, **kwargs):
#         try:
#             assets_id = json.loads(request.body).get('assets_id', [])
#             assets_node_id = json.loads(request.body).get('node_id', None)
#         except ValueError:
#             return HttpResponse('Json object not valid', status=400)
#
#         if not assets_id and assets_node_id:
#             assets_node = get_object_or_none(Node, id=assets_node_id)
#             assets = assets_node.get_all_assets()
#             for asset in assets:
#                 assets_id.append(asset.id)
#
#         spm = uuid.uuid4().hex
#         cache.set(spm, assets_id, 300)
#         url = reverse_lazy('assets:asset-export') + '?spm=%s' % spm
#         return JsonResponse({'redirect': url})


class AssetExportView(TemplateView):
    pass


class BulkImportAssetView(TemplateView):
    pass
