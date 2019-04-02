# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-04-02 09:46
#   FileName = context_processor


def operation_processor(request):
    """ 自定义上下文处理器，设置全局默认变量， """
    return {
        'DEFAULT_PK': '00000000-0000-0000-0000-000000000000'
    }
