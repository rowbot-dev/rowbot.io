
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
from rowbot.models import EventModel, Event, EventInstance
from rowbot.serializers import EventModelSerializer, EventSerializer, EventInstanceSerializer

# API
class EventModelViewSet(BaseModelViewSet):
  queryset = EventModel.objects.all()
  serializer = EventModelSerializer

class EventViewSet(BaseModelViewSet):
  queryset = Event.objects.all()
  serializer = EventSerializer

  @list_route(methods=['get'])
  def pending(self, request):
    return Response({})

class EventInstanceViewSet(BaseModelViewSet):
  queryset = EventInstance.objects.all()
  serializer = EventInstanceSerializer
