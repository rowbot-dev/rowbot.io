
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from rowbot.models import EventModel, Event, EventInstance
from rowbot.serializers import EventModelSerializer, EventSerializer, EventInstanceSerializer

# API
class EventModelViewSet(viewsets.ViewSet):
  queryset = EventModel.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = EventModelSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    event_model = get_object_or_404(self.queryset, pk=pk)
    serializer = EventModelSerializer(event_model)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = EventModelSerializer(data=request.data)
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
    event = get_object_or_404(self.queryset, pk=pk)
    serializer = EventSerializer(event)
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
    event_instance = get_object_or_404(self.queryset, pk=pk)
    serializer = EventInstanceSerializer(event_instance)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = EventInstanceSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
