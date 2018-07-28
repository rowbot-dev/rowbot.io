
import json

from django.db import models
from django.test import TestCase

from apps.base.models import MockModel, MockParentModel

from ...constants import model_schema_constants
from ..set import (
  NullableSchema,
  RelationshipSetPluralSchema,
  RelationshipSetSchema,
  SetSchema,
)

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
    one_to_one = False
    many_to_one = False
    null = False

  class single_relationship:
    name = 'single'
    one_to_one = True
    many_to_one = False
    null = True

  def setUp(self):
    self.schema = RelationshipSetSchema(self.single_relationship)

  def test_plural_relationship(self):
    payload = {
      'null': False,
    }

    response = self.schema.respond(payload=payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(True)

class SetSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent1 = MockParentModel.objects.create(name='1')
    self.mock_parent2 = MockParentModel.objects.create(name='2')
    self.mock_model = MockModel.objects.create(parent=self.mock_parent1, name='name')
    self.mock_other1 = MockModel.objects.create(parent=self.mock_parent1, name='other1')
    self.mock_other2 = MockModel.objects.create(parent=self.mock_parent1, name='other2')
    self.mock_model.under.add(self.mock_other1)

    self.schema = SetSchema(MockModel)

  def test_set(self):
    payload = {
      self.mock_model._id: {
        model_schema_constants.ATTRIBUTES: {
          'name': 'welrkjwelkrwer',
        },
        model_schema_constants.RELATIONSHIPS: {
          'parent': {
            'null': True,
          },
          'under': {
            'add': [
              self.mock_other2._id,
            ],
            'remove': [
              self.mock_other1._id,
            ],
          },
        },
      },
    }

    response = self.schema.respond(payload=payload)

    print(json.dumps(response.render(), indent=2))

    self.mock_model.refresh_from_db()
    print(self.mock_other1._id, self.mock_other2._id, self.mock_model.under.all(), self.mock_model.parent, self.mock_model.name)

    self.assertTrue(False)
