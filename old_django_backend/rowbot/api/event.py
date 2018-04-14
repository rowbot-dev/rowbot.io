
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
from rowbot.models import EventModel, EventNotificationModel, Event, EventInstance, EventNotification
from rowbot.serializers import EventModelSerializer, EventNotificationModelSerializer, EventSerializer, EventRepeatSerializer, EventInstanceSerializer, EventNotificationSerializer

# API
class EventModelViewSet(BaseModelViewSet):
  queryset = EventModel.objects.all()
  serializer = EventModelSerializer

class EventNotificationModelViewSet(BaseModelViewSet):
  queryset = EventNotificationModel.objects.all()
  serializer = EventNotificationModelSerializer

class EventViewSet(BaseModelViewSet):
  queryset = Event.objects.all()
  serializer = EventSerializer

  @detail_route(methods=['post'])
  def clear(self, request, pk=None):
    event = Event.objects.get(pk=pk)
    if event is not None:
      return Response(event.clear())
    return Response({})

  @detail_route(methods=['post'])
  def repeat(self, request, pk=None):
    event = Event.objects.get(pk=pk)
    if event is not None:
      event_repeat_serializer = EventRepeatSerializer(request.data)
      if event_repeat_serializer.is_valid():
        return Response(event.repeat(**event_repeat_serializer.validated_data))
      else:
        return Response(event_repeat_serializer.errors)
    return Response({})

class EventInstanceViewSet(BaseModelViewSet):
  queryset = EventInstance.objects.all()
  serializer = EventInstanceSerializer

  @detail_route(methods=['post'])
  def cancel(self, request, pk=None):
    event_instance = EventInstance.objects.get(pk=pk)
    if event_instance is not None:
      return Response(event_instance.cancel())
    return Response({})

class EventNotificationViewSet(BaseModelViewSet):
  queryset = EventNotification.objects.all()
  serializer = EventNotificationSerializer
