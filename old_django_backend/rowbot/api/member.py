
# http://polyglot.ninja/django-rest-framework-authentication-permissions/

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
from apps.rowbot.api.base import BaseModelViewSet
from apps.rowbot.models import Member
from apps.rowbot.serializers import MemberSerializer

# API
class MemberViewSet(BaseModelViewSet):
  queryset = Member.objects.all()
  permission_classes = (IsAuthenticated,)
  serializer = MemberSerializer

  @detail_route(methods=['POST'])
  def change_password(self, request, pk=None):
    changed = False
    if pk is not None and (request.user._id == pk or request.user.is_staff):
      password = request.data['password']
      user = get_object_or_404(self.get_queryset(), pk=pk)
      user.set_password(password)
      changed = True
      user.save()
    return Response({'changed': changed})

  @detail_route(methods=['POST'])
  def send_activation_email(self, request, pk=None):
    if pk is not None:
      user = get_object_or_404(self.get_queryset(), pk=pk)
      success = user.send_activation_email()
      return Response({'success': success})
    return Response({'success': False})
