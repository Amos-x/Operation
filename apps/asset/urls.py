from django.urls import path,re_path
from . import views

app_name = 'asset'
#
urlpatterns = [
    path('',views.home),
    path('error/',views.raise_exception,name='raise_exception'),
    path('index/',views.index,name='index'),
    path('login/',views.login),
    path('changepassword/',views.changepassword,name='changepassword'),
    path('logout/',views.logout,name='logout'),

#     re_path(r'^host/(.+?)/$',views.host_all,name='host_all'),
#     re_path('^vps/(.+?)/$',views.vps_all,name='vps_all'),
#     re_path(r'^user/(.+?)/$',views.user_all,name='user_all'),
#     re_path(r'^usergroup/(.+?)/$',views.usergroup_all,name='usergroup_all'),
#
#     path('equipment/',views.equipment,name='equipment'),
#     path('hostgroup/',views.hostgroup,name='hostgroup'),
#     path('hostremoteuser/',views.hostremoteuser,name='hostremoteuser')
]