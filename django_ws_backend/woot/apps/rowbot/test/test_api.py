
import json
from django.test import TestCase

from ..api import api
from ..models import Member

class APITestCase(TestCase):
  def setUp(self):
    Member.objects.create(username='alfred', email='alfred@alfred.com')
    Member.objects.create(username='alfred1', email='alfred111@alfred.com')
    Member.objects.create(username='wilbur', email='wilbur@wilbur.com')

  def test_empty(self):
    # print(json.dumps(api.respond().render(), indent=2))
    self.assertTrue(True)
    # self.assertTrue(False)

  def test_respond(self):
    payload = {
      'models': {
        'Member': {
          'methods': {
            'filter': {
              'composite': [
                {
                  'key': 'username__contains',
                  'value': 'a',
                },
                {
                  'and': [
                    {
                      'key': 'email__contains',
                      'value': 'd',
                    },
                    {
                      'key': 'email__startswith',
                      'value': 'al',
                    },
                  ],
                },
              ],
            },
          },
        },
      },
    }

    response = api.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
    # self.assertTrue(True)
