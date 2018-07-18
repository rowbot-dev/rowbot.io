
import uuid

from django.db import models
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist

from util.api import Schema, StructureSchema, Error, constants

from .constants import query_directives, is_valid_query_directive
from .schema import (
  model_schema_constants,
  SchemaManagerMixin,
)
from .schema.methods.filter import (
  FieldDoesNotExistError,
  MultipleDirectivesForNonRelatedFieldError,
  InvalidQueryDirectiveError,
)

class models_constants:
  ID = 'id'

class Manager(models.Manager, SchemaManagerMixin):
  use_for_related_fields = True

  def attributes(self):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        not field.is_relation
        and field.name != models_constants.ID
      )
    ]

  def relationships(self):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        field.is_relation
      )
    ]

  def get(self, **kwargs):
    if super().filter(**kwargs).exists():
      return super().get(**kwargs)
    return None

  def filter(self, *args, **kwargs):
    return super().filter(*args, **kwargs)

  def query_check(self, key, value):
    tokens = key.split(query_directives.JOIN)
    query_errors = []
    field_name, rest_of_tokens = tokens[0], tokens[1:]

    try:
      field = self.model._meta.get_field(field_name)
    except FieldDoesNotExist:
      query_errors.append(FieldDoesNotExistError(field=field_name, model=self.model._meta.object_name))
      return query_errors

    if field.is_relation:
      related_field_errors = field.related_model.objects.query_check(query_directives.JOIN.join(rest_of_tokens), value)
      if related_field_errors:
        query_errors.extend(related_field_errors)
        return query_errors
    else:
      if len(rest_of_tokens) > 1:
        query_errors.append(MultipleDirectivesForNonRelatedFieldError(field=field_name, directives=rest_of_tokens))
        return query_errors
      elif len(rest_of_tokens) == 1:
        [directive] = rest_of_tokens
        if not is_valid_query_directive(directive):
          query_errors.append(InvalidQueryDirectiveError(field=field_name, directive=directive))
          return query_errors

    return query_errors

  def serialize(self, instance, attributes=[], relationships=[]):
    return {
      model_schema_constants.ATTRIBUTES: self.serialize_attributes(instance, attributes=attributes),
      model_schema_constants.RELATIONSHIPS: self.serialize_relationships(instance, relationships=relationships),
    }

  def serialize_attributes(self, instance, attributes=attributes):
    return {
      attribute_field.name: str(getattr(instance, attribute_field.name))
      for attribute_field
      in self.attributes()
      if attribute_field.name in attributes
    }

  def serialize_relationships(self, instance, relationships=relationships):
    return {
      relationship_field.name: (
        (
          getattr(instance, relationship_field.name)._ref
          if getattr(instance, relationship_field.name) is not None
          else constants.NULL
        )
        if relationship_field.one_to_one or relationship_field.many_to_one
        else [
          related_object._ref
          for related_object
          in getattr(instance, relationship_field.name).all()
        ]
      )
      for relationship_field
      in self.relationships()
      if relationship_field.name in relationships
    }

class Model(models.Model):

  objects = Manager()

  class Meta:
    abstract = True

  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  date_created = models.DateTimeField(auto_now_add=True)

  @property
  def _id(self):
    return self.id.hex

  @property
  def _ref(self):
    return '{}.{}'.format(self.__class__.__name__, self._id)

class MockParentModel(Model):
  class Meta:
    app_label = 'base'

  name = models.CharField(max_length=255)

class MockModel(Model):
  class Meta:
    app_label = 'base'

  parent = models.ForeignKey(MockParentModel, related_name='children', on_delete=models.CASCADE, null=True)
  name = models.CharField(max_length=255)
