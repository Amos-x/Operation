# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-01 17:10
#   FileName = cluster


import uuid
import logging
from django.db import models
from django.utils.translation import ugettext_lazy as _


__all__ = ['Cluster']
logger = logging.getLogger(__name__)


class Cluster(models.Model):
    pass