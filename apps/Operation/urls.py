"""Operation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework.documentation import include_docs_urls
from Operation.views import IndexView
import re

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('core/',include('core.urls', namespace='core')),

    path('', IndexView.as_view(), name='index'),

    # module
    path('assets/', include('assets.urls', namespace='assets')),
    path('common/', include('common.urls', namespace='common')),
    path('users/', include('users.urls.views_urls', namespace='users')),
    path('perms/', include('perms.urls', namespace='perms')),
    path('terminal/', include('terminal.urls', namespace='terminal')),

    # captcha
    path('captcha/', include('captcha.urls')),

    # api module
    path('api/users/', include('users.urls.api_urls', namespace='api-users'))
]

# static and media
urlpatterns += [
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.STATIC_URL.lstrip('/')),
            serve, {'document_root': settings.STATIC_ROOT}),
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')),
            serve, {'document_root': settings.MEDIA_ROOT})
]
