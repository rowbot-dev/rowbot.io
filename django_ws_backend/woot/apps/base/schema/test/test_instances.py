
import json
from django.db import models
from django.test import TestCase

from ...models import MockParentModel, MockModel
from ..instances import InstancesSchema, InstancesResponse

class InstancesSchemaTestCase(TestCase):
  def setUp(self):
    self.mock_model = MockModel.objects.create(name='name')
    self.schema = InstancesSchema(MockModel)

  def test_filter(self):

    payload = {
      'aacf56cf7869476786531d575a4afab7': {
        'attributes': None,
      },
    }

    response = self.schema.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)

class InstancesResponseTestCase(TestCase):
  def setUp(self):

    self.schema = InstancesSchema(MockModel)
    self.response = self.schema.get_response()

  def test_add_instances(self):
    mock_parent_model = MockParentModel.objects.create(name='parent')
    instances = [
      MockModel.objects.create(name='name1', parent=mock_parent_model),
      MockModel.objects.create(name='name2', parent=mock_parent_model),
      MockModel.objects.create(name='name3', parent=mock_parent_model),
    ]
    attributes = ['name']
    relationships = ['parent']

    self.response.add_instances(instances, attributes, relationships)

    print(json.dumps(self.response.render(), indent=2))

    self.assertTrue(False)
