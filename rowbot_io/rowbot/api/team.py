
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from rowbot.models import TeamModel, Team, TeamInstance, TeamRecord
from rowbot.serializers import TeamModelSerializer, TeamSerializer, TeamInstanceSerializer, TeamRecordSerializer

# API
class TeamModelViewSet(viewsets.ViewSet):
  queryset = TeamModel.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = TeamModelSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    team_model = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamModelSerializer(team_model)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamModelSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class TeamViewSet(viewsets.ViewSet):
  queryset = Team.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = TeamSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    team = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamSerializer(team)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class TeamInstanceViewSet(viewsets.ViewSet):
  queryset = TeamInstance.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = TeamInstanceSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    team_instance = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamInstanceSerializer(team_instance)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamInstanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class TeamRecordViewSet(viewsets.ViewSet):
  queryset = TeamRecord.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = TeamRecordSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    team_record = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamRecordSerializer(team_record)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamRecordSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
