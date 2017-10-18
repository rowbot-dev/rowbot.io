
# Django
from django.db import models

# DRF


# Local
from row.models.base import Model

# Team
class TeamCategory(Model):
  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class TeamType(Model):
  # Connections
  category = models.ForeignKey('row.TeamCategory', related_name='types')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class Team(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('row.Club', related_name='teams')
  team = models.ForeignKey('row.Team', related_name='teams')
  type = models.ForeignKey('row.TeamType', related_name='instances')
  member = models.ForeignKey('row.Member', related_name='teams')

  # Properties
  nickname = models.CharField(max_length=255)


class TeamInstance(Model):
  class Meta:
    permissions = ()

	### Connections
  team = models.ForeignKey('row.Team', related_name='instances')
  event = models.ForeignKey('row.EventInstance', related_name='teams')


class TeamRecord(Model):
  class Meta:
    permissions = ()

  # Connections
  team = models.ForeignKey('row.Team', related_name='team_records')
  event = models.ForeignKey('row.EventInstance', related_name='team_records', null=True)

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
