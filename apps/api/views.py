from django.shortcuts import render,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.core.mail import send_mail,BadHeaderError
from django.http import Http404
import  logging
from ..repository import models
import importlib
from ..salt.core import SaltApiClient
from ..salt.auto_report import AutoReportManager
from . import serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,viewsets,permissions
from .permissions import IsOwnerOrReadOnly

logger = logging.getLogger(__name__)


def autocollect(request):

    # TODO 传递更新的 hostname 列表 tgt参数

    token = SaltApiClient().token()
    obj = AutoReportManager(token,['test'])
    obj.exec_plugins()
    return HttpResponse('ok')

@login_required
def send_email(request):
    subject = request.POST.get('subject')
    message = request.POST.get('message')
    from_email = request.POST.get('from_email')
    to_email = request.POST.get('to_email')
    if subject and message and from_email and to_email:
        try:
            send_mail(subject,message,from_email,to_email)
        except BadHeaderError:
            return HttpResponse('头部错误')
        return HttpResponse('ok，发送成功')
    else:
        return HttpResponse('检查填写的字段，字段不完全')


class Assets(APIView):
    """
    Asset , 资产类api，列出所有
    """

    def get(self,request):
        queryset = models.Asset.objects.all()

        s = serializers.AssetSerializers(queryset,many=True)
        return Response(s.data)

    def post(self,request):
        s = serializers.AssetSerializers(data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data,status=status.HTTP_201_CREATED)
        return Response(s.errors,status=status.HTTP_400_BAD_REQUEST)


class Asset_detail(APIView):
    """
    Asset 单个的操作
    """

    def get_object(self, pk):
        try:
            return models.Asset.objects.get(pk=pk)
        except models.Asset.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        asset = self.get_object(pk)
        s = serializers.AssetSerializers(asset)
        return Response(s.data)

    def put(self, request, pk, format=None):
        asset = self.get_object(pk)
        s = serializers.AssetSerializers(asset, data=request.data)
        if s.is_valid():
            s.save()
            return Response(s.data)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        asset = self.get_object(pk)
        asset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AssetViewset(viewsets.ModelViewSet):
    queryset = models.Asset.objects.all()
    serializer_class = serializers.AssetSerializers


class ManufactoryViewset(viewsets.ModelViewSet):
    queryset = models.Manufactory.objects.all()
    serializer_class = serializers.ManufactorySerializers


class BusinessUnitViewset(viewsets.ModelViewSet):
    queryset = models.BusinessUnit.objects.all()
    serializer_class = serializers.BusinessUnitSerializers


class ContractViewset(viewsets.ModelViewSet):
    queryset = models.Contract.objects.all()
    serializer_class = serializers.ContractSerializers


class IDCViewset(viewsets.ModelViewSet):
    queryset = models.IDC.objects.all()
    serializer_class = serializers.IDCSerializers


class TagViewset(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializerss


class EventLogViewset(viewsets.ModelViewSet):
    queryset = models.EventLog.objects.all()
    serializer_class = serializers.EventLogSerializers


class NewAssetApprovalZoneViewset(viewsets.ModelViewSet):
    queryset = models.NewAssetApprovalZone.objects.all()
    serializer_class = serializers.NewAssetApprovalZoneSerializers


class UserProfileViewset(viewsets.ModelViewSet):
    queryset = models.UserProfile.objects.all()
    serializer_class = serializers.UserProfileSerializers
    permission_classes = (permissions.IsAdminUser,)