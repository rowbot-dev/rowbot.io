
from django.db import models
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist

from util.api import Schema, Error
from util.is_valid_uuid import is_valid_uuid

from .constants import query_directives, is_valid_query_directive

from .schema import (
  model_schema_constants,
  ModelSchema,
  AttributeSchema,
  RelationshipSchema,
  InstancesSchema,
  ModelMethodsSchema
)

import uuid

ID_FIELD = 'id'

class FieldDoesNotExistError(Error):
  def __init__(self, field, model):
    return super().__init__(
      code='014',
      name='model_field_does_not_exist',
      description='Field <{}> does not exist on the <{}> model'.format(field, model),
    )

class MultipleDirectivesForNonRelatedFieldError(Error):
  def __init__(self, field, directives):
    return super().__init__(
      code='015',
      name='model_multiple_directives',
      description='Multiple directives given for field <{}>: [{}]'.format(field, ','.join(directives)),
    )

class InvalidQueryDirectiveError(Error):
  def __init__(self, field, directive):
    return super().__init__(
      code='016',
      name='model_invalid_directive',
      description='Invalid directive given for field <{}>: <{}>'.format(field, directive),
    )

class Manager(models.Manager):
  use_for_related_fields = True

  def attributes(self):
    return [
      field
      for field in self.model._meta.get_fields()
      if (
        not field.is_relation
        and field.name != ID_FIELD
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
    return super().filter(*args, **kwargs), '7eb995a5-d08f-44ce-bb64-a7a6d57680d9'

  def query_check(self, key, value):
    tokens = key.split(query_directives.JOIN)
    query_errors = []
    field_name, rest_of_tokens = tokens[0], tokens[1:]

    try:
      field = self.model._meta.get_field(field_name)
    except FieldDoesNotExist:
      query_errors.append(FieldDoesNotExistError(field_name, self.model._meta.object_name))
      return query_errors

    if field.is_relation:
      related_field_errors = field.related_model.objects.query_check(query_directives.JOIN.join(rest_of_tokens), value)
      if related_field_errors:
        query_errors.extend(related_field_errors)
        return query_errors
    else:
      if len(rest_of_tokens) > 1:
        query_errors.append(MultipleDirectivesForNonRelatedFieldError(field_name, rest_of_tokens))
        return query_errors
      elif len(rest_of_tokens) == 1:
        [directive] = rest_of_tokens
        if not is_valid_query_directive(directive):
          query_errors.append(InvalidQueryDirectiveError(field_name, directive))
          return query_errors

    return query_errors

  def schema(self):
    return ModelSchema(self.model)

  def schema_attributes(self, authorization=None):
    return AttributeSchema(self.model)

  def schema_relationships(self, authorization=None):
    return RelationshipSchema(self.model)

  def schema_instance_methods(self):
    return Schema(description='No available instance methods')

  def schema_model_methods(self):
    return ModelMethodsSchema(self.model)

  def schema_instances(self):
    return InstancesSchema(self.model)

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
      relationship_field.name: str(getattr(instance, relationship_field.name))
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
