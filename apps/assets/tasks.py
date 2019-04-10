# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-08 10:37
#   FileName = tasks

from django.core.cache import cache
from celery import shared_task
from assets.constant import ADMIN_USER_CONN_CACHE_KEY, ASSET_ADMIN_CONN_CACHE_KEY
from common.utils import get_logger
import logging

logger = logging.getLogger(__name__)


logger = get_logger(__file__)
CACHE_MAX_TIME = 60*60*60


@shared_task
def set_admin_user_connectability_info(result, **kwargs):
    admin_user = kwargs.get("admin_user")
    task_name = kwargs.get("task_name")
    if admin_user is None and task_name is not None:
        admin_user = task_name.split(":")[-1]

    raw, summary = result
    cache_key = ADMIN_USER_CONN_CACHE_KEY.format(admin_user)
    cache.set(cache_key, summary, CACHE_MAX_TIME)

    for i in summary.get('contacted', []):
        asset_conn_cache_key = ASSET_ADMIN_CONN_CACHE_KEY.format(i)
        cache.set(asset_conn_cache_key, 1, CACHE_MAX_TIME)

    for i, msg in summary.get('dark', {}).items():
        asset_conn_cache_key = ASSET_ADMIN_CONN_CACHE_KEY.format(i)
        cache.set(asset_conn_cache_key, 0, CACHE_MAX_TIME)
        logger.error(msg)
