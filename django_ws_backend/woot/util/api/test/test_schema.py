
import json
from django.test import TestCase

from util.merge import merge
from ..types import types
from ..schema import Schema, StructureSchema, ArraySchema, IndexedSchema, TemplateSchema
from ..errors import errors
from ..constants import constants

class SchemaTestCase(TestCase):
  def setUp(self):
    self.schema = Schema(description='Some description')

  def test_simple_response(self):
    payload = 'Sample value'
    response = self.schema.respond(payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = {}
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.server_types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.SERVER_TYPES: {
        server_type.code: server_type.render()
        for server_type in self.schema.server_types
      },
    })

class StructureSchemaTestCase(TestCase):
  def setUp(self):
    self.test_key = 'test'
    self.description = 'Some description'
    self.schema = StructureSchema(
      description=self.description,
      children={
        self.test_key: Schema(),
      }
    )

  def test_simple_response(self):
    payload = {
      self.test_key: 'value',
    }
    response = self.schema.respond(payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = 'Some string'
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.server_types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_child_fails_type_validation(self):
    payload = {
      self.test_key: True,
    }
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.children.get(self.test_key).server_types)

    self.assertEqual(response.render(), {
      self.test_key: {
        constants.ERRORS: {
          error.code: error.render(),
        },
      },
    })

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.SERVER_TYPES: {
        server_type.code: server_type.render()
        for server_type in self.schema.server_types
      },
      constants.CHILDREN: {
        self.test_key: {
          constants.DESCRIPTION: self.schema.children.get(self.test_key).description,
          constants.SERVER_TYPES: {
            server_type.code: server_type.render()
            for server_type in self.schema.children.get(self.test_key).server_types
          },
        },
      },
    })

class ArraySchemaTestCase(TestCase):
  def setUp(self):
    self.test_key = 'test'
    self.description = 'Some description'
    self.schema = ArraySchema(
      description=self.description,
      template=Schema(),
    )

  def test_simple_response(self):
    payload = [
      'value',
    ]
    response = self.schema.respond(payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = 'Some string'
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.server_types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_child_fails_type_validation(self):
    payload = [
      True,
    ]
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.template.server_types)

    self.assertEqual(response.render(), [
      {
        constants.ERRORS: {
          error.code: error.render(),
        },
      },
    ])

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.SERVER_TYPES: {
        server_type.code: server_type.render()
        for server_type in self.schema.server_types
      },
      constants.TEMPLATE: self.schema.template.respond().render(),
    })

class IndexedSchemaTestCase(TestCase):
  def setUp(self):
    self.test_index = 'test'
    self.description = 'Some description'
    self.schema = IndexedSchema(
      description=self.description,
      index_type=types.STRING(),
      template=Schema(),
    )

  def test_simple_response(self):
    payload = {
      self.test_index: 'Some value',
    }
    response = self.schema.respond(payload)
    self.assertEqual(response.render(), payload)

  def test_fails_type_validation(self):
    payload = 'Some string'
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.server_types)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_fails_type_validation_index(self):
    invalid_index = 0
    payload = {
      invalid_index: 'Some value',
    }
    response = self.schema.respond(payload)

    error = errors.INVALID_INDEXES([invalid_index], self.schema.index_type)

    self.assertEqual(response.render(), {
      constants.ERRORS: {
        error.code: error.render(),
      },
    })

  def test_child_fails_type_validation(self):
    payload = {
      self.test_index: True,
    }
    response = self.schema.respond(payload)

    error = errors.SERVER_TYPES(self.schema.template.server_types)

    self.assertEqual(response.render(), {
      self.test_index: {
        constants.ERRORS: {
          error.code: error.render(),
        },
      },
    })

  def test_empty(self):
    response = self.schema.respond()
    self.assertEqual(response.render(), {
      constants.DESCRIPTION: self.schema.description,
      constants.SERVER_TYPES: {
        server_type.code: server_type.render()
        for server_type in self.schema.server_types
      },
      constants.TEMPLATE: self.schema.template.respond().render(),
    })

class TemplateSchemaTestCase(TestCase):
  def setUp(self):
    self.maxDiff = None
    self.schema = TemplateSchema(
      description='Some description',
      template=Schema(),
    )

  def test_simple_response(self):
    payload = {}
    payload_response = self.schema.respond(payload)
    empty_response = self.schema.respond()
    self.assertEqual(payload_response.render(), empty_response.render())
