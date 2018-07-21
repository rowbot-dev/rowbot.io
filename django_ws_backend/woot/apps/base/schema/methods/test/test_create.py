
import json
from django.db import models
from django.test import TestCase

from apps.base.models import MockModel, MockParentModel
from ..create import CreateSchema

class CreateSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_parent = MockParentModel.objects.create(name='mock_parent')
    self.schema = CreateSchema(MockModel)

  def test_create(self):
    payload = {
      'temp_id_1': {
        'attributes': {
          'name': 'hello',
        },
        'relationships': {
          'parent': self.mock_parent._id,
        },
      },
    }

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))
    print(MockModel.objects.all())

    self.assertTrue(False)
