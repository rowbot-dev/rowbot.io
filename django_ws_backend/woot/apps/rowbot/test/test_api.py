
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
    # print(len(json.dumps(api.empty().empty())))
    self.assertTrue(True)

  def test_respond(self):
    payload = {
      'models': {
        'Member': {
          'methods': {
            'filter': {
              'composite': 'username',
              'components': {
                'username': {
                  '_key': 'username__contains',
                  '_value': 'a',
                },
              },
            },
          },
        },
      },
    }

    response = api.respond(payload)

    print(json.dumps(response.render(), indent=2))

    self.assertTrue(False)
