
from django.db import models

from apps.base.models import Model, Manager

import uuid

class ReferenceGroupManager(Manager):
  def from_queryset(self, queryset):
    reference_group = self.create()
    for obj in queryset:
      reference_group.references.create(value=obj._ref)

    return reference_group._id

class ReferenceGroup(Model):
  objects = ReferenceGroupManager()

class Reference(Model):
  group = models.ForeignKey('reference.ReferenceGroup', related_name='references', on_delete=models.CASCADE)
  value = models.CharField(max_length=255)
