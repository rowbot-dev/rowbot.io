
import json
from django.db import models
from django.test import TestCase

from ...models import Model
from ..instances import InstancesSchema, InstancesResponse

class InstancesSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_model = MockModel.objects.create(name='name')
    self.schema = InstancesSchema(MockModel)

  def test_filter(self):

    payload = {
      'aacf56cf7869476786531d575a4afab7': {

      }
    }

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))

    # self.assertTrue(False)
    self.assertTrue(True)

class InstancesResponseTestCase(TestCase):
  def setUp(self):
    self.mock_model = MockModel.objects.create(name='name')
    self.schema = InstancesSchema(MockModel)
    self.response = self.schema.get_response()

    print(self.response)

    self.assertTrue(False)
    # self.assertTrue(True)
