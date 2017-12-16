
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.decorators import detail_route, list_route

# API
class BaseModelViewSet(viewsets.ViewSet):
  permission_classes = (IsAuthenticated, DjangoObjectPermissions)

  def get_queryset(self):
    return self.queryset

  # GET
  def list(self, request):
    serializer = self.serializer(self.get_queryset().filter(**self.request.query_params.dict()), many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    model = get_object_or_404(self.get_queryset(), pk=pk)
    serializer = self.serializer(model)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = self.serializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

  # PATCH
  def partial_update(self, request, pk=None):
    serializer = self.serializer(data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)

  # DELETE
  def destroy(self, request, pk=None):
    model = get_object_or_404(self.get_queryset(), pk=pk)
    model.delete()
    return Response({'deleted': True})
