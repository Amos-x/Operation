"""
Django settings for Operation project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys
from django.urls import reverse_lazy

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)

sys.path.append(PROJECT_DIR)

# import config
try:
    from config import config as CONFIG
except ImportError:
    msg = """

    Error: No config file found.

    Please check the integrity of the project.
    """
    raise ImportError(msg)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '0gyi_s^pafm*^#vlkc9n__h+=%-#7=#h*m=ll!d0#u99l3fo5w'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.DEBUG or False
LOG_LEVEL = CONFIG.LOG_LEVEL or 'INFO'
LOG_DIR = CONFIG.LOG_DIR or os.path.join(PROJECT_DIR, 'logs')

ALLOWED_HOSTS = CONFIG.ALLOWED_HOSTS or ['*']

if DEBUG:
    SITE_URL = 'http://localhost:8000'
else:
    SITE_URL = CONFIG.SITE_URL or 'http://localhost'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',
    'django_celery_beat',
    'rest_framework',
    'bootstrap3',
    'captcha',
    'django_filters',
    'assets',
    'common',
    'users',
    'perms'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Operation.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'Operation.context_processor.operation_processor',
                'django.template.context_processors.i18n',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'Operation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.{}'.format(CONFIG.DB_ENGINE),
        'NAME': CONFIG.DB_NAME,
        'HOST': CONFIG.DB_HOST,
        'PORT': CONFIG.DB_PORT,
        'USER': CONFIG.DB_USER,
        'PASSWORD': CONFIG.DB_PASSWORD,
        'ATOMIC_REQUESTS': True,
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(PROJECT_DIR,'data','static')
# STATIC_DIR = os.path.join(BASE_DIR, "static")
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# 上传文件目录设置
MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'data', 'media')


##
# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "asgi_redis.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("localhost", 6379)],
#         },
#         "ROUTING": "Operation.routing.channel_routing",
#     },
# }

# Celery任务消息队列配置
CELERY_BROKER_URL = CONFIG.CELERY_BROKER_URL
CELERY_ACCEPT_CONTENT = ['json','pickle']
CELERY_TASK_SERIALIZER = 'pickle'    # task序列化方式
CELERY_RESULT_BACKEND = CELERY_BROKER_URL    # 使用django ORM作为celery储存后端
CELERY_RESULT_EXPIRES = 3600
CELERY_RESULT_SERIALIZER = 'pickle'    # 结果序列化方式

# Session配置，使用缓存存放session
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"

# 缓存配置
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": CONFIG.REDIS_CACHE_LOCATION,   ## redis单实例连接
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # 这里只能使用默认的序列化方式，不然报错，无法对类对象直接进行序列化缓存
            # "SERIALIZER": "django_redis.serializers.msgpack.MSGPackSerializer",  ## 指定序列化方式：msgpack（比json更快更小）
            # "SERIALIZER": "django_redis.serializers.json.JSONSerializer",  ## 指定序列化方式：json
            "IGNORE_EXCEPTIONS": True,      ## redis连接异常关闭时不触发异常
            "CONNECTION_POOL_KWARGS": {"max_connections": CONFIG.REDIS_MAX_CONNECTIONS},  ## 连接池最大连接池
        },
        'TIMEOUT': None,
        'KEY_PREFIX': 'Operation_system',
    }
}
DJANGO_REDIS_LOGGER = 'django'  # 指定缓存log记录器

# 登陆页面的设定
LOGIN_URL = reverse_lazy('users:login')
LOGIN_REDIRECT_URL = reverse_lazy('index')

# 拓展用户模型
AUTH_USER_MODEL = 'users.User'

# 用户默认过期时间
DEFAULT_EXPIRED_YEARS = CONFIG.DEFAULT_EXPIRED_YEARS or 70
# 默认登录和密码限制
DEFAULT_PASSWORD_MIN_LENGTH = 6
DEFAULT_LOGIN_LIMIT_COUNT = 6
DEFAULT_LOGIN_LIMIT_TIME = 30


# Email的SMTP配置
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = CONFIG.EMAIL_HOST
EMAIL_PORT = CONFIG.EMAIL_PORT
EMAIL_HOST_USER = CONFIG.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = CONFIG.EMAIL_HOST_PASSWORD
EMAIL_USE_SSL = CONFIG.EMAIL_USE_SSL
EMAIL_SUBJECT_PREFIX = CONFIG.EMAIL_SUBJECT_PREFIX or ''    # 邮件主题前缀
DEFAULT_FROM_EMAIL = CONFIG.EMAIL_HOST_USER    # 默认系统邮箱
SERVER_EMAIL = CONFIG.EMAIL_HOST_USER  # 错误消息邮件发送者，即管理员邮箱

# REST-API的所有全局设置
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [      # 权限方式类
        'rest_framework.permissions.IsAuthenticated'
    ],
    # 设置默认过滤器， 实现基本的搜索，排序等过滤
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'SEARCH_PARAM': 'search',
    'ORDERING_PARAM': 'order',
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'PAGE_SIZE': 10
}

# django自身分页设置，默认分页数
DISPLAY_PER_PAGE = CONFIG.DISPLAY_PER_PAGE or 25


# Django bootstrap3 setting, more see http://django-bootstrap3.readthedocs.io/en/latest/settings.html
BOOTSTRAP3 = {
    'horizontal_label_class': 'col-md-2',
    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',
    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,
    'success_css_class': '',
}


# logging日志配置，定义发送邮件给管理员，default，error，console四个处理器。
# 一个全局的logger，将日志发给几个处理器，根据日志级别进行不同处理
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
       'standard': {
            'format': '%(asctime)s [%(threadName)s:%(thread)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s'}  #日志格式
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR,'Operation.log'),   ## 日志输出文件
            'maxBytes': 1024*1024*10,   # 文件大小,10M
            'backupCount': 5,   # 备份份数
            'formatter':'standard',    # 使用哪种formatters日志格式
        },
        'error': {
            'level':'ERROR',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR,'error.log'),
            'maxBytes':1024*1024*10,    # 文件大小,10M
            'backupCount': 5,
            'formatter':'standard',
        },
        'tasks':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'tasks.log'),
            'maxBytes': 1024*1024*10,
            'backupCount': 10,
            'formatter':'standard',
        },
        'console':{
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['default', 'console','error'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'operation': {
            'handlers': ['default', 'console','error'],
            'level': LOG_LEVEL,
            'propagate': True
        },
        'scheduler_task': {
            'handlers': ['tasks','error'],
            'level': LOG_LEVEL,
            'propagate': True
        }
    }
}