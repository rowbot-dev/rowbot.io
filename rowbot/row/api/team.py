
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from row.models import TeamCategory, TeamType, Team, TeamInstance, TeamRecord
from row.serializers import TeamCategorySerializer, TeamTypeSerializer, TeamSerializer, TeamInstanceSerializer, TeamRecordSerializer

# API
class TeamCategoryViewSet(viewsets.ViewSet):
  queryset = TeamCategory.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = TeamCategorySerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamCategorySerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamCategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class TeamTypeViewSet(viewsets.ViewSet):
  queryset = TeamType.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = TeamTypeSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamTypeSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamTypeSerializer(data=request.data)
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
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamSerializer(club)
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
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamInstanceSerializer(club)
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
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = TeamRecordSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = TeamRecordSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
