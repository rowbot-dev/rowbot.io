
# http://polyglot.ninja/django-rest-framework-authentication-permissions/

# Django
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404

# DRF
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

# Local
from rowbot.api.base import BaseModelViewSet
from rowbot.models import Member
from rowbot.serializers import MemberSerializer

# API
class MemberViewSet(BaseModelViewSet):
  queryset = Member.objects.all()
  permission_classes = (IsAuthenticated,)
  serializer = MemberSerializer
  request_schema = {

  }

  def get_queryset(self):
    if self.request.user.is_staff:
      return Member.objects.all()
    else:
      return Member.objects.filter(id=self.request.user.id)
