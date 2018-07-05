
import json
from django.test import TestCase

from util.merge import merge
from ..types import types
from ..schema import Schema, StructureSchema, ArraySchema, IndexedSchema
from ..errors import errors
from ..constants import constants

class complex_schema_constants:
  SCHEMA_KEY = 'schema_key'
  STRUCTURE_SCHEMA_KEY = 'structure_schema_key'
  ARRAY_SCHEMA_KEY = 'array_schema_key'
  INDEXED_SCHEMA_KEY = 'indexed_schema_key'

class ComplexSchema(StructureSchema):
  def __init__(self, **kwargs):
    super().__init__(**kwargs)
    self.children = {
      complex_schema_constants.STRUCTURE_SCHEMA_KEY: StructureSchema(
        children={
          'key1': StructureSchema(
            children={
              'key11': Schema(),
            },
          ),
          'key2': StructureSchema(
            children={
              'key21': Schema(),
            },
          ),
        },
      ),
      complex_schema_constants.ARRAY_SCHEMA_KEY: ArraySchema(
        template=StructureSchema(
          children={
            'some_key': Schema(),
          },
        ),
      ),
    }

class ComplexSchemaTestCase(TestCase):
  def setUp(self):
    self.schema = ComplexSchema()

  def test_empty(self):
    response = self.schema.respond()

    print(json.dumps(response.render(), indent=2))

    self.assertEqual(response.render(), {})
