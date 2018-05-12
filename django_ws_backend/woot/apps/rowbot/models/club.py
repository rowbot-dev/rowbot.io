
# Django
from django.db import models

# DRF

# Local
from apps.base.models import Model

# Club
class Club(Model):

  # Properties
  name = models.CharField(max_length=255)

  # crest file
