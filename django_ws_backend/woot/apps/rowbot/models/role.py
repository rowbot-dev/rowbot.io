
# Django
from django.db import models

# DRF


# Local
from apps.rowbot.models.base import Model

# Role
class RoleModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('rowbot.Club', related_name='role_models', on_delete=models.CASCADE)
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
  roles = models.ManyToManyField('rowbot.RoleModel', related_name='permissions')

  # Properties
  model_name = models.CharField(max_length=255) # TODO: find out what this was for
  name = models.CharField(max_length=255)


class Role(Model):
  class Meta:
    permissions = ()

  # Connections
  team = models.ForeignKey('rowbot.Team', related_name='roles', null=True, on_delete=models.CASCADE)
  model = models.ForeignKey('rowbot.RoleModel', related_name='roles', on_delete=models.CASCADE)
  member = models.ForeignKey('rowbot.Member', related_name='roles', on_delete=models.CASCADE)
  is_superior_to = models.ManyToManyField('self', symmetrical=False, related_name='is_subordinate_to')

  # Properties
  nickname = models.CharField(max_length=255, default='')
  is_active = models.BooleanField(default=True)
  is_confirmed = models.BooleanField(default=False)


class RoleInstance(Model):
  class Meta:
    permissions = ()

	# Connections
  role = models.ForeignKey('rowbot.Role', related_name='instances', on_delete=models.CASCADE)
  event = models.ForeignKey('rowbot.EventInstance', related_name='roles', null=True, on_delete=models.CASCADE)

  # Properties
  is_active = models.BooleanField(default=True)
  is_confirmed = models.BooleanField(default=False)


class RoleRecord(Model):
  class Meta:
    permissions = ()

  # Connections
  role = models.ForeignKey('rowbot.Role', related_name='records', on_delete=models.CASCADE)
  event = models.ForeignKey('rowbot.EventInstance', related_name='records', null=True, on_delete=models.CASCADE)

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
