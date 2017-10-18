
# Django
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.conf.urls import url, include

# App
def auth(request):
  if request.method == 'GET':
    # logout any user to begin with
    logout(request)

    # return SPA
    return render(request, 'row/auth.html')

def app(request):
  if request.method == 'GET' and request.user.is_authenticated:
    return render(request, 'row/account.html')
  else:
    return redirect('/auth/')

urlpatterns = [
  url(r'^auth/$', auth),
  url(r'^$', app),
]
