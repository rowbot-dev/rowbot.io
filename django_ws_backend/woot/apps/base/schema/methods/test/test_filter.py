
import json
from django.db import models
from django.test import TestCase

from apps.base.models import MockModel, MockParentModel
from ..filter import FilterSchema

class FilterSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_model = MockModel.objects.create(name='name')
    self.schema = FilterSchema(MockModel)

  def test_filter(self):

    payload = {
      'composite': [
        {
          'key': 'name__contains',
          'value': 'a',
        },
      ],
    }

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
