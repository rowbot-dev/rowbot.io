
# Django
from django.db import models

# DRF


# Local
from row.models.base import Model

# Asset
class AssetModel(Model):
  class Meta:
    permissions = ()

  # Connections
  club = models.ForeignKey('row.Club', related_name='asset_models')
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
  club = models.ForeignKey('row.Club', related_name='assets')
  model = models.ForeignKey('row.AssetModel', related_name='assets')
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  # Properties
  name = models.CharField(max_length=255)
  description = models.TextField()


class AssetInstance(Model):
  class Meta:
    permissions = ()

  # Connections
  asset = models.ForeignKey('row.Asset', related_name='instances')
  team = models.ForeignKey('row.Team', related_name='assets')
  in_possession_of = models.ForeignKey('row.Team', related_name='external_assets', null=True)

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
