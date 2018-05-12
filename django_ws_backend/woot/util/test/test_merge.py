
from django.test import TestCase
from util.merge import merge

class MergeTestCase(TestCase):
  def setUp(self):
    pass

  def test_merge(self):
    dictionary_one = {
      'integer': 5,
      'string': 'some string',
      'string2': 'some string2',
      'list': ['lm1', 'lm2', 'lm3'],
      'dictionary': {
        'nested': {
          'string': 'some nested string',
          'list': ['nested lm1'],
        },
        'nested2': {
          'some key': 'something',
        }
      },
    }
    dictionary_two = {
      'integer': 16,
      'string': 'some other string',
      'list': ['lm4', 'lm5', 'lm6'],
      'dictionary': {
        'nested': {
          'string': 'changed nested string',
        },
        'nested3': {
          'string': 'some other nested string',
          'list': ['other nested lm1'],
        },
      },
    }
    dictionary_three = {
      'integer': 18,
      'string2': 'some other string2',
      'list': ['lm7'],
      'dictionary': {
        'nested': {
          'list': 'this list is now a string',
        },
        'nested2': 'this dictionary is now a string',
      },
    }

    merged_dictionary = merge(None, dictionary_one, dictionary_two, dictionary_three)

    self.assertEqual(merged_dictionary, {
      'integer': 18,
      'string': 'some other string',
      'string2': 'some other string2',
      'list': ['lm1', 'lm2', 'lm3', 'lm4', 'lm5', 'lm6', 'lm7'],
      'dictionary': {
        'nested': {
          'string': 'changed nested string',
          'list': 'this list is now a string',
        },
        'nested2': 'this dictionary is now a string',
        'nested3': {
          'string': 'some other nested string',
          'list': ['other nested lm1'],
        },
      },
    })
