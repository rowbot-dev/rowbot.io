
# Django
from django.conf.urls import url

# DRF
from rest_framework import routers
from rest_framework.authtoken import views

# Local
from row.api.member import MemberViewSet
from row.api.club import ClubViewSet
from row.api.event import EventCategoryViewSet, EventTypeViewSet, EventViewSet, EventInstanceViewSet
from row.api.team import TeamCategoryViewSet, TeamTypeViewSet, TeamViewSet, TeamInstanceViewSet, TeamRecordViewSet
from row.api.role import RoleCategoryViewSet, RoleTypeViewSet, RoleViewSet, RoleInstanceViewSet, RoleRecordViewSet
from row.api.asset import AssetCategoryViewSet, AssetTypeViewSet, AssetViewSet, AssetInstanceViewSet

# Routes
router = routers.SimpleRouter()

# member
router.register(r'members', MemberViewSet)

# club
router.register(r'clubs', ClubViewSet)

# event
router.register(r'events/categories', EventCategoryViewSet)
router.register(r'events/types', EventTypeViewSet)
router.register(r'events/root', EventViewSet)
router.register(r'events/instances', EventInstanceViewSet)

# team
router.register(r'teams/categories', TeamCategoryViewSet)
router.register(r'teams/types', TeamTypeViewSet)
router.register(r'teams/root', TeamViewSet)
router.register(r'teams/instances', TeamInstanceViewSet)
router.register(r'teams/records', TeamRecordViewSet)

# role
router.register(r'roles/categories', RoleCategoryViewSet)
router.register(r'roles/types', RoleTypeViewSet)
router.register(r'roles/root', RoleViewSet)
router.register(r'roles/instances', RoleInstanceViewSet)
router.register(r'roles/records', RoleRecordViewSet)

# asset
router.register(r'assets/categories', AssetCategoryViewSet)
router.register(r'assets/types', AssetTypeViewSet)
router.register(r'assets/root', AssetViewSet)
router.register(r'assets/instances', AssetInstanceViewSet)

# patterns
urlpatterns = router.urls

# api token
urlpatterns += [
  url(r'^token/', views.obtain_auth_token)
]
