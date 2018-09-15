# __author__: Amos,Chinese
# Email：379833553@qq.com

from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('base/',views.base)
]