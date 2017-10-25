
# Django
from django.conf.urls import url

# DRF
from rest_framework.authtoken import views

# Local
from rowbot.api.router import SchemaRouter
from rowbot.api.member import MemberViewSet
from rowbot.api.club import ClubViewSet
from rowbot.api.event import EventModelViewSet, EventViewSet, EventInstanceViewSet
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
urlpatterns += [
  url(r'^token/', views.obtain_auth_token)
]
