
import json
from django.test import TestCase
from util.api.schema import Schema, modes

class models:
  def as_system_model_entries():
    pass

class EmptyPayloadSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = Schema({}, {})

  def test_schema_init(self):
    print(self.schema.root)
