
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from row.models import AssetModel, Asset, AssetInstance
from row.serializers import AssetModelSerializer, AssetSerializer, AssetInstanceSerializer

# API
class AssetModelViewSet(viewsets.ViewSet):
  queryset = AssetModel.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = AssetModelSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    asset_model = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetModelSerializer(asset_model)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = AssetModelSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class AssetViewSet(viewsets.ViewSet):
  queryset = Asset.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = AssetSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    asset = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetSerializer(asset)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = AssetSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class AssetInstanceViewSet(viewsets.ViewSet):
  queryset = AssetInstance.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = AssetInstanceSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    asset_instance = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetInstanceSerializer(asset_instance)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = AssetInstanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
