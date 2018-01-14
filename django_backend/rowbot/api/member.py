
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
from rowbot.api.base import BaseModelViewSet
from rowbot.models import Member
from rowbot.serializers import MemberSerializer

# API
class MemberViewSet(BaseModelViewSet):
  queryset = Member.objects.all()
  permission_classes = (IsAuthenticated,)
  serializer = MemberSerializer

  def get_queryset(self):
    if self.request.user.is_staff:
      return Member.objects.all()
    else:
      return Member.objects.filter(id=self.request.user.id)

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

  @detail_route(methods=['GET'])
  def send_activation_email(self, request, pk=None):
    if pk is not None:
      user = get_object_or_404(self.get_queryset(), pk=pk)
      success = user.send_activation_email()
      return Response({'success': success})
    return Response({'success': False})
