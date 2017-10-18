
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from row.models import EventCategory, EventType, Event, EventInstance
from row.serializers import EventCategorySerializer, EventTypeSerializer, EventSerializer, EventInstanceSerializer

# API
class EventCategoryViewSet(viewsets.ViewSet):
  queryset = EventCategory.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = EventCategorySerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = EventCategorySerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = EventCategorySerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class EventTypeViewSet(viewsets.ViewSet):
  queryset = EventType.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = EventTypeSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = EventTypeSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = EventTypeSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class EventViewSet(viewsets.ViewSet):
  queryset = Event.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = EventSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = EventSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = EventSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

class EventInstanceViewSet(viewsets.ViewSet):
  queryset = EventInstance.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = EventInstanceSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = EventInstanceSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = EventInstanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
