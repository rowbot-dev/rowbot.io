
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from row.models import AssetCategory, AssetType, Asset, AssetInstance
from row.serializers import AssetCategorySerializer, AssetTypeSerializer, AssetSerializer, AssetInstanceSerializer

# API
class AssetCategoryViewSet(viewsets.ViewSet):
  queryset = AssetCategory.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = AssetCategorySerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetCategorySerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = AssetCategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class AssetTypeViewSet(viewsets.ViewSet):
  queryset = AssetType.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = AssetTypeSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetTypeSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = AssetTypeSerializer(data=request.data)
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
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetSerializer(club)
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
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = AssetInstanceSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = AssetInstanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
