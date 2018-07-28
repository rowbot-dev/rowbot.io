
import json

from django.db import models
from django.test import TestCase

from apps.base.models import MockModel, MockParentModel

from ...constants import model_schema_constants
from ..set import SetSchema

class FilterSchemaTestCase(TestCase):
  NAME = 'name'
  new_name = 'new_name'
  PARENT = 'parent'
  mock_parent2 = 'mock_parent2'

  def setUp(self):
    self.mock_parent1 = MockParentModel.objects.create(name='mock_parent1')
    self.mock_parent2 = MockParentModel.objects.create(name=self.mock_parent2)
    self.mock_model = MockModel.objects.create(name='name', parent=self.mock_parent1)
    self.schema = SetSchema(MockModel)

  def test_filter(self):

    payload = {
      self.mock_model._id: {
        model_schema_constants.ATTRIBUTES: {
          self.NAME: self.new_name,
        },
        model_schema_constants.RELATIONSHIPS: {
          self.PARENT: self.mock_parent2,
          'one-to-many': {
            'remove': [],
            'add': [],
          },
        },
      }
    }

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
