
import json
from django.test import TestCase

from ..api import api
from ..models import Member, Role, RoleModel, Club

class APITestCase(TestCase):
  def setUp(self):
    Member.objects.create(username='alfred', email='alfred@alfred.com')
    Member.objects.create(username='alfred1', email='alfred111@alfred.com')
    Member.objects.create(username='wilbur', email='wilbur@wilbur.com')
    member = Member.objects.create(username='jamal', email='aldjamal@wilbur.com')

    club = Club.objects.create(name='club_name')
    role_model = RoleModel.objects.create(club=club)
    Role.objects.create(model=role_model, member=member, nickname='jamal')

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

    # self.assertTrue(False)
    self.assertTrue(True)

  def test_respond_role(self):
    payload = {
      'models': {
        'Role': {
          'attributes': {
            'id': True,
            'date_created': True,
          },
          'methods': {
            'filter': {
              'composite': [
                {
                  'key': 'member__username__contains',
                  'value': 'a',
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
