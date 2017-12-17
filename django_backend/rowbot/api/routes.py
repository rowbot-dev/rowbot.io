
# Django
from django.conf.urls import url
from django.conf import settings

# DRF
from rest_framework.authtoken import views
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

# Local
from rowbot.api.router import SchemaRouter
from rowbot.api.member import MemberViewSet
from rowbot.api.club import ClubViewSet
from rowbot.api.event import EventModelViewSet, EventViewSet, EventInstanceViewSet, EventNotificationViewSet
from rowbot.api.team import TeamModelViewSet, TeamViewSet, TeamInstanceViewSet, TeamRecordViewSet
from rowbot.api.role import RoleModelViewSet, RolePermissionViewSet, RoleViewSet, RoleInstanceViewSet, RoleRecordViewSet
from rowbot.api.asset import AssetModelViewSet, AssetViewSet, AssetInstanceViewSet

# Routes
router = SchemaRouter()

# member
router.register(r'members', MemberViewSet)

# club
router.register(r'clubs', ClubViewSet)

# event
router.register(r'events/models', EventModelViewSet)
router.register(r'events/root', EventViewSet)
router.register(r'events/instances', EventInstanceViewSet)
router.register(r'events/notifications', EventNotificationViewSet)

# team
router.register(r'teams/models', TeamModelViewSet)
router.register(r'teams/root', TeamViewSet)
router.register(r'teams/instances', TeamInstanceViewSet)
router.register(r'teams/records', TeamRecordViewSet)

# role
router.register(r'roles/models', RoleModelViewSet)
router.register(r'roles/permissions', RolePermissionViewSet)
router.register(r'roles/root', RoleViewSet)
router.register(r'roles/instances', RoleInstanceViewSet)
router.register(r'roles/records', RoleRecordViewSet)

# asset
router.register(r'assets/models', AssetModelViewSet)
router.register(r'assets/root', AssetViewSet)
router.register(r'assets/instances', AssetInstanceViewSet)

# patterns
urlpatterns = router.urls

# api token
class AuthTokenView(views.ObtainAuthToken):
  def post(self, request, *args, **kwargs):
    user = None
    if request.user.is_authenticated:
      user = request.user
    else:
      serializer = self.serializer_class(data=request.data, context={'request': request})
      if serializer.is_valid():
        user = serializer.validated_data['user']

    if user is not None:
      token, created = Token.objects.get_or_create(user=user)
      return Response({'token': token.key})
    else:
      return Response({})

urlpatterns += [
  url(r'^token/', AuthTokenView.as_view())
]

# web socket token
class SocketTokenView(views.APIView):
  def post(self, request, *args, **kwargs):
    user = None
    if request.user.is_authenticated:
      user = request.user
    else:
      serializer = self.serializer_class(data=request.data, context={'request': request})
      if serializer.is_valid():
        user = serializer.validated_data['user']

    if user is not None:
      socket = request.user.new_socket_token()
      return Response({'socket': socket._id, 'host': settings.WEBSOCKET['host'], 'port': settings.WEBSOCKET['socket']})
    else:
      return Response({})

urlpatterns += [
  url(r'^socket/', SocketTokenView.as_view())
]
