
from django.test import TestCase
from ..types import types
from ..errors import error_constants, errors, Error

class ErrorClassTestCase(TestCase):
  def setUp(self):
    self.error = Error()

  def test_error(self):
    self.assertEqual(self.error.render(), {
      error_constants.name: None,
      error_constants.description: None,
    })

class ClosedTestCase(TestCase):
  def setUp(self):
    self.closed_error_with_no_arguments = errors.CLOSED()

  def test_closed(self):
    self.assertEqual(self.closed_error_with_no_arguments.render(), {
      error_constants.name: errors.CLOSED.name,
      error_constants.description: errors.CLOSED.description,
    })

class ServerTypesTestCase(TestCase):
  server_types = [
    types.BOOLEAN(),
    types.INTEGER(),
  ]

  def setUp(self):
    self.server_types_error_with_no_arguments = errors.SERVER_TYPES()
    self.server_types_error = errors.SERVER_TYPES(server_types=self.server_types)

  def test_server_types_error_with_no_arguments(self):
    self.assertEqual(self.server_types_error_with_no_arguments.render(), {
      error_constants.name: errors.SERVER_TYPES.name,
      error_constants.description: errors.SERVER_TYPES.description,
    })

  def test_server_types_error(self):
    self.assertEqual(self.server_types_error.render(), {
      error_constants.name: errors.SERVER_TYPES.name,
      error_constants.description: errors.SERVER_TYPES.description_with_arguments.format(
        ', '.join([str(server_type.type) for server_type in self.server_types])
      ),
    })

class InvalidKeysTestCase(TestCase):
  invalid_keys = [
    'key1',
    'key2',
  ]

  def setUp(self):
    self.invalid_keys_error_with_no_arguments = errors.INVALID_KEYS()
    self.invalid_keys_error = errors.INVALID_KEYS(keys=self.invalid_keys)

  def test_invalid_keys_error_with_no_arguments(self):
    self.assertEqual(self.invalid_keys_error_with_no_arguments.render(), {
      error_constants.name: errors.INVALID_KEYS.name,
      error_constants.description: errors.INVALID_KEYS.description,
    })

  def test_invalid_keys_error(self):
    self.assertEqual(self.invalid_keys_error.render(), {
      error_constants.name: errors.INVALID_KEYS.name,
      error_constants.description: errors.INVALID_KEYS.description_with_arguments.format(
        ', '.join([str(key) for key in self.invalid_keys])
      ),
    })

class InvalidIndexesTestCase(TestCase):
  index_type = types.BOOLEAN()
  invalid_indexes = [
    'index1',
    'index2',
  ]

  def setUp(self):
    self.invalid_indexes_error_with_no_arguments = errors.INVALID_INDEXES()
    self.invalid_indexes_error = errors.INVALID_INDEXES(indexes=self.invalid_indexes, index_type=self.index_type)

  def test_invalid_keys_error_with_no_arguments(self):
    self.assertEqual(self.invalid_indexes_error_with_no_arguments.render(), {
      error_constants.name: errors.INVALID_INDEXES.name,
      error_constants.description: errors.INVALID_INDEXES.description,
    })

  def test_invalid_keys_error(self):
    self.assertEqual(self.invalid_indexes_error.render(), {
      error_constants.name: errors.INVALID_INDEXES.name,
      error_constants.description: errors.INVALID_INDEXES.description_with_arguments.format(
        ', '.join([str(index) for index in self.invalid_indexes]),
        self.index_type.type,
      ),
    })
