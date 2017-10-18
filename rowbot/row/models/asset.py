
# Django
from django.db import models

# DRF


# Local
from row.models.base import Model

# Asset
class AssetCategory(Model):
  # Properties
  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()


class AssetType(Model):
  # Connections
  category = models.ForeignKey('row.AssetCategory', related_name='types')

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
  type = models.ForeignKey('row.AssetType', related_name='instances')

  # Properties
  name = models.CharField(max_length=255)
  location = models.CharField(max_length=255)
  description = models.TextField()


class AssetInstance(Model):
  class Meta:
    permissions = ()

  # Connections
  asset = models.ForeignKey('row.Asset', related_name='instances')
  team = models.ForeignKey('row.Team', related_name='assets')
  in_possession_of = models.ForeignKey('row.Team', related_name='external_assets')

  # Properties
  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
