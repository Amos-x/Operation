from __future__ import absolute_import,unicode_literals
from celery import shared_task

import time


@shared_task
def test_celery():
    a = []
    for x in range(10):
        a.append(x)
        time.sleep(2)
    return a

@shared_task
def update_keys():
    pass