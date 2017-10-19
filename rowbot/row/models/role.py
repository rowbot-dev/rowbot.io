
# Django
from django.db import models

# DRF


# Local
from row.models.base import Model

# Role
class RoleModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('row.Club', related_name='role_models')
  is_superior_to = models.ManyToManyField('self', symmetrical=False, related_name='is_subordinate_to')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class RolePermission(Model):
  class Meta:
    permissions = ()

  # Connections
  roles = models.ManyToManyField('row.RoleModel', related_name='permissions')

  # Properties
  model_name = models.CharField(max_length=255)
  name = models.CharField(max_length=255)


class Role(Model):
  class Meta:
    permissions = ()

  # Connections
  team = models.ForeignKey('row.Team', related_name='roles', null=True)
  model = models.ForeignKey('row.RoleModel', related_name='roles')
  member = models.ForeignKey('row.Member', related_name='roles')
  is_superior_to = models.ManyToManyField('self', symmetrical=False, related_name='is_subordinate_to')

  # Properties
  nickname = models.CharField(max_length=255)
  is_active = models.BooleanField(default=True)


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
