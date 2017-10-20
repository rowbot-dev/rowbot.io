
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from rowbot.models import RoleModel, RolePermission, Role, RoleInstance, RoleRecord
from rowbot.serializers import RoleModelSerializer, RolePermissionSerializer, RoleSerializer, RoleInstanceSerializer, RoleRecordSerializer

# API
class RoleModelViewSet(viewsets.ViewSet):
  queryset = RoleModel.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RoleModelSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    role_model = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleModelSerializer(role_model)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleModelSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class RolePermissionViewSet(viewsets.ViewSet):
  queryset = RolePermission.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = RolePermissionSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    role_permission = get_object_or_404(self.queryset, pk=pk)
    serializer = RolePermissionSerializer(role_permission)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RolePermissionSerializer(data=request.data)
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
    role = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleSerializer(role)
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
    role_instance = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleInstanceSerializer(role_instance)
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
    role_record = get_object_or_404(self.queryset, pk=pk)
    serializer = RoleRecordSerializer(role_record)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = RoleRecordSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
