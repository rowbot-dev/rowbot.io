
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from rowbot.models import Club
from rowbot.serializers import ClubSerializer

# API
class ClubViewSet(viewsets.ViewSet):
  queryset = Club.objects.all()
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  # GET
  def list(self, request):
    serializer = ClubSerializer(self.queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    club = get_object_or_404(self.queryset, pk=pk)
    serializer = ClubSerializer(club)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = ClubSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
