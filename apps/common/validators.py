# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-27 18:52
#   FileName = validators


from django.core.validators import RegexValidator, ValidationError
from django.utils.translation import ugettext_lazy as _


__all__ = ['alphanumeric']


alphanumeric = RegexValidator(r'^[0-9a-zA-Z_@\-\.]*$', _('Special char not allowed'))
