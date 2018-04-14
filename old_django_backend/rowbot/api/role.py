
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
from apps.rowbot.api.base import BaseModelViewSet
from apps.rowbot.models import RoleModel, RolePermission, Role, RoleInstance, RoleRecord
from apps.rowbot.serializers import RoleModelSerializer, RolePermissionSerializer, RoleSerializer, RoleInstanceSerializer, RoleRecordSerializer

# API
class RoleModelViewSet(BaseModelViewSet):
  queryset = RoleModel.objects.all()
  serializer = RoleModelSerializer

class RolePermissionViewSet(BaseModelViewSet):
  queryset = RolePermission.objects.all()
  serializer = RolePermissionSerializer

class RoleViewSet(BaseModelViewSet):
  queryset = Role.objects.all()
  serializer = RoleSerializer

class RoleInstanceViewSet(BaseModelViewSet):
  queryset = RoleInstance.objects.all()
  serializer = RoleInstanceSerializer

class RoleRecordViewSet(BaseModelViewSet):
  queryset = RoleRecord.objects.all()
  serializer = RoleRecordSerializer
