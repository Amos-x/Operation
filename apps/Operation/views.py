# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-07 21:00
#   FileName = views

from django.shortcuts import redirect
from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            return redirect('assets:user-asset-list')
        return super().get(request, *args, **kwargs)
