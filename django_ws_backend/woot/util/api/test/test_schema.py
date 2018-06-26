
import json
from django.test import TestCase

from util.merge import merge
from ..types import types
from ..schema import Schema
from ..errors import errors

class MockSchema(Schema):
  true_value = 'true'
  false_value = 'false'
  checked_key = 'checked'

  def query(self, payload):
    if self.active_server_type == types.STRUCTURE():
      return merge(
        payload,
        {
          self.checked_key: True,
        },
      )

    return self.true_value if payload else self.false_value

class SchemaRespondTestCase(TestCase):
  def setUp(self):
    self.test_key_1 = 'test1'
    self.test_key_2 = 'test2'
    self.schema = Schema(
      children={
        self.test_key_1: MockSchema(
          server_types=[types.BOOLEAN(), types.STRUCTURE()],
        ),
        self.test_key_2: MockSchema(
          server_types=types.BOOLEAN(),
        ),
      },
    )

  def test_invalid_server_type(self):
    payload = {
      self.test_key_1: 'string',
      self.test_key_2: True,
    }

    response = self.schema.respond(payload)
    self.assertFalse(response.errors)

    test_key_1_response = response.children.get(self.test_key_1)
    self.assertTrue(test_key_1_response.errors)

    test_key_1_server_types = test_key_1_response.server_types
    server_types_error = errors.SERVER_TYPES(test_key_1_server_types)
    self.assertEqual(server_types_error.description, test_key_1_response.errors[0].description)

  def test_no_children(self):
    schema = MockSchema()
    payload = {}

    response = schema.respond(payload)
    rendered_response = response.render()

    self.assertIn(MockSchema.checked_key, rendered_response)

  def test_unrecognised_key(self):
    unrecognised_key = 'unrecognised_key'
    payload = {
      self.test_key_1: True,
      unrecognised_key: False,
    }

    response = self.schema.respond(payload)
    self.assertTrue(response.errors)

    unrecognised_keys_error = errors.UNRECOGNISED_KEYS([unrecognised_key])
    self.assertEqual(unrecognised_keys_error.description, response.errors[0].description)

  def test_children_boolean_payload(self):
    payload = {
      self.test_key_1: True,
      self.test_key_2: False,
    }

    response = self.schema.respond(payload)
    self.assertFalse(response.errors)

    rendered_response = response.render()
    self.assertEqual(rendered_response.get(self.test_key_1), MockSchema.true_value)
    self.assertEqual(rendered_response.get(self.test_key_2), MockSchema.false_value)

  def test_children_structure_payload(self):
    test_key_3 = 'test3'
    test_value_3 = 'test_value_3'
    payload = {
      self.test_key_1: {
        test_key_3: test_value_3,
      },
      self.test_key_2: False,
    }

    response = self.schema.respond(payload)
    self.assertFalse(response.errors)

    rendered_response = response.render()
    self.assertIn(test_key_3, rendered_response.get(self.test_key_1))
    self.assertIn(MockSchema.checked_key, rendered_response.get(self.test_key_1))
    self.assertEqual(rendered_response.get(self.test_key_2), MockSchema.false_value)

class SchemaEmptyTestCase(TestCase):
  def setUp(self):
    self.test_key_1 = 'test1'
    self.test_key_2 = 'test2'
    self.schema = Schema(
      description='Testing the empty schema',
      children={
        self.test_key_1: MockSchema(
          description='The first test entry',
          server_types=[
            types.BOOLEAN('Return the whole entry'),
            types.STRUCTURE('Choose parts of the entry to return')
          ],
          children={
            self.test_key_2: MockSchema(
              description='The second test entry',
              server_types=types.BOOLEAN('Return the whole entry'),
            ),
          }
        ),
        self.test_key_2: MockSchema(
          description='The second test entry',
          server_types=types.BOOLEAN('Return the whole entry'),
        ),
      },
    )

  def test_empty(self):
    empty_response = self.schema.empty()

class SchemaValidateSystemTypesTestCase(TestCase):
  def setUp(self):
    self.schema = MockSchema(server_types=types.BOOLEAN())

  def test_validates(self):
    payload = True

    type_validated = self.schema.validate_server_type(payload)

    self.assertTrue(type_validated)
    self.assertEqual(self.schema.active_server_type, types.BOOLEAN())

  def test_does_not_validate(self):
    payload = 'string'

    type_validated = self.schema.validate_server_type(payload)

    self.assertFalse(type_validated)
    self.assertIsNone(self.schema.active_server_type)
