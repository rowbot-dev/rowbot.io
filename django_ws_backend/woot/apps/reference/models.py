
import uuid

from django.db import models

from apps.base.schema.constants import model_schema_constants
from apps.base.schema import ModelSchema, ModelMethodsSchema
from apps.base.models import Model, Manager

from .constants import reference_constants
from .retrieve import RetrieveSchema

class ReferenceModelSchema(ModelSchema):
  def add_model(self, model):
    methods_schema = self.children.get(model_schema_constants.METHODS)
    methods_schema.add_model(model)

class ReferenceModelMethodsSchema(ModelMethodsSchema):
  def __init__(self, Model, **kwargs):
    super().__init__(
      Model,
      **kwargs,
    )

    self.children.update({
      reference_constants.RETRIEVE: RetrieveSchema(Model),
    })

  def add_model(self, model):
    retrieve_schema = self.children.get(reference_constants.RETRIEVE)
    retrieve_schema.add_model(model)

class ReferenceManager(Manager):
  def from_queryset(self, queryset):
    reference = self.create()
    for obj in queryset:
      reference.entries.create(value=obj._ref)

    return reference._id

  def from_multiple_querysets(self, querysets):
    reference = self.create()
    for queryset in querysets:
      for obj in queryset:
        reference.entries.create(value=obj._ref)

    return reference._id

  def schema(self):
    return ReferenceModelSchema(self.model)

  def schema_model_methods(self):
    return ReferenceModelMethodsSchema(self.model)

class Reference(Model):
  objects = ReferenceManager()

class Entry(Model):
  reference = models.ForeignKey('reference.Reference', related_name='entries', on_delete=models.CASCADE)
  value = models.CharField(max_length=255)
