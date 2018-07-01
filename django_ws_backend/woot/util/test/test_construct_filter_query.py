
from django.db.models import Q
from django.test import TestCase

from ..construct_filter_query import composite_parse, construct_filter_query

class constants:
  KEY = '_key'
  VALUE = '_value'

class BasicTestCase(TestCase):
  def setUp(self):
    self.composite = 'username & ( email | password )'
    self.components = {
      'username': {
        constants.KEY: 'username__contains',
        constants.VALUE: 'a',
      },
      'email': {
        constants.KEY: 'email__contains',
        constants.VALUE: 'a',
      },
      'password': {
        constants.KEY: 'password__contains',
        constants.VALUE: 'a',
      },
    }

  def test_composite_parse(self):

    expected = Q(**{'username__contains': 'a'}) | (Q(**{'email__contains': 'a'}) | ~Q(**{'password__contains': 'a'}))

    print(expected)
    # print(composite_parse(self.composite, self.components))

    self.assertTrue(False)

    self.filter = {
      '_and': {
        '_and': [
          {
            '_key': 'username__contains',
            '_value': 'a',
          },
        ],
        '_or': [
          {
            
          },
        ],
      },
    }
