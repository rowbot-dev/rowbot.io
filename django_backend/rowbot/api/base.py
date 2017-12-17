
# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions
from rest_framework.decorators import detail_route, list_route

# Permissions
class CustomDjangoPermissions(DjangoObjectPermissions):
  perms_map = {
    'GET': [],
    'OPTIONS': [],
    'HEAD': [],
    'POST': [],
    'PUT': [],
    'PATCH': [],
    'DELETE': [],
  }

  def get_required_object_permissions(self, method, model_cls):
    kwargs = {
      'app_label': model_cls._meta.app_label,
      'model_name': model_cls._meta.model_name
    }

    if method not in self.perms_map:
      raise exceptions.MethodNotAllowed(method)

    return [perm % kwargs for perm in self.perms_map[method]]

  def has_object_permission(self, request, view, obj):
    # authentication checks have already executed via has_permission
    queryset = self._queryset(view)
    model_cls = queryset.model
    user = request.user

    perms = self.get_required_object_permissions(request.method, model_cls)

    if not user.has_perms(perms, obj):
      # If the user does not have permissions we need to determine if
      # they have read permissions to see 403, or not, and simply see
      # a 404 response.

      if request.method in SAFE_METHODS:
        # Read permissions already checked and failed, no need
        # to make another lookup.
        raise Http404

      read_perms = self.get_required_object_permissions('GET', model_cls)
      if not user.has_perms(read_perms, obj):
        raise Http404

      # Has read permissions.
      return False
    return True

# API
class BaseModelViewSet(viewsets.ViewSet):
  permission_classes = (IsAuthenticated, CustomDjangoPermissions)

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
