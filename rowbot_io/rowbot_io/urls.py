
# Django
from django.conf.urls import url, include
from django.contrib import admin

# URLs
urlpatterns = [
  # admin
  url(r'^admin/', admin.site.urls),

  # row
  url(r'^api/', include('rowbot.api.routes')),
  url(r'^', include('rowbot.api.app')),
]
