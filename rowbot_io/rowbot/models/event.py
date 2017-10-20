
# Django
from django.db import models

# DRF


# Local
from rowbot.models.base import Model

# Event
class EventModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('rowbot.Club', related_name='event_models')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)


class Event(Model):
  class Meta:
    permissions = ()

  # Connections
  model = models.ForeignKey('rowbot.EventModel', related_name='events')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  name = models.CharField(max_length=255)
  description = models.TextField()


class EventInstance(Model):
  class Meta:
    permissions = ()

  # Connections
  event = models.ForeignKey('rowbot.Event', related_name='instances')

  # Properties
  start_time = models.DateTimeField(auto_now_add=False, null=True)
  end_time = models.DateTimeField(auto_now_add=False, null=True)
  location = models.CharField(max_length=255)
  description = models.TextField()
