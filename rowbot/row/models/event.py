
# Django
from django.db import models

# DRF


# Local
from row.models.base import Model

# Event
class EventCategory(Model):
  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)


class EventType(Model):
  # Connections
  category = models.ForeignKey('row.EventCategory', related_name='types')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)


class Event(Model):
  class Meta:
    permissions = ()

  # Connections
  type = models.ForeignKey('row.EventType', related_name='events')
  club = models.ForeignKey('row.Club', related_name='events')

  # Properties
  name = models.CharField(max_length=255)
  description = models.TextField()


class EventInstance(Model):
  class Meta:
    permissions = ()

  # Connections
  event = models.ForeignKey('row.Event', related_name='instances')

  # Properties
  description = models.TextField()
