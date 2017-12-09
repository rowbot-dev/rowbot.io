
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.decorators import detail_route, list_route

# Local
from rowbot.api.base import BaseModelViewSet
from rowbot.models import AssetModel, Asset, AssetInstance
from rowbot.serializers import AssetModelSerializer, AssetSerializer, AssetInstanceSerializer

# API
class AssetModelViewSet(BaseModelViewSet):
  queryset = AssetModel.objects.all()
  serializer = AssetModelSerializer

  @list_route(methods=['GET'])
  def change_password(self, request):
    return Response({})

  @detail_route(methods=['GET'])
  def hmm(self, request, pk=None):
    return Response({})

class AssetViewSet(BaseModelViewSet):
  queryset = Asset.objects.all()
  serializer = AssetSerializer

class AssetInstanceViewSet(BaseModelViewSet):
  queryset = AssetInstance.objects.all()
  serializer = AssetInstanceSerializer
