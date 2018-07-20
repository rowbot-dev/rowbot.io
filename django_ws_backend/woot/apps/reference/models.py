
from django.db import models

from apps.base.models import Model, Manager

import uuid

class ReferenceManager(Manager):
  def from_queryset(self, queryset):
    reference = self.create()
    for obj in queryset:
      reference.entries.create(value=obj._ref)

    return reference._id

  def from_multiple_querysets(self, querysets):
    reference = self.create()
    for queryset in querysets:
      for obj in queryset:
        reference.entries.create(value=obj._ref)

    return reference._id

class Reference(Model):
  objects = ReferenceManager()

class Entry(Model):
  reference = models.ForeignKey('reference.Reference', related_name='entries', on_delete=models.CASCADE)
  value = models.CharField(max_length=255)
