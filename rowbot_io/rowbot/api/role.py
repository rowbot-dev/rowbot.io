
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from rowbot.api.base import BaseModelViewSet
from rowbot.models import RoleModel, RolePermission, Role, RoleInstance, RoleRecord
from rowbot.serializers import RoleModelSerializer, RolePermissionSerializer, RoleSerializer, RoleInstanceSerializer, RoleRecordSerializer

# API
class RoleModelViewSet(BaseModelViewSet):
  queryset = RoleModel.objects.all()
  serializer = RoleModelSerializer
  request_schema = {

  }

class RolePermissionViewSet(BaseModelViewSet):
  queryset = RolePermission.objects.all()
  serializer = RolePermissionSerializer
  request_schema = {

  }

class RoleViewSet(BaseModelViewSet):
  queryset = Role.objects.all()
  serializer = RoleSerializer
  request_schema = {

  }

class RoleInstanceViewSet(BaseModelViewSet):
  queryset = RoleInstance.objects.all()
  serializer = RoleInstanceSerializer
  request_schema = {

  }

class RoleRecordViewSet(BaseModelViewSet):
  queryset = RoleRecord.objects.all()
  serializer = RoleRecordSerializer
  request_schema = {

  }
