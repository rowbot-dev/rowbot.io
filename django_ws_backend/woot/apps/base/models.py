
from django.db import models
from django.db.models import Q

from util.merge import merge

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

class Manager(models.Manager):
  use_for_related_fields = True
  def get(self, **kwargs):
    if self.filter(**kwargs).exists():
      return super().get(**kwargs)
    return None

  def query(self, query, authorization=None):
    filter = query.get('filter', {})

    instances = {}
    for instance in self.filter(**filter):
      instances = merge(
        instances,
        {
          instance._id: instance.serialize(),
        }
      )

    return {
      'data': {
        'models': {
          self.model.__name__: {
            'instances': instances,
          },
        },
      },
    }

  def schema(self, authorization=None):
    schema = {}
    for field in self.model._meta.get_fields():
      if field.is_relation:
        schema = merge(
          schema,
          {
            'relationships': {
              field.name: field.related_model.__name__,
            },
          },
        )
      else:
        schema = merge(
          schema,
          {
            'attributes': {
              field.name: field.get_internal_type(),
            },
          },
        )

    return schema

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

  def serialize(self):
    return str(self.date_created)
