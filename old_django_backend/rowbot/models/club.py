
# Django
from django.db import models

# DRF

# Local
from apps.rowbot.models.base import Model

# Club
class Club(Model):

  # Properties
  name = models.CharField(max_length=255)
  
  # crest file
