import json

import requests

from salt.settings import SALT_API_URL

"""
    定义的工具方法，用来简单化对salt-api的调用。
    在资产采集，或执行命令时，则可以直接调用这些工具方法，执行salt命令
"""

def exec_command(token, data ,piefix='/'):
    """
    基础的salt-api请求方法，其余salt工具方法都依赖此进行salt-api的调用
    :param token: salt认证token
    :param data: json格式的post数据
    :param piefix: 请求路径，默认为无
    :return: 返回salt执行后的结果
    """
    headers = {
        'X-Auth-Token': token,
        'Content-Type': 'application/json',
    }
    url = '%s%s' %(SALT_API_URL, piefix)
    response = requests.post(url, headers=headers, data=data, verify=False)
    result = response.json()
    return result


def update_all_keys(token):
    """
    列出所有的salt-minion。
    :param token: salt认证token
    :return: 返回salt执行后的结果
    """
    data = {'client':'wheel','fun':'key.list_all'}
    post_data = json.dumps(data)
    result = exec_command(token,post_data)
    return result

def manage_key(token,node_name,comm):
    """
    管理key，可以删除，通过，拒绝salt-minion的连接请求。
    :param token: salt认证token
    :param node_name: salt-minion的key名。
    :param comm: 需求命令
    :return: 返回salt执行后的结果
    """
    if comm == 'del':
        fun = 'key.del'
    elif comm == 'accept':
        fun = 'key.accept'
    elif comm == 'reject':
        fun = 'key.reject'
    else:
        fun = 'None'
    if fun:
        data={'client':'wheel','fun':fun,'match':node_name}
        post_data = json.dumps(data)
        result = exec_command(token,post_data)
        return result
    else:
        raise Exception


def shell_exec_command(token,tgt,arg):
    """
    通过这个工具，在minion上执行shell命令，得到返回结果
    :param token: salt认证token
    :param tgt: salt-minion的key名列表，用来匹配需执行命令的minion
    :param arg: 命令参数
    :return: 返回salt执行后的结果
    """
    data = {'client' : 'local','tgt' : tgt,'fun' : 'cmd.run','arg' : arg,'expr_form': 'list'}
    post_data = json.dumps(data)
    result = exec_command(token,post_data)
    return result

def get_info(token,tgt,comm):
    """
    获取salt收集的基础信息，包括grains或pillar
    :param token: salt认证token
    :param tgt: salt-minion的key名列表，用来匹配需执行命令的minion
    :param comm: 用于判断salt返回什么插件采集的基础信息
    :return: 返回salt执行后的结果
    """
    if comm == 'grains':
        fun = 'grains.items'
    elif comm == 'pillar':
        fun = 'pillar.items'
    else:
        fun = None
    if fun:
        data = {'client' : 'local','tgt' : tgt,'fun' : fun,'expr_form': 'list'}
        post_data = json.dumps(data)
        result = exec_command(token,post_data)
        return result
    else:
        raise Exception


def salt_exec_command(token,tgt,fun,arg):
    """
    通过这个命令执行salt命令，通过输入模块，参数，来执行
    :param token: salt认证token
    :param tgt: salt-minion的key名列表，用来匹配需执行命令的minion
    :param fun: salt的模块方法
    :param arg: 命令参数
    :return: 返回salt执行后的结果
    """
    data = {'client':'local','tgt':tgt,'fun':fun,'arg':arg,'expr_form': 'list'}
    post_data = json.dumps(data)
    result = exec_command(token,post_data)
    return result