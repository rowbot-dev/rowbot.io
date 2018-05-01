
from django.urls import path

from channels.routing import ProtocolTypeRouter, URLRouter
from apps.rowbot.consumer import Consumer

application = ProtocolTypeRouter({
  'websocket': URLRouter([
    path('api/', Consumer),
  ])
})
