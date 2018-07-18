
from django.db import models

from apps.base.models import Model

class AssetModel(Model):
  class Meta:
    permissions = ()

  club = models.ForeignKey('rowbot.Club', related_name='asset_models', on_delete=models.CASCADE)
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  reference = models.CharField(max_length=255)
  verbose_name = models.CharField(max_length=255)
  verbose_name_plural = models.CharField(max_length=255)
  description = models.TextField()

class Asset(Model):
  class Meta:
    permissions = ()

  club = models.ForeignKey('rowbot.Club', related_name='assets', on_delete=models.CASCADE)
  model = models.ForeignKey('rowbot.AssetModel', related_name='assets', on_delete=models.CASCADE)
  parts = models.ManyToManyField('self', symmetrical=False, related_name='is_part_of')

  name = models.CharField(max_length=255)
  description = models.TextField()

class AssetInstance(Model):
  class Meta:
    permissions = ()

  asset = models.ForeignKey('rowbot.Asset', related_name='instances', on_delete=models.CASCADE)
  team = models.ForeignKey('rowbot.Team', related_name='assets', on_delete=models.CASCADE)
  in_possession_of = models.ForeignKey('rowbot.Team', related_name='external_assets', null=True, on_delete=models.CASCADE)
  event = models.ForeignKey('rowbot.EventInstance', related_name='assets', null=True, on_delete=models.CASCADE)

  metadata = models.TextField() # replace with django.contrib.postgres.fields.JSONField
