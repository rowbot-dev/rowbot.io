
# Django
from django.conf.urls import url, include
from django.contrib import admin

# URLs
urlpatterns = [
  # admin
  url(r'^admin/', admin.site.urls),

  # row
  url(r'^api/', include('row.api.routes')),
  url(r'^', include('row.api.app')),
]
