
from django.test import TestCase
from ..types import types
from ..errors import errors, Error

class ErrorsTestCase(TestCase):
  def setUp(self):
    pass

  def test_errors(self):

    print(errors.CLOSED().code)
    print(errors.SERVER_TYPES().code)
    print(errors.INVALID_KEYS().code)
    print(errors.INVALID_KEYS().code)
    print(errors.INVALID_KEYS().code)
    print(errors.INVALID_KEYS().code)

    self.assertTrue(False)
