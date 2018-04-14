
from django.db import models
from apps.base.models import Model

class Server(Model):

  server_type = models.CharField(max_length=255)
  public_key = models.TextField()


class ServerToken(Model):

  server = models.ForeignKey(Server, related_name='tokens', on_delete=models.CASCADE)

  payload = models.TextField()
  signature = models.TextField()
