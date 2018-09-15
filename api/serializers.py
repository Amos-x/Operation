# __author__ = "Amos"
# Email: 379833553@qq.com

from rest_framework import serializers
from apps.core import models


class AssetSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.Asset
        fields = ('id','asset_type','name','sn','contract','price','expire_date','bussiness_unit',
                  'tags','admin','idc','status','memo')


class ManufactorySerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Manufactory
        fields = ('id','manufactory','support_person','support_num','memo')


class BusinessUnitSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.BusinessUnit
        fields = ("id","parent_unit","name","memo")


class ContractSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.Contract
        fields = ("id","contract_num","name","contract_factory","price","detail","memo")


class IDCSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.IDC
        fields = ("id","name","address","memo")


class TagSerializerss(serializers.ModelSerializer):

    class Meta:
        model = models.Tag
        fields = ("id","name","creator")


class EventLogSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.EventLog
        fields = ('id',"name","event_type","asset","detail","handler","memo")


class NewAssetApprovalZoneSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.NewAssetApprovalZone
        fields = ("id","name","sn","asset_type","contract","bussiness_unit","tags","idc","data",
                  "approved","approved_by")


class UserProfileSerializers(serializers.ModelSerializer):

    class Meta:
        model = models.UserProfile
        fields = ("id","email","username","full_name","is_admin","is_active","department","phone","memo")
