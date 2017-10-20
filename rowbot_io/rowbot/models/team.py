
# Django
from django.db import models

# DRF


# Local
from rowbot.models.base import Model

# Team
class TeamModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('rowbot.Club', related_name='team_models')
  is_superset_of = models.ManyToManyField('self', symmetrical=False, related_name='is_subset_of')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class Team(Model):
  class Meta:
    permissions = ()

  # Connections
  model = models.ForeignKey('rowbot.TeamModel', related_name='teams')
  is_superset_of = models.ManyToManyField('self', symmetrical=False, related_name='is_subset_of')

  # Properties
  name = models.CharField(max_length=255)


class TeamInstance(Model):
  class Meta:
    permissions = ()

	### Connections
  team = models.ForeignKey('rowbot.Team', related_name='instances')
  event = models.ForeignKey('rowbot.EventInstance', related_name='teams')


class TeamRecord(Model):
  class Meta:
    permissions = ()

  # Connections
  team = models.ForeignKey('rowbot.Team', related_name='team_records')
  event = models.ForeignKey('rowbot.EventInstance', related_name='team_records', null=True)

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
