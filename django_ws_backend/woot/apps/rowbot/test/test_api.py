
import json
from django.test import TestCase

from ..api import ModelSchema, api

class ModelSchemaTestCase(TestCase):
  pass

class APITestCase(TestCase):
  def setUp(self):
    pass

  def test_api_schema_render(self):
    print(json.dumps(api.empty().empty(), indent=2))
    print(len(json.dumps(api.empty().empty())))
    self.assertTrue(False)
