
import json

from django.db import models
from django.test import TestCase

from apps.base.models import MockModel, MockParentModel

from ...constants import model_schema_constants
from ..set import NullableSchema, RelationshipSetPluralSchema, RelationshipSetSchema

class NullableSchemaTestCase(TestCase):
  class nullable_field:
    null = True
    name = 'nullable'

  def setUp(self):
    self.schema = NullableSchema(self.nullable_field)

  def test_nullable(self):

    payload = {
      'null': True,
    }

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(True)

class RelationshipSetPluralSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = RelationshipSetPluralSchema()

  def test_plural_relationship(self):
    payload = {
      'add': [

      ],
      'remove': [

      ],
    }

    response = self.schema.respond(payload)

    print(response.value.to_add)

    self.assertTrue(True)

class RelationshipSetSchemaTestCase(TestCase):
  class plural_relationship:
    name = 'plural'
    one_to_one = True
    null = False

  class single_relationship:
    name = 'single'
    one_to_one = False
    null = True

  def setUp(self):
    self.schema = RelationshipSetSchema(self.plural_relationship)

  def test_plural_relationship(self):
    payload = {
      'add': [

      ],
      'remove': [

      ],
    }

    response = self.schema.respond(payload)

    print(response.render())

    self.assertTrue(False)
