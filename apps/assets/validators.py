# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-02-28 16:44
#   FileName = validators

from django.core.validators import ValidationError
from assets.utils import validate_ssh_private_key


def private_key_validator(value):
    if not validate_ssh_private_key(value):
        raise ValidationError(_('{} is not an even number'.format(value)))
