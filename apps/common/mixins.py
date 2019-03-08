# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-01 19:19
#   FileName = mixins

from django.contrib.auth.mixins import UserPassesTestMixin


__all__ = ['AdminUserRequiredMixin']


class AdminUserRequiredMixin(UserPassesTestMixin):
    """ 管理员用户权限验证 """
    def test_func(self):
        if not self.request.user.is_authenticated:
            return False
        elif not self.request.user.is_superuser:
            self.raise_exception = True
            return False
        return True
