
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
from rowbot.models import TeamModel, Team, TeamInstance, TeamRecord
from rowbot.serializers import TeamModelSerializer, TeamSerializer, TeamInstanceSerializer, TeamRecordSerializer

# API
class TeamModelViewSet(BaseModelViewSet):
  queryset = TeamModel.objects.all()
  serializer = TeamModelSerializer

class TeamViewSet(BaseModelViewSet):
  queryset = Team.objects.all()
  serializer = TeamSerializer

class TeamInstanceViewSet(BaseModelViewSet):
  queryset = TeamInstance.objects.all()
  serializer = TeamInstanceSerializer

class TeamRecordViewSet(BaseModelViewSet):
  queryset = TeamRecord.objects.all()
  serializer = TeamRecordSerializer
