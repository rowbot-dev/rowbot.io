
from django.db import models

from apps.base.models import Model, Manager

from .schema import RoleRunSchema

class RoleModel(Model):
  class Meta:
    permissions = ()

  club = models.ForeignKey('rowbot.Club', related_name='role_models', on_delete=models.CASCADE)
  is_superior_to = models.ManyToManyField('self', symmetrical=False, related_name='is_subordinate_to')

  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class RolePermission(Model):
  class Meta:
    permissions = ()

  roles = models.ManyToManyField('rowbot.RoleModel', related_name='permissions')

  model_name = models.CharField(max_length=255)
  name = models.CharField(max_length=255)


class RoleManager(Manager):
  def schema_instance_methods(self):
    return RoleRunSchema(self.model)

class Role(Model):
  class Meta:
    permissions = ()

  objects = RoleManager()

  team = models.ForeignKey('rowbot.Team', related_name='roles', null=True, on_delete=models.CASCADE)
  model = models.ForeignKey('rowbot.RoleModel', related_name='roles', on_delete=models.CASCADE)
  member = models.ForeignKey('rowbot.Member', related_name='roles', on_delete=models.CASCADE)
  is_superior_to = models.ManyToManyField('self', symmetrical=False, related_name='is_subordinate_to')

  nickname = models.CharField(max_length=255, default='')
  is_active = models.BooleanField(default=True)
  is_confirmed = models.BooleanField(default=False)

  def something(self, argument1=None, argument2=None):
    return {
      'hello': argument1 * 2,
      'goodbye': argument2 * 5,
    }

class RoleInstance(Model):
  class Meta:
    permissions = ()

  role = models.ForeignKey('rowbot.Role', related_name='instances', on_delete=models.CASCADE)
  event = models.ForeignKey('rowbot.EventInstance', related_name='roles', null=True, on_delete=models.CASCADE)

  is_active = models.BooleanField(default=True)
  is_confirmed = models.BooleanField(default=False)


class RoleRecord(Model):
  class Meta:
    permissions = ()

  role = models.ForeignKey('rowbot.Role', related_name='records', on_delete=models.CASCADE)
  event = models.ForeignKey('rowbot.EventInstance', related_name='records', null=True, on_delete=models.CASCADE)

  metadata = models.TextField()
