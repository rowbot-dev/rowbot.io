
# Django
from django.conf.urls import url

# DRF
from rest_framework import routers
from rest_framework.authtoken import views

# Local
from row.api.member import MemberViewSet

# Routes
router = routers.SimpleRouter()
router.register(r'members', MemberViewSet)
urlpatterns = router.urls

# api token
urlpatterns += [
  url(r'^token/', views.obtain_auth_token)
]
