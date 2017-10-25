
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
from rowbot.models import Club
from rowbot.serializers import ClubSerializer

# API
class ClubViewSet(BaseModelViewSet):
  queryset = Club.objects.all()
  serializer = ClubSerializer
