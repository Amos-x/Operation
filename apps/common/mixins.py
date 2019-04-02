# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-01 19:19
#   FileName = mixins

from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from django.http import JsonResponse
from rest_framework_bulk import BulkListSerializer


__all__ = ['AdminUserRequiredMixin', 'DatetimeSearchMixin', 'JSONResponseMixin', 'IDInFilterMixin',
           'BulkSerializerMixin']


class AdminUserRequiredMixin(UserPassesTestMixin):
    """ 管理员用户权限验证 """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True


class DatetimeSearchMixin(object):
    """ 定义时间查询的转换函数 """
    date_format = '%Y-%m-%d'
    date_from = date_to = None

    def get_date_range(self):
        date_from_s = self.request.GET.get('date_from')
        date_to_s = self.request.GET.get('date_to')

        # 没有起始日期则默认查询7天内
        if date_from_s:
            date_from = timezone.datetime.strptime(date_from_s, self.date_format)
            tz = timezone.get_current_timezone()
            self.date_from = tz.localize(date_from)
        else:
            self.date_from = timezone.now() - timezone.timedelta(7)

        if date_to_s:
            date_to = timezone.datetime.strptime(
                date_to_s + ' 23:59:59', self.date_format + ' %H:%M:%S'
            )
            self.date_to = date_to.replace(
                tzinfo=timezone.get_current_timezone()
            )
        else:
            self.date_to = timezone.now()

    def get(self, request, *args, **kwargs):
        # 在请求中解析日志，生产self.data_form and self.data_to
        self.get_date_range()
        return super().get(request, *args, **kwargs)


class JSONResponseMixin(object):
    """JSON mixin"""
    @staticmethod
    def render_json_response(context):
        return JsonResponse(context)


class IDInFilterMixin(object):
    """
    重写后端过滤方法，用于queryset过滤，作为minix组件，用于批量操作Api
    rest framework 中 query_params 来代替request.GET，详见rest framework 源码
    必须同时继承于rest framework 的通用视图类，或视图集，以保证filter_queryset方法的重写和request.query_params的属性存在
    """
    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        id_list = self.request.query_params.get('id__in')
        if id_list:
            import json
            try:
                ids = json.loads(id_list)
            except Exception as e:
                return queryset
            if isinstance(ids, list):
                queryset = queryset.filter(id__in=ids)
        return queryset


class BulkSerializerMixin(object):
    """
    Become rest_framework_bulk not support uuid as a primary key
    so rewrite it. https://github.com/miki725/django-rest-framework-bulk/issues/66
    """
    def to_internal_value(self, data):
        ret = super(BulkSerializerMixin, self).to_internal_value(data)

        id_attr = getattr(self.Meta, 'update_lookup_field', 'id')
        request_method = getattr(getattr(self.context.get('view'), 'request'), 'method', '')

        # add update_lookup_field field back to validated data
        # since super by default strips out read-only fields
        # hence id will no longer be present in validated_data
        if all((isinstance(self.root, BulkListSerializer),
                id_attr,
                request_method in ('PUT', 'PATCH'))):
            id_field = self.fields[id_attr]
            if data.get("id"):
                id_value = id_field.to_internal_value(data.get("id"))
            else:
                id_value = id_field.to_internal_value(data.get("pk"))
            ret[id_attr] = id_value

        return ret
