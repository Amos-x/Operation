# -*- coding:utf-8 -*-
# __author__ = Amos
#      Email = 379833553@qq.com
#  Create_at = 2019-03-18 15:36
#   FileName = utils

import requests
import ipaddress
from django.utils import timezone
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from common.utils import reverse_lazy
from django.core.cache import cache
from django.http import Http404
from common.tasks import send_email_async
from common.models import Setting
from common.utils import get_logger
from users.models import LoginLog


logger = get_logger(__name__)


def date_expired_default():
    try:
        years = int(settings.DEFAULT_EXPIRED_YEARS)
    except:
        years = 70
    return timezone.now() + timezone.timedelta(days=365*years)


def send_user_created_mail(user):
    """ 发送用户创建成功邮件，并通过邮件设置密码 """
    subject = "Create account successfully"
    recipient_list = [user.email]
    message = _("""
    Hello {name}:
    </br>
    Your account has been created successfully
    </br>
    Username: {username}
    </br>
    <a href="{rest_password_url}?token={rest_password_token}">click here to set your password</a>
    </br>
    This link is valid for 1 hour. After it expires, <a href="{forget_password_url}?email={email}">request new one</a>

    </br>
    ---

    </br>
    <a href="{login_url}">Login direct</a>

    </br>
    """.format(
        name=user.name,
        username=user.username,
        rest_password_url=reverse_lazy('users:reset-password', external=True),
        rest_password_token=user.generate_reset_token(),
        forget_password_url=reverse_lazy('users:forgot-password', external=True),
        email=user.email,
        login_url=reverse_lazy('users:login', external=True)
    ))
    if settings.DEBUG:
        try:
            logger.debug(message)
        except OSError:
            pass
    send_email_async.delay(subject, message, recipient_list, html_message=message)


def send_reset_password_mail(user):
    """ 发送用户重置密码邮件 """
    subject = "Reset password"
    recipient_list = [user.email]
    message = _("""
        Hello {name}:
        </br>
        Please click the link below to reset your password, if not your request, concern your account security
        </br>
        <a href="{rest_password_url}?token={rest_password_token}">Click here reset password</a>
        </br>
        This link is valid for 1 hour. After it expires, <a href="{forget_password_url}?email={email}">request new one</a>

        </br>
        ---

        </br>
        <a href="{login_url}">Login direct</a>

        </br>
    """.format(
        name=user.name,
        rest_password_url=reverse_lazy('users:reset-password', external=True),
        rest_password_token=user.generate_reset_token(),
        forget_password_url=reverse_lazy('users:forgot-password', external=True),
        email=user.email,
        login_url=reverse_lazy('users:login', external=True)
    ))
    if settings.DEBUG:
        logger.debug(message)
    send_email_async.delay(subject, message, recipient_list, html_message=message)


def send_reset_ssh_key_mail(user):
    """ 发送用户重置密码邮件 """
    subject = "Reset ssh key"
    recipient_list = [user.email]
    message = _("""
    Hello {name}:
    </br>
    Your ssh public key has been reset by site administrator.
    Please login and reset your ssh public key.
    </br>
    <a href="{login_url}">Login direct</a>

    </br>
    """.format(
        name=user.name,
        login_url=reverse_lazy('users:login', external=True)
    ))
    if settings.DEBUG:
        logger.debug(message)
    send_email_async.delay(subject, message, recipient_list, html_message=message)


def redirect_user_first_login_or_index(request, redirect_field_name):
    # if request.user.is_first_login:
    #     return reverse_lazy('users:user-first-login')
    return request.POST.get(
        redirect_field_name, request.GET.get(redirect_field_name, reverse_lazy('index'))
    )


def get_login_ip(request):
    """ 获取登录地址ip """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')
    if x_forwarded_for and x_forwarded_for[0]:
        login_ip = x_forwarded_for[0]
    else:
        login_ip = request.META.get('REMOTE_ADDR', '')
    return login_ip


def is_block_login(key_limit):
    """ 是否限制登录,获取限制登录次数，并判断 """
    count = cache.get(key_limit)

    setting_limit_count = Setting.objects.filter(
        name='SECURITY_LOGIN_LIMIT_COUNT'
    ).first()
    limit_count = setting_limit_count.cleaned_value if setting_limit_count \
        else settings.DEFAULT_LOGIN_LIMIT_COUNT

    if count and count >= limit_count:
        return True


def set_user_login_failed_count_to_cache(key_limit, key_block):
    """ 设置用户登录失败次数到缓存,并判断是否进行限制登录 """
    count = cache.get(key_limit)
    count = count + 1 if count else 1
    # 限制登录次数
    setting_limit_count = Setting.objects.filter(name='SECURITY_LOGIN_LIMIT_COUNT').first()
    limit_count = setting_limit_count.cleaned_value if setting_limit_count else settings.DEFAULT_LOGIN_LIMIT_COUNT
    # 限制登录时间
    setting_limit_time = Setting.objects.filter(name='SECURITY_LOGIN_LIMIT_TIME').first()
    limit_time = setting_limit_time.cleaned_value if setting_limit_time else settings.DEFAULT_LOGIN_LIMIT_TIME

    if count >= limit_count:
        cache.set(key_block, 1, int(limit_time) * 60)
    cache.set(key_limit, count, int(limit_time) * 60)


def set_tmp_user_to_cache(request, user):
    """ 设置临时用户缓存，有效期10分钟, """
    cache.set(request.session.session_key+'user', user, 600)


def get_tmp_user_from_cache(request):
    """ 从缓存中获取临时用户，没有则返回None """
    if not request.session.session_key:
        return None
    user = cache.get(request.session.session_key+'user')
    return user


def get_user_or_tmp_user(request):
    """ 获取用户或临时用户,找不到则报错404 """
    user = request.user
    tmp_user = get_tmp_user_from_cache(request)
    if user.is_authenticated:
        return user
    elif tmp_user:
        return tmp_user
    else:
        raise Http404("Not found this user")


def validate_ip(ip):
    """ 判断ip地址是否合规 """
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        pass
    return False


def write_login_log(*args, **kwargs):
    """ 写入登录历史,根据ip，得到ip所在地 """
    ip = kwargs.get('ip', '')
    # if not (ip and validate_ip(ip)):
    if not ip or not validate_ip(ip):
        city = "Unknown"
    else:
        city = get_ip_city(ip)
    kwargs.update({'ip': ip, 'city': city})
    LoginLog.objects.create(**kwargs)


def get_ip_city(ip, timeout=10):
    """ 通过ip，返回ip所在城市 """
    # Taobao ip api: http://ip.taobao.com/service/getIpInfo.php?ip=8.8.8.8
    # Sina ip api: http://int.dpool.sina.com.cn/iplookup/iplookup.php?ip=8.8.8.8&format=json

    url = 'http://ip.taobao.com/service/getIpInfo.php?ip={}'.format(ip)
    try:
        response = requests.get(url, timeout=timeout)
    except:
        response = None
    city = 'Unknown'
    if response and response.status_code == 200:
        try:
            data = response.json()
            if not isinstance(data, int) and data['code'] == 0:
                city = data['data']['county'] + ' ' + data['data']['city']
        except ValueError:
            pass
    return city


def is_need_unblock(block_key):
    """ 检查环境key，看看用户是否被锁，被锁则返回True，反之则否 """
    if not cache.get(block_key):
        return False
    return True
