# __author__ = "Amos"
# Email: 379833553@qq.com

from django.urls import path,re_path
from django.conf.urls import include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

app_name = 'api'

router = DefaultRouter()
router.register('asset',views.AssetViewset)
router.register('manufactory',views.ManufactoryViewset)
router.register('businessUnit',views.BusinessUnitViewset)
router.register('contract',views.ContractViewset)
router.register('idc',views.IDCViewset)
router.register('tag',views.TagViewset)
router.register("newassetapprovalzone",views.NewAssetApprovalZoneViewset)
router.register("user",views.UserProfileViewset)
schema_view = get_schema_view(title='Pastebin API')

urlpatterns = [
    path('sendemail/',views.send_email),
    path('autocollect/',views.autocollect),
    path('',include(router.urls)),  # 视图集的路由
    path('schema/',schema_view),    # 概要
       # 文档
    # path('asset/',views.Assetlist.as_view(),name="asset-list"),
    # re_path('^asset/(?P<pk>[0-9]+)/$',views.Assetdetail.as_view(),name="asset-detail"),
]

# urlpatterns = format_suffix_patterns(urlpatterns)   # 接受格式后缀，如.json
