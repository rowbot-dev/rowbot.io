
# Django
from django.conf.urls import url, include
from django.shortcuts import render
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Test
def test(request):
  if request.method == 'GET':
    return render(request, 'test.html')

# URLs
urlpatterns = [
  # admin
  url(r'^admin/', admin.site.urls),

  # row
  url(r'^api/', include('rowbot.api.routes')),
  url(r'^', include('rowbot.api.app')),

  # test
  url(r'^test/', test),
]
