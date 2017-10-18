
# Django
from django.db import models

# DRF


# Local
from row.models.base import Model

# Role
class RoleCategory(Model):
  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class RoleType(Model):
  # Connections
  category = models.ForeignKey('row.RoleCategory', related_name='types')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class Role(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('row.Club', related_name='roles')
  team = models.ForeignKey('row.Team', related_name='roles')
  type = models.ForeignKey('row.RoleType', related_name='instances')
  member = models.ForeignKey('row.Member', related_name='roles')

  # Properties
  nickname = models.CharField(max_length=255)


class RoleInstance(Model):
  class Meta:
    permissions = ()

	### Connections
  role = models.ForeignKey('row.Role', related_name='instances')
  event = models.ForeignKey('row.EventInstance', related_name='roles')


class RoleRecord(Model):
  class Meta:
    permissions = ()

  # Connections
  role = models.ForeignKey('row.Role', related_name='records')
  event = models.ForeignKey('row.EventInstance', related_name='records', null=True)

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
