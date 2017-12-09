
# Django
from django.db import models

# DRF


# Local
from rowbot.models.base import Model

# Asset
class AssetModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('rowbot.Club', related_name='asset_models')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class Asset(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('rowbot.Club', related_name='assets')
  model = models.ForeignKey('rowbot.AssetModel', related_name='assets')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  name = models.CharField(max_length=255)
  description = models.TextField()


class AssetInstance(Model):
  class Meta:
    permissions = ()

  # Connections
  asset = models.ForeignKey('rowbot.Asset', related_name='instances')
  team = models.ForeignKey('rowbot.Team', related_name='assets')
  in_possession_of = models.ForeignKey('rowbot.Team', related_name='external_assets', null=True)

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
