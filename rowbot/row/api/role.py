
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from row.models import RoleCategory, RoleType, Role, RoleInstance, RoleRecord
from row.serializers import RoleCategorySerializer, RoleTypeSerializer, RoleSerializer, RoleInstanceSerializer, RoleRecordSerializer

# API
class RoleCategoryViewSet(viewsets.ViewSet):
  queryset = RoleCategory.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RoleCategorySerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleCategorySerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleCategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class RoleTypeViewSet(viewsets.ViewSet):
  queryset = RoleType.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RoleTypeSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleTypeSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleTypeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class RoleViewSet(viewsets.ViewSet):
  queryset = Role.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RoleSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class RoleInstanceViewSet(viewsets.ViewSet):
  queryset = RoleInstance.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RoleInstanceSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleInstanceSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleInstanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class RoleRecordViewSet(viewsets.ViewSet):
  queryset = RoleRecord.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RoleRecordSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleRecordSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleRecordSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
