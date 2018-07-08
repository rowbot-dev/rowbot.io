
from django.db import models
from django.db.models import Q
from django.core.exceptions import FieldDoesNotExist

from util.api import Schema, Error

from .constants import query_directives, is_valid_query_directive

from .schema import (
  ModelSchema,
  AttributeSchema,
  RelationshipSchema,
  InstancesSchema,
  ModelMethodsSchema
)

import uuid
from uuid import UUID
import string
import random

def random_key():
  chars = string.ascii_uppercase + string.digits
  return ''.join([random.choice(chars) for _ in range(8)])

def is_valid_uuid(uuid_string):
  try:
    if hasattr(uuid_string, 'hex') and is_valid_uuid(uuid_string.hex):
      val = uuid_string
    else:
      val = UUID(uuid_string, version=4)
  except ValueError:
    return False
  return str(val) == uuid_string or val.hex == uuid_string or val == uuid_string

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

  def get(self, **kwargs):
    if self.filter(**kwargs).exists():
      return super().get(**kwargs)
    return None

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

    return []

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
