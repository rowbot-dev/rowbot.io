
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
from row.models import Member
from row.serializers import MemberSerializer

# API
class MemberViewSet(viewsets.ViewSet):
  queryset = Member.objects.all()
  permission_classes = (IsAuthenticated,)

  def get_queryset(self):
    if self.request.user.is_staff:
      return Member.objects.all()
    else:
      return Member.objects.filter(id=self.request.user.id)

  # GET
  def list(self, request):
    queryset = self.get_queryset()
    serializer = MemberSerializer(queryset, many=True)
    return Response(serializer.data)

  # GET
  def retrieve(self, request, pk=None):
    queryset = self.get_queryset()
    member = get_object_or_404(queryset, pk=pk)
    serializer = MemberSerializer(member)
    return Response(serializer.data)

  # POST
  def create(self, request):
    serializer = MemberSerializer(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data)
    else:
      return Response(serializer.errors)
